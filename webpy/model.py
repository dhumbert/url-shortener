import web, helper, app
from datetime import datetime

db = web.database(
    dbn=web.config.db_dbn, 
    host=web.config.db_host, 
    db=web.config.db_name, 
    user=web.config.db_user, 
    passwd=web.config.db_pass
)

# base 62 encode table IDs: http://stackoverflow.com/questions/742013/how-to-code-a-url-shortener
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shorten(url):
    if not url:
        raise ValueError('URL cannot be blank')
    
    if url[:7] != 'http://':
        url = 'http://' + url
    
    id = db.insert('urls', 
        url=url,
        created=datetime.now()
    )
    
    hash = encode_hash(id)
    return hash
    
def redirect(hash):
    if not hash:
        raise ValueError('Hash cannot be blank')
        
    id = decode_hash(hash)
    if not id:
        raise ValueError('Invalid hash')
        
    url = db.select('urls', where='id=$id', vars=locals(), limit=1)
    if not url:
        raise KeyError('URL not found')
    
    url = url[0]
    
    record(url.id)
    
    return url.url

def record(id):
    db.insert('clicks',
        url_id = id,
        ip = web.ctx.env['REMOTE_ADDR'],
        user_agent = web.ctx.env['HTTP_USER_AGENT'],
        referrer = web.ctx.env['HTTP_REFERER'],
        created = datetime.now()
    )
    
def urls():
    urls = db.select('urls', order="created DESC")
    urls = map(attach_url_data, urls)
    return urls
    
def attach_url_data(url):
    url.hashed_url = helper.site_url('/'+encode_hash(url.id))
    url.clicks = db.select('clicks', where="url_id=$url_id", vars={'url_id': url.id}, order='created ASC')
    
    return url
    
def get_url(id):
    if not id:
        raise KeyError('URL not found')
    
    url = db.select('urls', where="id=$id", vars={'id':id}, limit=1)
    url = url[0]
    
    url = attach_url_data(url)
    return url
 
def delete_url(id):
    if not id:
        raise KeyError('URL not found')
    
    db.delete('urls', where="id=$id", vars={'id':id})
 
def encode_hash(id):
    return base62_encode(id)

def decode_hash(hash):
    return base62_decode(hash)
    
def base62_encode(num):
    if (num == 0):
        return ALPHABET[0]
        
    arr = []
    base = len(ALPHABET)
    while num:
        rem = num % base
        num = num // base
        arr.append(ALPHABET[rem])
        
    arr.reverse()
    return ''.join(arr)
    
def base62_decode(string):
    base = len(ALPHABET)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += ALPHABET.index(char) * (base ** power)
        idx += 1

    return num