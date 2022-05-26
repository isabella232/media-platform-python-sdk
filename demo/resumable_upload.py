from demo.globals import demo_path, resources_dir, client, project_id
from media_platform import FileDescriptor
from media_platform.service.file_service.upload_configuration import Protocol
from media_platform.service.lifecycle import Lifecycle, Action

video_path = demo_path + '/video_720p.mov'


def resumable_upload_demo():
    video = upload()
    print_video_url(video)


def upload() -> FileDescriptor:
    print('uploading video to %s...' % video_path)

    with open(resources_dir + '/video_720p.mov', 'rb') as image:
        return client.file_service.upload_file_request(). \
            set_path(video_path). \
            set_content(image). \
            set_lifecycle(Lifecycle(3600, Action.delete)). \
            set_protocol(Protocol.tus). \
            execute()


def print_video_url(video: FileDescriptor):
    print(f'file url: https://{project_id}.wixmp.com{video.path}')
    print('')


if __name__ == '__main__':
    resumable_upload_demo()
