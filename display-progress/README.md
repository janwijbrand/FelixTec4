# Display progress

Gcode post processor that use `M530 S1` and `M530 S0` command to respectively enable and disable the printing mode display. It then intersperses `M532 x.y% L0` commands that report progress codes in the original gcode file. It sends the `M531 filename` command to set display the file being printed.

## Notes

* Replaces the original gcode file with the processed data file
* Replaces all existing `M117` commands in the gcode file
* Assumes pre-layer change lines to be added by slicer for detecting layer change.
* Tries to measure filament "position", uses that to compute total amount of filament used and for tracking progress.
* ~~Logs (naively) to `/tmp/progressed.log`~~
* Can be used as a Slic3r post processor
* See [http://reprap.org/wiki/G-code#M530:_Enable_printing_mode]
* See [http://reprap.org/wiki/G-code#M531:_Set_print_name]
* See [http://reprap.org/wiki/G-code#M532:_Set_print_progress]
* See [TODO.md]
