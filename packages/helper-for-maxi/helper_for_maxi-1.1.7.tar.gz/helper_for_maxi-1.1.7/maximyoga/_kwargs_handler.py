class KWArgsHandler[_VT]:
	type __allowedKeywordsType = str |\
		tuple[str, type | tuple[type, ...]] |\
		tuple[str, type | tuple[type, ...], object]

	def __init__(
			self,
			kwargs: dict[str, _VT],
			*allowedKeywords: __allowedKeywordsType
	) -> None:
		r"""
		Handles Keyword Arguments for a function
		:param kwargs:
		:param allowedKeywords:
		:raises ValueError: Invalid format for 'allowedKeywords' or disallowed keyword in 'kwargs'
		:raises TypeError: Invalid value type for keyword in 'kwargs'
		"""
		allowedKeywords_: dict[str, tuple[type | tuple[type, ...], object]] = {}
		self.kwargs = {}
		for kw in allowedKeywords:
			if isinstance(kw, tuple) and len(kw) in (2, 3):
				keyword, argType = kw[:2]
				defValue = kw[2] if len(kw) == 3 else None
				allowedKeywords_[keyword] = (argType, defValue)
			elif isinstance(kw, str):
				allowedKeywords_[kw] = (object, None)
			else:
				raise ValueError('Invalid format for allowedKeywords. \n'
				                 'Use either ("keyword", type, defaultValue) ("keyword", type) or "keyword".')
		for keyword, value in kwargs.items():
			if keyword not in allowedKeywords_:
				raise ValueError(f"Invalid keyword '{keyword}' provided.")
			if not isinstance(value, expVT := allowedKeywords_[keyword][0]):
				raise TypeError(
					f"Invalid type for keyword '{keyword}'. Expected {
						expVT.__name__ 
						if not isinstance(expVT, tuple) 
						else f"({" | ".join([vt.__name__ for vt in expVT])})"
					}, got {type(value).__name__}"
				)

		for keyword, (valueType, defValue) in allowedKeywords_.items():
			value = kwargs.get(keyword, defValue)
			if keyword not in allowedKeywords_:
				raise ValueError(f"Invalid keyword '{keyword}' provided.")
			if valueType is not None and not isinstance(value, valueType):
				raise TypeError(
					f"Invalid type for keyword '{keyword}'. Expected {
						valueType.__name__ if not isinstance(valueType, tuple) else (vt.__name__ for vt in valueType)
					}, got {type(value).__name__}.")
			self.kwargs[keyword] = value

	def __getattr__(self, attr) -> _VT:
		if attr in self.kwargs:
			return self.kwargs[attr]
		raise AttributeError(f"'KWArgsHandler' object has no attribute '{attr}'.")

	def __getitem__(self, item):
		if isinstance(item, int):
			raise IndexError("KWArgsHandler does not support indexing!")
		elif not isinstance(item, str):
			raise KeyError("KWArgsHandler only supports keys of type 'str'!")
		if item in self.kwargs:
			return self.kwargs[item]
		raise KeyError(f"KWArgsHandler object has no attribute '{item}'")

	def __repr__(self) -> str:
		return f"KWArgsHandler: {self.kwargs}"