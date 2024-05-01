"""Routines for finding the sources that mypy will check"""

from __future__ import annotations

import functools
import os
from typing import Final, Sequence

from mypy.fscache import FileSystemCache
from mypy.modulefinder import PYTHON_EXTENSIONS, BuildSource, matches_exclude, mypy_path
from mypy.options import Options

PY_EXTENSIONS: Final = tuple(PYTHON_EXTENSIONS)


class InvalidSourceList(Exception):
    """Exception indicating a problem in the list of sources given to mypy."""


def create_source_list(
    paths: Sequence[str],
    options: Options,
    fscache: FileSystemCache | None = None,
    allow_empty_dir: bool = False,
) -> list[BuildSource]:
    """From a list of source files/directories, makes a list of BuildSources.

    Raises InvalidSourceList on errors.
    """
    fscache = fscache or FileSystemCache()
    finder = SourceFinder(fscache, options)

    sources = []
    for path in paths:
        path = os.path.normpath(path)
        if path.endswith(PY_EXTENSIONS):
            # Can raise InvalidSourceList if a directory doesn't have a valid module name.
            name, base_dir = finder.crawl_up(path)
            sources.append(BuildSource(path, name, None, base_dir))
        elif fscache.isdir(path):
            sub_sources = finder.find_sources_in_dir(path)
            if not sub_sources and not allow_empty_dir:
                raise InvalidSourceList(f"There are no .py[i] files in directory '{path}'")
            sources.extend(sub_sources)
        else:
            mod = os.path.basename(path) if options.scripts_are_modules else None
            sources.append(BuildSource(path, mod, None))
    return sources


def keyfunc(name: str) -> tuple[bool, int, str]:
    """Determines sort order for directory listing.

    The desirable properties are:
    1) foo < foo.pyi < foo.py
    2) __init__.py[i] < foo
    """
    base, suffix = os.path.splitext(name)
    for i, ext in enumerate(PY_EXTENSIONS):
        if suffix == ext:
            return (base != "__init__", i, base)
    return (base != "__init__", -1, name)


def normalise_package_base(root: str) -> str:
    if not root:
        root = os.curdir
    root = os.path.abspath(root)
    if root.endswith(os.sep):
        root = root[:-1]
    return root


def get_explicit_package_bases(options: Options) -> list[str] | None:
    """Returns explicit package bases to use if the option is enabled, or None if disabled.

    We currently use MYPYPATH and the current directory as the package bases. In the future,
    when --namespace-packages is the default could also use the values passed with the
    --package-root flag, see #9632.

    Values returned are normalised so we can use simple string comparisons in
    SourceFinder.is_explicit_package_base
    """
    if not options.explicit_package_bases:
        return None
    roots = mypy_path() + options.mypy_path + [os.getcwd()]
    return [normalise_package_base(root) for root in roots]


