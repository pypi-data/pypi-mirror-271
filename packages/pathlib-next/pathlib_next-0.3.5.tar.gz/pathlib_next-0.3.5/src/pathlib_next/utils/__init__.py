import collections
import functools as _functools
import time as _time
import typing as _ty
from email.utils import parsedate as _parsedate
from threading import RLock

K = _ty.ParamSpec("K")
V = _ty.TypeVar("V")


class LRU(_ty.Generic[K, V]):

    def __init__(self, func: _ty.Callable[K, V], maxsize=128):
        self.cache = collections.OrderedDict()
        self.func = func
        self._maxsize = maxsize
        self.lock = RLock()

    @property
    def maxsize(self):
        return self._maxsize

    @maxsize.setter
    def maxsize(self, maxsize: int):
        cache = self.cache
        with self.lock:
            self._maxsize = maxsize
            while len(cache) > maxsize:
                cache.pop(last=False)

    def __call__(self, *args: K.args) -> V:
        cache = self.cache
        with self.lock:
            if args in cache:
                cache.move_to_end(args)
                return cache[args]
        result = self.func(*args)
        with self.lock:
            cache[args] = result
            if len(cache) > self._maxsize:
                cache.popitem(last=False)
        return result

    def invalidate(self, *args: K.args) -> V:
        with self.lock():
            if args in self.cache:
                self.cache.pop(args, None)

        return self(*args)


def parsedate(date: _ty.Union[str, _time.struct_time, tuple, float]):
    if date is None:
        return _time.time()
    if isinstance(date, str):
        date = _parsedate(date)
    return _time.mktime(date)


def sizeof_fmt(num: _ty.Union[int, float]):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024:
            if unit:
                return "%3.1f%s" % (num, unit)
            else:
                return int(num)
        num /= 1024.0
    return "%.1f%s" % (num, "Y")


def notimplemented(method):
    @_functools.wraps(method)
    def _notimplemented(*args, **kwargs):
        raise NotImplementedError(f"Not implement method  {method.__name__}")

    return _notimplemented


import ipaddress as _ip
import socket as _socket


def get_machine_ips():
    ips: list[_ip.IPv4Address | _ip.IPv6Address] = list()
    for item in _socket.getaddrinfo(_socket.gethostname(), None):
        protocol, *_, (ip, *_) = item
        if protocol == _socket.AddressFamily.AF_INET:
            ips.append(_ip.ip_address(ip))
        elif protocol == _socket.AddressFamily.AF_INET6:
            ips.append(_ip.ip_address(ip))

    return ips
