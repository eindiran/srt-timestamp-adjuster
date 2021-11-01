#!/usr/bin/env python3
'''
srt_timestamp_adjuster_gui.py

Increment or decrement all the timestamps in an SRT file by a specified offset,
producing a new version of the .srt file with modified timestamps.

This is the GUI version, which uses Gooey to convert the CLI version
to a GUI app.

Info on the SRT file format can be found here: https://docs.fileformat.com/video/srt/
'''
from datetime import datetime, timedelta
from gooey import Gooey, GooeyParser


VERBOSE_LOGGING = False
RANGE_MARKER = '-->'


def generate_new_srt_file(srt_file: str, output_srt_file: str, offset_ms: int,
                          time_format: str) -> None:
    '''
    Increment all timestamps in an SRT file. Takes an input file, an output file,
    an offset of milliseconds, and a time format in strptime/strftime notation.
    '''
    lines = []
    with open(srt_file, 'r') as f:
        for i, line in enumerate(f):
            if RANGE_MARKER in line:
                # Change these range lines by incrementing both timestamps in them
                new_line = increment_line(line, offset_ms, time_format)
                if VERBOSE_LOGGING:
                    print(f'Old line {i}: {line}')
                    print(f'New line {i}: {new_line}')
                lines.append(new_line)
            else:
                # Leave lines without the range marker '-->' alone
                lines.append(line)
    with open(output_srt_file, 'w') as o:
        for line in lines:
            o.write(line)


def increment_line(line: str, offset_ms: int, time_format: str) -> str:
    '''
    Increment the two timestamps in a single line.
    The lines are composed of a start timestamp, the
    '-->' symbol, and an end timestamp. Returns a new line
    with the modified timestamps.
    '''
    ts1, ts2 = (datetime.strptime(x.strip(), time_format) for x in line.split(RANGE_MARKER))
    offset = timedelta(milliseconds=offset_ms)
    return ' --> '.join([
        datetime.strftime(ts1 + offset, time_format),
        datetime.strftime(ts2 + offset, time_format),
    ]) + '\n'


@Gooey(
    program_name='SRT Timestamp Adjuster'
)
def main() -> None:
    '''
    Run the GUI tool:
        (1) parse the arguments filled in to the app by the user
        (2) call generate_new_srt_file() to do all the heavy lifting.
    '''
    parser_description = 'Take an SRT file and change each timestamp in it by a specified amount'
    tf_description = 'Specify the format of timestamps using strptime/strftime notation ' + \
        '(default: \'%H:%M:%S,%f\')'
    delta_description = 'Offset each timestamp in the file by this many milliseconds ' + \
        '(may be any signed integer)'
    parser = GooeyParser(description=parser_description)
    parser.add_argument('-i', '--input_file', type=str, required=True,
                        metavar='Input file',
                        help='SRT file to use as the starting point')
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        metavar='Output file',
                        help='SRT file that will be created')
    parser.add_argument('-d', '--delta', type=int, required=True,
                        metavar='Offset',
                        help=delta_description)
    parser.add_argument('-t', '--time_format', type=str, required=False,
                        metavar='Time format string',
                        help=tf_description)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        metavar='Verbose',
                        help='Turn up the logging')
    args = parser.parse_args()
    input_filename = args.input_file
    output_filename = args.output_file
    time_format = args.time_format if args.time_format else '%H:%M:%S,%f'
    offset = args.delta
    # pylint: disable=global-statement
    global VERBOSE_LOGGING
    VERBOSE_LOGGING = args.verbose
    if VERBOSE_LOGGING:
        print(f'Arguments: {args}')
        print(f'Parsed into: [input file {input_filename}], [output file {output_filename}], ' +
              f'[delta {offset}], and [time format "{time_format}"]')
    try:
        generate_new_srt_file(input_filename, output_filename, offset, time_format)
    except (ValueError, TypeError) as err:
        raise ValueError('Failed to parse SRT file: incorrect format') from err
    print(f'Completed processing! The new file is available at {output_filename}')


if __name__ == '__main__':
    main()
