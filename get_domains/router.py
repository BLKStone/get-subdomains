# -*- coding:utf8 -*-

#导入模块中的各个类
from domain_server import *


#------------------------------------------------------------------------
#路由配置
routers = [
        (r"/", MainHandler),
        (r"/ips/", MainHandler),
        (r'/alldomains/', AllDomainsHandler)
        ]

settings = dict(
            xsrf_cookies = False,
            cookie_secret = "www.xsec.io"
            )
