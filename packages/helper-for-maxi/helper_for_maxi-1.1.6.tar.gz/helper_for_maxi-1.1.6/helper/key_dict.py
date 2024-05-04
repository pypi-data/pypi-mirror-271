class kdict(dict):
	r"""Like a dict but accessible with x.key and x["key"]

	A class that creates a dict that is also accessible by using x.key, not just by using x["key"]. Only works with keys that pass str.isidentifier()!

	How To Use
	----------
	x = kdict({"key": value, ...}); y = x.key
	print(y) # Output: value

	OR

	d = {"key": value, ...}; x = kdict(d); y = x.key
	print(y) # Output: value
	"""
	def __getattr__(self, name:str):
		if name in self and name.isidentifier():
			return self[name]
		raise KeyError(f"'{name}'")
	
	def __setattr__(self, name, value) -> None:
		self[name] = value