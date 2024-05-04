from typing import Type, Tuple, Union

class KWArgsHandler:
	r"""Handles allowed keywords and types for values in kwargs

	Makes sure the parsed `kwargs` only contain allowed keywords and the correct types of values for the corresponding keywords

	Parameters
	----------
	kwargs: dict
		The keyword arguments to be used
	
	*allowedKeywords: Union[str, tuple(str, type, any)]
		tuple:
			0: the allowed keyword
			1: the expected type of value (object for any)
			2: the default value, if not given: None
		str: the allowed keyword
	"""
	def __init__(self, kwargs: dict, *allowedKeywords: Tuple[Union[str, Tuple[str, Type[object], object]]]) -> None:
		allowedKeywords_ = {}
		self.kwargs = {}
		for kw in allowedKeywords:
			if isinstance(kw, tuple) and len(kw) in (2, 3):
				keyword, argType = kw[:2]
				defValue = kw[2] if len(kw) == 3 else None
				allowedKeywords_[keyword] = (argType, defValue)
			elif isinstance(kw, str):
				allowedKeywords_[kw] = (object, None)
			else:
				raise ValueError("Invalid format for allowedKeywords. Use either (\"keyword\", type) or \"keyword\".")
		for keyword, (valueType, defValue) in allowedKeywords_.items():
			value = kwargs.get(keyword, defValue)
			if keyword not in allowedKeywords_:
				raise ValueError(f"Invalid keyword '{keyword}' provided.")
			if valueType is not None and not isinstance(value, valueType):
				raise TypeError(f"Invalid type for keyword '{keyword}'. Expected {valueType.__name__}, got {type(value).__name__}.")
			self.kwargs[keyword] = value

	def __getattr__(self, name):
		if name in self.kwargs:
			return self.kwargs[name]
		raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'.")
	
	def __repr__(self) -> str:
		return f"KWArgsHandler: {self.kwargs}"