if __name__ != "__main__": #if run via wsgi, make sure to chdir into the appropriate dir
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)

import web, helper, model

urls = (
    '^/?$', 'index',
)

# do some configuration
web.config.base_url = 'http://webpyus'

# init app
webpyapp = web.application(urls, globals())

# start session
session = web.session.Session(webpyapp, web.session.DiskStore('sessions'), initializer = {'flash': None })
# add session to web context
def session_hook():
    web.ctx.session = session

webpyapp.add_processor(web.loadhook(session_hook))

# set up views
view = web.template.render('views/', base='base', globals = { 'helper': helper, 'hasattr': hasattr, 'str': str })


# page handlers
class index:
    def GET(self):
        return view.index()

# run it
if __name__ == "__main__":
    webpyapp.run()
else:
    web.config.debug = True
    application = webpyapp.wsgifunc()
