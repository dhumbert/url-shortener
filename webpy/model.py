import web
from datetime import datetime

db = web.database(dbn='mysql', host='localhost', db='urlshort', user='root', passwd='')
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shorten(url):
    if not url:
        raise ValueError('URL cannot be blank')
    
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
        
    return url[0].url
    
def urls():
    return db.select('urls', order="created DESC")
    
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