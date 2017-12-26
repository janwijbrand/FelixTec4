# Display progress

Gcode post processor that intersperses `M117` codes in the original gcode file sending the print progress as a simple progress bar and percentage to the printer's display.

## Notes

* Replaces the original gcode file with the processed data
* Replaces all existing `M117` commands in the gcode file
* Logs (naively) to `/tmp/progressed.log`
* Can be used as a Slic3r post processor
* See [TODO.md]
