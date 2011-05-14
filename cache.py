class CacheQueue(object):
	def __init__(self, size):
		self.size = size
		self.keys = []
		self.data = {}
		
	def has_key(self, key):
		return key in self.data
	
	def append(self, key, obj):
		self.remove(key)
		if len(self.keys) >= self.size:
			self.remove(self.keys[0])
		self.keys.append(key)
		self.data[key] = obj

	def remove(self, key):
		if key in self.data:
			self.keys.remove(key)
			del self.data[key]
			
	def __getitem__(self, key):
		"do not use this method to append data"
		return self.data[key]
		
	def get(self, key, default=None):
		return self.data.get(key, default)