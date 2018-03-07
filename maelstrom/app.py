import pathlib

from tornado import ioloop, web

from maelstrom import ffmpeg

video = pathlib.Path('bean.mkv')


class MasterManifestHandler(web.RequestHandler):

    def get(self):
        self.write('\n'.join(ffmpeg.make_master_manifest()))


class PlaylistManifestHandler(web.RequestHandler):

    def get(self):
        self.write('\n'.join(ffmpeg.make_playlist_manifest(
            ffmpeg.get_duration_seconds(video))))


def make_app():
    return web.Application([
        ('/stream/master.m3u8', MasterManifestHandler),
        ('/stream/playlist.m3u8', PlaylistManifestHandler),
        ('/stream/(.*)', web.StaticFileHandler, {'path': 'transcode'}),
        ('/(.*)', web.StaticFileHandler, {
            'path': 'static',
            'default_filename': 'index.html'})
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    ioloop.IOLoop.current().start()
