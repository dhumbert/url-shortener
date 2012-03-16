import web, helper

# @restricted decorator to require login
def restricted(func):
    def decorator(self, *args, **kwargs):
        if not hasattr(web.ctx.session, 'user_id'):
            raise web.seeother(helper.site_url('/login'))
        else:
            return func(self, *args, **kwargs)
        
    return decorator