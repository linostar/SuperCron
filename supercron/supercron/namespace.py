class Namespace(dict):
	"""A dict subclass that exposes its items as attributes"""

	def __init__(self, obj={}):
		super(Namespace, self).__init__(obj)

	def __dir__(self):
		return tuple(self)

	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, super(Namespace, self).__repr__())

	def __getattribute__(self, name):
		try:
			return self[name]
		except KeyError:
			msg = "'%s' object has no attribute '%s'"
			raise AttributeError(msg % (type(self).__name__, name))

	def __setattr__(self, name, value):
		self[name] = value

	def __delattr__(self, name):
		del self[name]
