if __name__ != "__main__": #if run via wsgi, make sure to chdir into the appropriate dir
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)

import web, helper, model, environment_config

urls = (
    '^/?$', 'index',
    '/shorten', 'shorten',
    '/url/([0-9]+)', 'url',
    '/([0-9A-Za-z]+)', 'redirect',
)

# do some configuration
web.config.base_url = environment_config.url
web.config.db_dbn = environment_config.db_dbn
web.config.db_host = environment_config.db_host
web.config.db_name = environment_config.db_name
web.config.db_user = environment_config.db_user
web.config.db_pass = environment_config.db_pass

# init app
webpyapp = web.application(urls, globals())

# start session
session = web.session.Session(webpyapp, web.session.DiskStore('sessions'), initializer = {'flash': None })
# add session to web context
def session_hook():
    web.ctx.session = session

webpyapp.add_processor(web.loadhook(session_hook))

# set up views
view = web.template.render('views/', base='base', globals = { 'helper': helper, 'str': str })


# page handlers
class index:
    def GET(self):
        urls = model.urls()
        return view.index(urls, model.encode_hash)
        
class shorten:
    def POST(self):
        try:
            hash = model.shorten(web.input().url)
        except ValueError as e:
            web.ctx.session.flash = 'Error shortening URL: %s' % e
            raise web.seeother(helper.site_url())
        
        web.ctx.session.flash = 'Shortened URL <a target="_blank" href="'+helper.site_url('/'+hash)+'">'+helper.site_url('/'+hash)+'</a> created';
        raise web.seeother(helper.site_url())

class url:
    def GET(self, id):
        url = model.get_url(id)
        return view.url(url)
        
    def DELETE(self, id):
        try:
            model.delete_url(id)
        except KeyError:
            raise web.notfound()
        
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
