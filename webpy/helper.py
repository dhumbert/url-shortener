import web

def site_url(page=None):
    if page is not None:
        if page[0] == '/' and web.config.base_url[-1] == '/':
            page = page[1:]
        return web.config.base_url + page
    else:
        return web.config.base_url

def print_flash():
    if web.ctx.session.flash is not None:
        flash = web.ctx.session.flash
        web.ctx.session.flash = None
        return ("<div class=\"alert-message info\">"
                "<a class=\"close\" href=\"javascript:void(0);\">x</a>"
                "<p>"+flash+"</p>"
                "</div>")

def print_error(message):
    return ("<div class=\"alert-message error\">"
            "<a class=\"close\" href=\"javascript:void(0);\">x</a>"
            "<p>"+message+"</p>"
            "</div>")

def get_value(key, obj, default=''):
    if hasattr(web.input(), key) and getattr(web.input(), key):
        return getattr(web.input(), key)
    elif hasattr(obj, key) and getattr(obj, key):
        return getattr(obj, key)
    else:
        return default

def dropdown(name, opts = {}, selected_value = None):
    dropdown_html =  '<select name="{0}" id="{0}">'.format(name)
    for key, value in opts.items():
        if key == selected_value:
            selected = ' selected="selected"'
        else:
            selected = ''
        dropdown_html += '<option value="{0}"{1}>{2}</option>'.format(key, selected, value)
    
    dropdown_html += '</select>'
    return dropdown_html
