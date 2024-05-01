import functools as _func
import os as _os
import pathlib as _path
import re as _re
import typing as _ty

from . import path as _proto


@_func.cache
def _is_case_sensitive(flavour: _os.path) -> bool:
    return flavour.normcase("Aa") == "Aa"


class _BaseFSPathname(_path.PurePath, _proto.Pathname):
    __slots__ = ()

    @property
    def _parser(self) -> _os.path:
        try:
            return self.parser
        except AttributeError:
            return self._flavour

    @property
    def _path_separators(self) -> _ty.Sequence[str]:
        return (self._parser.pathsep, self._parser.altsep)

    @property
    def _is_case_sensitive(self) -> bool:
        return _is_case_sensitive(self._parser)

    @property
    def segments(self):
        return self.parts

    def with_segments(self, *args: str | _proto.FsPathLike):
        return type(self)(*args)


class PosixPathname(_path.PurePosixPath, _BaseFSPathname):
    __slots__ = ()


class WindowsPathname(_path.PureWindowsPath, _BaseFSPathname):
    __slots__ = ()


class LocalPath(
    _path.WindowsPath if _os.name == "nt" else _path.PosixPath,
    _proto.Path,
    _BaseFSPathname,
):
    __slots__ = ()

    def glob(
        self,
        pattern: str | _proto.FsPathLike,
        *,
        case_sensitive: bool = None,
        include_hidden: bool = False,
        recursive: bool = False,
        dironly: bool = False,
    ):
        """Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.
        """
        if not isinstance(pattern, (str, _re.Pattern)):
            pattern = _os.fspath(pattern)
        if dironly is None:
            dironly = (
                isinstance(pattern, str)
                and pattern
                and pattern[-1] in self._path_separators
            )
        yield from _proto.Path.glob(
            self,
            pattern,
            case_sensitive=case_sensitive,
            include_hidden=include_hidden,
            recursive=recursive,
            dironly=dironly,
        )
