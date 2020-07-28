invoke_flow_with_add_sources_response = {
    'invocation': {
        'sources': [],
        'entryPoints': ['addSources1'],
        'callback': None,
        'errorStrategy': 'stopOnError',
        'operationCallbackStatusFilter': []
    },
    'operations': {
        'addSources1': {
            'status': 'success',
            'deleteSources': False,
            'specification': {
                'sources': [{
                    'path': '/source/path.mp3',
                    'fileId': None
                }]
            },
            'callback': None,
            'successors': ['metadata1'],
            'type': 'flow.add_sources'
        },
        'metadata1': {
            'status': 'waiting',
            'deleteSources': False,
            'jobs': ['g_1'],
            'specification': {
                'destination': {
                    'directory': None,
                    'path': '/destination/path.mp3',
                    'lifecycle': None,
                    'acl': 'private'
                },
                'audioExtraMetadata': {
                    'trackName': 'track_name',
                    'lyrics': {
                        'lang': 'eng',
                        'language': 'eng',
                        'text': 'text',
                        'description': 'lyrics_description'
                    },
                    'artist': 'artist',
                    'image': {
                        'url': 'image-url',
                        'mimeType': 'mime_type',
                        'description': 'image_description'
                    },
                    'albumName': 'album_name',
                    'composer': 'composer',
                    'year': 'year',
                    'genre': 'genre',
                    'trackNumber': 'track_number'
                }
            },
            'callback': None,
            'results': [
                {
                    'mimeType': 'audio/mp3',
                    'hash': None,
                    'urn': 'urn:file:123',
                    'dateCreated': '2018-01-11T13:15:57Z',
                    'path': '/destination-path.mp3',
                    'dateUpdated': '2018-01-11T13:15:57Z',
                    'acl': 'private',
                    'type': '-',
                    'id': 'abcd',
                    'size': 1234,
                    'lifecycle': None
                }
            ],
            'extraResults': {},
            'sources': [],
            'successors': [
                'transcode'
            ],
            'type': 'av.extra_metadata.replace'
        }
    },
    'id': '12342134',
    'status': 'success',
    'error': None
}
