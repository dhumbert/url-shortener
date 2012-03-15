if __name__ != "__main__": #if run via wsgi, make sure to chdir into the appropriate dir
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)

import web, helper, model

urls = (
    '^/?$', 'index',
    '/shorten', 'shorten',
    '/([0-9A-Za-z]+)', 'redirect',
)

# do some configuration
web.config.base_url = 'http://localhost:8080'

# init app
webpyapp = web.application(urls, globals())

# start session
session = web.session.Session(webpyapp, web.session.DiskStore('sessions'), initializer = {'flash': None })
# add session to web context
def session_hook():
    web.ctx.session = session

webpyapp.add_processor(web.loadhook(session_hook))

# set up views
view = web.template.render('views/', base='base', globals = { 'helper': helper })


# page handlers
class index:
    def GET(self):
        urls = model.urls()
        return view.index(urls, model.encode_hash)
        
class shorten:
    def POST(self):
        hash = model.shorten(web.input().url)
        web.ctx.session.flash = 'Shortened URL created'
        raise web.seeother(helper.site_url())

class redirect:
    def GET(self, hash):
        try:
            url = model.redirect(hash)
            raise web.seeother(url)
        except KeyError:
            raise web.notfound()
        except ValueError:
            raise web.notfound()
        
# run it
if __name__ == "__main__":
    webpyapp.run()
else:
    web.config.debug = True
    application = webpyapp.wsgifunc()
