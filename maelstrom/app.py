import logging
import pathlib

from tornado import ioloop, web

from maelstrom import handlers, media


class Application(web.Application):

    def __init__(self, **kwargs):
        routes = [
            ('/media/(?P<media_id>[a-z0-9]*)/master.m3u8',
             handlers.MasterManifestHandler),
            ('/media/(?P<media_id>[a-z0-9]*)/(?P<variant_id>[a-z0-9]*).m3u8',
             handlers.VariantManifestHandler),
            ('/media/(.*)', web.StaticFileHandler, {'path': 'transcode'}),
            ('/(.*)', web.StaticFileHandler, {
                'path': 'static',
                'default_filename': 'index.html'})
        ]
        super().__init__(routes, **kwargs)
        self.database = {
            'bean': media.Video('bean', pathlib.Path('bean.mkv')),
            'arde': media.Video('arde', pathlib.Path('arde.mkv'))
        }


def make_app():
    return Application(autoreload=True)


def run():
    logging.basicConfig(level=logging.INFO)

    app = make_app()
    app.listen(8000)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()
