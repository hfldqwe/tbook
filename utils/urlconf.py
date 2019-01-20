import urllib.parse

def urlencode(url,query):
    ''' 用来处理url '''
    return url + "?" + urllib.parse.urlencode(query)
