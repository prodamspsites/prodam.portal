from Products.Five import BrowserView


class chamadaView(BrowserView):

    def getImage(self, imgsize):
        images = self.context.restrictedTraverse('@@images')
        scale = images.scale(fieldname='image', scale=imgsize)
        return scale.tag()
