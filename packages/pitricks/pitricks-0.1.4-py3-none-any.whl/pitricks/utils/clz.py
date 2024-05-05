from typing import Any

__all__ = ['Conf', 'Empty']

class Empty:
  def __getattribute__(self, __name: str):
    return self
  def __call__(self, *args, **kwds):
    return self


_getattr = object.__getattribute__
class Conf:
  
  # Start by filling-out the abstract methods
  def __init__(self, dict=None, /, **kwargs):
    data = {}
    if dict is not None:
      data.update(dict)
    if kwargs:
      data.update(kwargs)
    self.data = data

  def __getitem__(self, key):
    data = _getattr(self, 'data')
    if key in data:
      if isinstance(data[key], dict):
        ret = _getattr(self, '__new__')(_getattr(self, '__class__'))
        _getattr(ret, '__init__')(data[key])
        return ret
      else:
        return data[key]
    raise KeyError(key)

  # Modify __contains__ to work correctly when __missing__ is present
  def __contains__(self, key):
    return key in _getattr(self, 'data')

  # Now, add the methods in dicts but not in MutableMapping
  def __repr__(self):
    return repr(_getattr(self, 'data'))
  
  def __getattribute__(self, key: str) -> Any:
    return _getattr(self, '__getitem__')(key)
