from communityalmanac.lib.base import BaseController, render

class AboutController(BaseController):
    def about(self):
        return render('/about.mako')
