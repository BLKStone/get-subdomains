# *-* coding: utf8 *-*
import json
import time
import requests
import pymongodb

#-------------------------------------------------------------------------
# 获取公司所有域名信息
def get_all_domain():
	#key配置，需要与服务器端的统一
	payload = dict(
		sec_key = "sec_key_string",
		is_cn = 0
		)
	url = "http://111.111.111.111/api/get_domain/"
	response = requests.get(url, params=payload)
	domains = json.loads(response.text).get('data', [])
	return domains


class SubDomains(object):
	"""docstring for SubDomains"""
	def __init__(self, domain):
		self.url = 'http://ips.xsec.io/ips/'
		self.domain = domain
		self.result = dict()

	def get_subdomain(self):
		r = requests.get(self.url, params={'domain' : self.domain})
		if r.text:
			self.result = json.loads(r.text)

		return self.result


if __name__ == '__main__':
	sub_domains = dict()
	all_domains = get_all_domain()
	for item in all_domains:
		domain = item.get('domain')
		sub_domain = SubDomains(domain)
		try:
			result = sub_domain.get_subdomain()
			print result
			sub_domains[domain] = result
		except Exception, e:
			print domain
		else:
			time.sleep(0.5)

	print sub_domains
