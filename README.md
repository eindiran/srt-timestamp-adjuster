# srt-timestamp-adjuster
Have you ever had the problem that a `.srt` file you have doesn't match your copy of the movie, and the all of dialogue in the subtitles is delayed by 2 seconds? This script is for you.

Just plug in the `.srt` file to the script and specify an offset; this script will then produce a new copy of the `.srt` file with the timestamps adjusted by the offset.

A quick way to find the offset is to open the original `.srt` file in an editor and find the first timestamp matching dialogue; hop to that point in your video player and check how close the timestamps are.

Note that the offset should be specified in milliseconds, and can be positive (the subtitles are early) or negative (the subtitles are late).
