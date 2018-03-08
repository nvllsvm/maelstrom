from tornado import web


class BaseHandler(web.RequestHandler):

    pass


class MasterManifestHandler(BaseHandler):

    def get(self, media_id):
        try:
            video = self.application.database[media_id]
        except KeyError:
            raise web.HTTPError(404)
        self.write(video.manifest.text)


class VariantManifestHandler(BaseHandler):

    def get(self, media_id, variant_id):
        try:
            video = self.application.database[media_id]
            variant = video.manifest.variants[variant_id]
        except KeyError:
            raise web.HTTPError(404)
        self.write(variant.text)
