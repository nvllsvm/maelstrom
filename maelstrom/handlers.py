import urllib.parse

from tornado import web


class MasterManifestHandler(web.RequestHandler):

    def get(self, media_id):
        try:
            video = self.application.media[media_id]
        except KeyError:
            raise web.HTTPError(404)
        self.write(video.manifest.text)


class VariantManifestHandler(web.RequestHandler):

    def get(self, media_id, variant_id):
        try:
            video = self.application.media[media_id]
            variant = video.manifest.variants[variant_id]
        except KeyError:
            raise web.HTTPError(404)
        self.write(variant.text)


class IndexHandler(web.RequestHandler):

    def get(self):
        media = []
        for mediafile in self.application.media.values():
            url = urllib.parse.quote(
                f'/media/{mediafile.media_id}/master.m3u8'
            )
            media.append((url, mediafile))

        self.render(
            'index.html',
            title=__package__,
            media=media
        )
