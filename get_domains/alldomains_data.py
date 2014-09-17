# *-* coding : utf-8 *-*
import pymongo
import datetime

class AllDomainsData(object):
	"""docstring for SubdomainData"""
	def __init__(self, server, username, password):
		self.client = pymongo.MongoClient(server)
		self.client.subdomains.authenticate(username, password)
		db = self.client['subdomains']
		self.collection = db['alldomains']


	def query(self, domain):
		ret = self.collection.find({'domain' : domain})
		return ret

	def query_time(self, domain):
		t = self.collection.find_one({'domain' : domain}, {'time' : 1})
		return t

	def is_expired(self, domain):
		now = datetime.datetime.now()
		t = self.query_time(domain)
		if not t:
			return True
			
		timedelta = (now - t.get('time')).days
		if timedelta > 7:
			return True
		else:
			return False
			

	def insert(self, domain, values):
		self.collection.remove({'domain' : domain})
		self.collection.insert(values)


if __name__ == '__main__':
	server = '127.0.0.1'
	username = 'xsec'
	password = 'xsec'

	mongodb = AllDomainsData(server, username, password)
	