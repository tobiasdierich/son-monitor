import json,urllib2

class Http(object):
    def __init__(self):
        self
        
    def GET(self,url_,headers_):
        try: 
            req = urllib2.Request(url_)
            req.add_header('Content-Type','application/json')
            response=urllib2.urlopen(req)
            code = response.code
            data = json.loads(response.read())
            return data
        
        except urllib2.HTTPError, e:
            return e.code
        except urllib2.URLError, e: 
            return e
        except ValueError, e:
            return e

    def POST(self, url_,headers_,data_):
        try: 
            req = urllib2.Request(url_)
            req.add_header('Content-Type','text/html')
            req.get_method = lambda: 'POST'
            response=urllib2.urlopen(req,data_)
            code = response.code  
            return code
        except urllib2.HTTPError, e:
            return e.code
        except urllib2.URLError, e:
            return e
