class kdict(dict):
	r"""Like a dict but accessible with x.key and x["key"] if key passes str.isidentifier()"""

	def __getattr__(self, name: str):
		if name in self and name.isidentifier():
			return self[name]
		raise KeyError(f"'{name}'")
	
	def __setattr__(self, name, value) -> None:
		self[name] = value