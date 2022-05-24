import json
import os
import sys

from demo.globals import demo_path, client
from media_platform.service.live_service.live_stream import LiveStream
from media_platform.service.live_service.stream_protocol import StreamProtocol

archive_path = demo_path + '/archive1.zip'
extracted_path = demo_path + '/extracted'
report_path = extracted_path + '/report.csv'


def live_stream_demo(output_format='json'):
    stream = client.live_service.open_stream_request(). \
        set_connect_timeout(60). \
        set_reconnect_timeout(60). \
        set_protocol(StreamProtocol.rtmp). \
        execute()  # type: LiveStream

    if output_format == 'json':
        print(json.dumps(stream.serialize(), indent=4))
    else:
        server, stream_key = os.path.split(stream.publish_endpoint.url)
        print('Server: ' + server)
        print('Stream Key: ' + stream_key)
        print('Playback url: https:' + stream.playback[0].path)

        stream = client.live_service.get_stream_request().set_id(stream.id).execute()
        print('Got stream: %s' % stream.serialize())


def output_format_from_params():
    return sys.argv[1] if len(sys.argv) > 1 else 'json'


if __name__ == '__main__':
    output_format = output_format_from_params()
    live_stream_demo(output_format)
