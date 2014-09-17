# *_* coding : utf8 *-*
import re
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup

class AllDomains(object):
	"""docstring for AllDomains"""
	def __init__(self, domain):
		url = 'http://fofa.so/lab/alldomains'
		self.domain = domain
		self.session = requests.Session()
		ret = self.session.get(url)
		print ret.headers
		result = ret.text.encode('utf8')
		soup = BeautifulSoup(result)
		meta = soup.find_all('meta', {'name' : 'csrf-token'})
		r = r'<meta content="(.+?)" name="csrf-token"/>'
		p = re.compile(r)
		self.csrf_token = p.findall(str(meta[0]))[0]



	def get_jobId(self):
		url = 'http://fofa.so/lab/addtask/'

		payload = dict(
			taskaction='alldomains',
			domain=self.domain
			)

		headers = {
		'Host': 'fofa.so',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Origin': 'http://fofa.so',
		'Referer': 'http://fofa.so/lab/alldomains',
		'X-CSRF-Token' : self.csrf_token,
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
		}

		ret = self.session.post(url, data=payload, headers=headers)
		print ret.text
		if ret.text:
			result = json.loads(ret.text)
			self.jobId = result.get('jobId')

	def _get_domains(self):
		url = 'http://fofa.so/lab/gettask'
		t = str(time.time()).replace('.', '')
		payload = dict(
			jobId = self.jobId,
			t = t
			)
		ret = self.session.get(url, params=payload)
		if ret:
			finished = json.loads(ret.text).get('finished')
			if finished:
				return json.loads(ret.text)
			else:
				return False

	def all_domains(self):
		ret = []
		while True:
			tmp = self._get_domains()
			if tmp:
				return tmp

	def result(self):
		ret = self.all_domains()
		result = dict(
			domain = self.domain,
			time = datetime.datetime.now(),
			data = ret
			)
		return result

				

if __name__ == '__main__':
	domain = '360.cn'
	domains = AllDomains(domain)
	domains.get_jobId()
	print domains.result()