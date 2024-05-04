from functools import wraps
from inspect import signature, Parameter
from typing import Callable


def checkParams[P, R](func: Callable[[P], R]) -> Callable[[P], R]:
	r"""
	Checks that all given parameters are the expected type. Excludes **kwargs!
	:param func:
	:raises TypeError: Parameter's value is not of the expected type.
	:return: The decorated function.
	"""
	@wraps(func)
	def wrapper(*args, **kwargs) -> R:
		params = signature(func).parameters
		for arg, param in zip(args, params.values()):
			annot = param.annotation
			if not isinstance(arg, annot) and annot != Parameter.empty:
				raise TypeError(
					f"Invalid type for parameter {param.name}: {type(arg)}. Expected: {annot}"
				)

		for k, v in kwargs.items():
			if k not in params:
				continue
			annot = params[k].annotation
			if not isinstance(v, annot) and annot != Parameter.empty:
				raise TypeError(
					f"Invalid type for parameter '{k}': {type(v)}. Expected: {params[k].annotation}"
				)

		return func(*args, **kwargs)
	return wrapper