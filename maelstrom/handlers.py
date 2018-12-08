import urllib.parse

from tornado import web

from . import transcode


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


class TranscodeHandler(web.RequestHandler):

    async def get(self, media_id, variant_id, segment):
        mediafile = self.application.media[media_id]
        if mediafile not in self.application.actively_transcoding:
            await self.transcode(
                mediafile,
                mediafile.path,
                variant_id,
                mediafile.media_id,
                self.application.transcode_cache,
                segment.split('.')[0]
            )
        self.write(
            self.application.transcode_cache.joinpath(
                media_id, variant_id, segment).read_bytes()
        )

    async def transcode(self, mediafile, *args):
        self.application.actively_transcoding.add(mediafile)
        await transcode.transcode(*args)
        self.application.actively_transcoding.pop(mediafile)


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
