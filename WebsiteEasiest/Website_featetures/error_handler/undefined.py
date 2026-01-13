from jinja2 import Undefined
from WebsiteEasiest.logger import logger
class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        logger.warning(f"Undefined variable: {self._undefined_name}, args: {args}, kwargs: {kwargs}")
        return 'undefined'

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = \
        __int__ = __float__ = __complex__ = __pow__ = __rpow__ = \
        __sub__ = __rsub__ = _fail_with_undefined_error
