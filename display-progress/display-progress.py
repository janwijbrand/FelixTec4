#!/usr/local/bin/python3

import os
import sys
import datetime

comments = 0
controls = 0
display_messages = 0

with open(sys.argv[1], 'r', encoding='ascii') as gcode:
    for line in gcode:
        line = line.strip()
        if line.startswith(';'):
            comments += 1
            continue
        if line.startswith('M117'):
            display_messages += 1
            continue
        controls += 1

    print(sys.argv[1])
    print('{} control commands'.format(controls))
    print('{} comments'.format(comments))
    print('{} display messages'.format(display_messages))

    with open('/tmp/progressed.gcode', 'w', encoding='ascii') as output:
        chunk_counter = 0
        chunk_size = int(controls / 1000)
        write_counter = 0

        gcode.seek(0)
        for line in gcode:
            line = line.strip()
            if line.strip().startswith('M117'):
                continue
            output.write('{}\n'.format(line))
            if line.startswith(';'):
                continue
            chunk_counter += 1
            write_counter += 1
            if chunk_counter == chunk_size:
                chunk_counter = 0
                percentage = write_counter / controls
                progress = int(percentage / 0.05)
                output.write('M117 {:20}{:6.1%}\n'.format(
                    '=' * progress, percentage))
        if chunk_counter:
            output.write('M117 {:20}{:6.1%}\n'.format('=' * 20, 1))

gcode.close()
output.close()

with open('/tmp/progressed.log', 'a', encoding='ascii') as log:
    log.write('processed "{}" ({})\n'.format(
        sys.argv, datetime.datetime.now()))
log.close()

os.replace('/tmp/progressed.gcode', sys.argv[1])
