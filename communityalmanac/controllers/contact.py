from communityalmanac.lib.base import BaseController, render

class ContactController(BaseController):
    def contact(self):
        return render('/contact.mako')
