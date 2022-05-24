#!/bin/bash
export PYTHONPATH=PYTHONPATH:.

stream=$(python demo/live_stream.py json)
echo $stream | jq -r '"https:" + .playbackUrls[0].path'
cmd=$(echo $stream | tee | jq -r '.| "ffmpeg -re -i ~/Movies/ElephantsDream.mp4  -c copy -f flv " + "\"" + .publishEndpoint.url + "\""')
#echo $cmd
bash -c "$cmd"