class SourceFinder:
    def __init__(self, fscache: FileSystemCache, options: Options) -> None:
        self.fscache = fscache
        self.explicit_package_bases = get_explicit_package_bases(options)
        self.namespace_packages = options.namespace_packages
        self.exclude = options.exclude
        self.verbosity = options.verbosity

    def is_explicit_package_base(self, path: str) -> bool:
        assert self.explicit_package_bases
        return normalise_package_base(path) in self.explicit_package_bases

    def find_sources_in_dir(self, path: str) -> list[BuildSource]:
        sources = []

        seen: set[str] = set()
        names = sorted(self.fscache.listdir(path), key=keyfunc)
        for name in names:
            # Skip certain names altogether
            if name in ("__pycache__", "site-packages", "node_modules") or name.startswith("."):
                continue
            subpath = os.path.join(path, name)

            if matches_exclude(subpath, self.exclude, self.fscache, self.verbosity >= 2):
                continue

            if self.fscache.isdir(subpath):
                sub_sources = self.find_sources_in_dir(subpath)
                if sub_sources:
                    seen.add(name)
                    sources.extend(sub_sources)
            else:
                stem, suffix = os.path.splitext(name)
                if stem not in seen and suffix in PY_EXTENSIONS:
                    seen.add(stem)
                    module, base_dir = self.crawl_up(subpath)
                    sources.append(BuildSource(subpath, module, None, base_dir))

        return sources

    def crawl_up(self, path: str) -> tuple[str, str]:
        """Given a .py[i] filename, return module and base directory.

        For example, given "xxx/yyy/foo/bar.py", we might return something like:
        ("foo.bar", "xxx/yyy")

        If namespace packages is off, we crawl upwards until we find a directory without
        an __init__.py

        If namespace packages is on, we crawl upwards until the nearest explicit base directory.
        Failing that, we return one past the highest directory containing an __init__.py

        We won't crawl past directories with invalid package names.
        The base directory returned is an absolute path.
        """
        path = os.path.abspath(path)
        parent, filename = os.path.split(path)

        module_name = strip_py(filename) or filename

        parent_module, base_dir = self.crawl_up_dir(parent)
        if module_name == "__init__":
            return parent_module, base_dir

        # Note that module_name might not actually be a valid identifier, but that's okay
        # Ignoring this possibility sidesteps some search path confusion
        module = module_join(parent_module, module_name)
        return module, base_dir

    def crawl_up_dir(self, dir: str) -> tuple[str, str]:
        return self._crawl_up_helper(dir) or ("", dir)

    @functools.lru_cache  # noqa: B019
    def _crawl_up_helper(self, dir: str) -> tuple[str, str] | None:
        """Given a directory, maybe returns module and base directory.

        We return a non-None value if we were able to find something clearly intended as a base
        directory (as adjudicated by being an explicit base directory or by containing a package
        with __init__.py).

        This distinction is necessary for namespace packages, so that we know when to treat
        ourselves as a subpackage.
        """
        # stop crawling if we're an explicit base directory
        if self.explicit_package_bases is not None and self.is_explicit_package_base(dir):
            return "", dir

        parent, name = os.path.split(dir)
        if name.endswith("-stubs"):
            name = name[:-6]  # PEP-561 stub-only directory

        # recurse if there's an __init__.py
        init_file = self.get_init_file(dir)
        if init_file is not None:
            if not name.isidentifier():
                # in most cases the directory name is invalid, we'll just stop crawling upwards
                # but if there's an __init__.py in the directory, something is messed up
                raise InvalidSourceList(f"{name} is not a valid Python package name")
            # we're definitely a package, so we always return a non-None value
            mod_prefix, base_dir = self.crawl_up_dir(parent)
            return module_join(mod_prefix, name), base_dir

        # stop crawling if we're out of path components or our name is an invalid identifier
        if not name or not parent or not name.isidentifier():
            return None

        # stop crawling if namespace packages is off (since we don't have an __init__.py)
        if not self.namespace_packages:
            return None

        # at this point: namespace packages is on, we don't have an __init__.py and we're not an
        # explicit base directory
        result = self._crawl_up_helper(parent)
        if result is None:
            # we're not an explicit base directory and we don't have an __init__.py
            # and none of our parents are either, so return
            return None
        # one of our parents was an explicit base directory or had an __init__.py, so we're
        # definitely a subpackage! chain our name to the module.
        mod_prefix, base_dir = result
        return module_join(mod_prefix, name), base_dir

    def get_init_file(self, dir: str) -> str | None:
        """Check whether a directory contains a file named __init__.py[i].

        If so, return the file's name (with dir prefixed).  If not, return None.

        This prefers .pyi over .py (because of the ordering of PY_EXTENSIONS).
        """
        for ext in PY_EXTENSIONS:
            f = os.path.join(dir, "__init__" + ext)
            if self.fscache.isfile(f):
                return f
            if ext == ".py" and self.fscache.init_under_package_root(f):
                return f
        return None


def module_join(parent: str, child: str) -> str:
    """Join module ids, accounting for a possibly empty parent."""
    if parent:
        return parent + "." + child
    return child


def strip_py(arg: str) -> str | None:
    """Strip a trailing .py or .pyi suffix.

    Return None if no such suffix is found.
    """
    for ext in PY_EXTENSIONS:
        if arg.endswith(ext):
            return arg[: -len(ext)]
    return None
