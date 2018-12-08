import argparse
import logging
import pathlib

from tornado import ioloop, web
import pkg_resources

from . import handlers, media

LOGGER = logging.getLogger(__package__)

STATIC_PATH = pathlib.Path(
    pkg_resources.resource_filename(__package__, 'static')
)
TEMPLATE_PATH = pathlib.Path(
    pkg_resources.resource_filename(__package__, 'templates')
)


def all_files(root):
    files = []
    stack = [root]
    while stack:
        for path in stack.pop().iterdir():
            if path.is_dir():
                stack.append(path)
            elif path.is_file():
                files.append(path)
    return files


class Application(web.Application):

    def __init__(self, paths, transcode_cache, **kwargs):
        routes = [
            ('/media/(?P<media_id>[a-z0-9]*)/master.m3u8',
             handlers.MasterManifestHandler),
            ('/media/(?P<media_id>[a-z0-9]*)/(?P<variant_id>[a-z0-9]*).m3u8',
             handlers.VariantManifestHandler),
            ('/media/(?P<media_id>[a-z0-9]*)/(?P<variant_id>[a-z0-9]*)/(?P<segment>.*)',
             handlers.TranscodeHandler),
            ('/media/(.*)', web.StaticFileHandler, {'path': 'transcode'}),
            ('/', handlers.IndexHandler),
            ('/static/(.*)', web.StaticFileHandler, {
                'path': STATIC_PATH,
                'default_filename': 'index.html'}
             )
        ]
        super().__init__(routes, template_path=TEMPLATE_PATH, **kwargs)

        self.transcode_cache = transcode_cache
        self.add_transform(ServerHeaderTransform)

        self.actively_transcoding = set()

        self.media = {}
        for root in paths:
            for path in all_files(root):
                video = media.Video(path)
                LOGGER.info('Found video "%s" %s', video.path, video.media_id)
                self.media[video.media_id] = video


class ServerHeaderTransform(web.OutputTransform):

    server = '/'.join([
        __package__,
        pkg_resources.get_distribution(__package__).version
    ])

    def transform_first_chunk(self, status_code, headers, chunk, _):
        headers['Server'] = self.server
        return status_code, headers, chunk


def run():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--media',
        type=pathlib.Path,
        action='append',
        required=True
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8000
    )
    parser.add_argument(
        '-t', '--transcode-cache',
        type=pathlib.Path,
        required=True
    )
    args = parser.parse_args()

    app = Application(args.media, args.transcode_cache, autoreload=True)
    app.listen(args.port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()
