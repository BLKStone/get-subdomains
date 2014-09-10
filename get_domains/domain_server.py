# -*- coding:utf8 -*-
import os
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options

from router import *
from config import *
from get_subdomains import SubDomains
from subdomain_data import SubdomainData

#继承自tornado.web.Application类
#---------------------------------------------------------------------------
class Application(tornado.web.Application):
    def __init__(self):
        handlers = routers
        tornado.web.Application.__init__(self, handlers, **settings)

#---------------------------------------------------------------------------
#首页面
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        domain = self.get_argument("domain", "") or "360.cn"
        domain_data = SubdomainData(options.server, options.username, options.password)
        if domain_data.is_expired(domain):
            instance = SubDomains(domain)
            utf8, token = instance.get_token()
            instance.get_submains(token, utf8)
            result = instance.result()
            domain_data.insert(domain, result)
            
        else:
            ret = domain_data.query(domain)
            for item in ret:
                result = item
        del result['_id']
        result['time'] = str(result['time'])

        self.write(json.dumps(result))
        

    def post(self):
        domain = self.get_argument("domain", "") or "360.cn"
        domain_data = SubdomainData(options.server, options.username, options.password)
        if domain_data.is_expired(domain):
            instance = SubDomains(domain)
            utf8, token = instance.get_token()
            instance.get_submains(token, utf8)
            result = instance.result()
            domain_data.insert(domain, result)
            
        else:
            ret = domain_data.query(domain)
            for item in ret:
                del item['_id']
                result = item

        result['time'] = str(result['time'])
        self.write(json.dumps(result))


#---------------------------------------------------------------------------
#主函数
def main():
    app = Application()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
