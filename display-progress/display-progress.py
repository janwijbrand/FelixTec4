#!/usr/local/bin/python3

import os
import sys


controls = 0
has_progress_enabled = False
layers_total = 1


class Filament(object):

    def __init__(self, total):
        self.cummulative = 0
        self.position = 0
        self.total = total

    @property
    def used(self):
        return self.cummulative + self.position

    def progress(self):
        return round((self.used / self.total) * 100, 1)

    def extrude(self, position):
        self.position = position

    def reset(self):
        self.cummulative += self.position
        self.position = 0


with open(sys.argv[1], 'r', encoding='ascii') as gcode:
    filament_length = 0
    filament_total = 0
    previous_z = 0

    for line in gcode:
        line = line.strip()
        if line.startswith('G1 '):
            for param in line.split():
                if param.startswith('E'):
                    filament_length = float(param[1:])
        if line.startswith('G92 '):
            for param in line.split():
                if param.startswith('E'):
                    # Reset extruder position, we can sum the length of used
                    # material to the total now.
                    filament_total += filament_length
                    filament_length = 0
        if line.startswith('M530 S1'):
            has_progress_enabled = True
        if line.startswith(';'):
            if 'before layer change' in line:
                layers_total += 1
            continue
        if line.startswith('M117'):
            continue
        controls += 1

    print(sys.argv[1])
    print('{} control commands'.format(controls))
    print('{} layers'.format(layers_total))
    print('{:.1f}mm filament used'.format(filament_total))

    if not has_progress_enabled:
        print('No enableprinting mode (M530) command detected. Exiting.')
        sys.exit(0)

    with open('/tmp/progressed.gcode', 'w', encoding='ascii') as output:
        filament = Filament(total=filament_total)
        layer = 1
        previous_percentage = None
        previous_z = 0
        track_progress = False

        gcode.seek(0)
        for line in gcode:
            line = line.strip()
            if line.startswith('M530 S1'):
                # Enables "progress display" mode. Start injecting from this
                # point on.
                track_progress = True
            if line.startswith('M530 S0'):
                # Disables "progress display" mode. Stop injecting from this
                # point on.
                track_progress = False
            output.write('{}\n'.format(line))
            if track_progress:
                if line.startswith('G1 '):
                    for param in line.split():
                        if param.startswith('E'):
                            filament.extrude(float(param[1:]))
                if line.startswith('G92 '):
                    for param in line.split():
                        if param.startswith('E'):
                            filament.reset()
                if line.startswith(';'):
                    if 'before layer change' in line:
                        layer += 1
                    continue
                if line.startswith('M117'):
                    continue
                percentage = filament.progress()

                if percentage > 100:
                    import pdb; pdb.set_trace()

                if previous_percentage is None or \
                        percentage > previous_percentage:
                    output.write('M532 X{:.1f} L{}\n'.format(
                        percentage, layer))
                    previous_percentage = percentage

gcode.close()
output.close()

# with open('/tmp/progressed.log', 'a', encoding='ascii') as log:
#     log.write('processed "{}" ({})\n'.format(
#         sys.argv, datetime.datetime.now()))
# log.close()

os.replace('/tmp/progressed.gcode', sys.argv[1])
