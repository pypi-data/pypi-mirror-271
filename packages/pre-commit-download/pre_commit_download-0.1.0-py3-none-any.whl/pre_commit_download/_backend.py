"""Build-backend implementation."""

from dataclasses import dataclass
import glob
import io
import os
import platform
import stat
import sys
import tarfile
from typing import Any, Dict, List, Mapping, Optional, Union
from urllib.request import urlopen
import zipfile

from setuptools.build_meta import build_wheel as original_build_wheel
import tomli


@dataclass
class Distro:
    """Data model for `tool.pre-commit-download.binaries.*` tables."""

    name: str
    sys_platform: str
    platform_machine: str
    url: str
    extract_method: Optional[str] = None
    extract_path: Optional[str] = None
    exec_suffix: str = ""

    @property
    def install_name(self) -> str:
        """Get the executable basename.

        :return: name
        """
        if not self.exec_suffix:
            return self.name
        return f"{self.name}.{self.exec_suffix}"

    def is_suitable(self) -> bool:
        """Check if the distro is an appropriate one for current platform.

        :return: bool
        """
        return (
            self.sys_platform == sys.platform
            and self.platform_machine == platform.machine()
        )

    def download(self) -> bytes:
        """Download and unpack (if required) the executable.

        :raises ValueError: wrong URL
        :return: the executable as bytes
        """
        if not self.url.startswith("http"):
            raise ValueError(f"URL must start with 'http': {self.url}")
        with urlopen(self.url) as resp:  # noqa: S310
            distro = resp.read()
        if self.extract_method:
            distro = extract_from_archive(
                self.extract_method,
                distro,
                self.extract_path or self.install_name,
            )
        return distro

    def install(self, dst: str) -> None:
        """Install the distro.

        :param dst: an installation root
        """
        distro = self.download()
        install_path = os.path.join(dst, self.install_name)
        with open(install_path, "wb") as install:
            install.write(distro)
        os.chmod(
            install_path,
            stat.S_IRWXU
            | stat.S_IRGRP
            | stat.S_IXGRP
            | stat.S_IROTH
            | stat.S_IXOTH,
        )


def extract_from_archive(
    extract_method: str,
    archive_data: bytes,
    path: str,
) -> bytes:
    """Extract a file from an archive.

    :param extract_method: an extraction provider (tarfile, zipfile)
    :param archive_data: an archive as bytes
    :param path: a relative path to the file in the archive
    :raises ValueError: wrong extract method
    :return: an extracted file as bytes
    """
    extractor = {
        "tarfile": extract_from_tar,
        "zipfile": extract_from_zip,
    }
    if extract_method not in extractor:
        methods = set(extractor.keys())
        msg = f"wrong extract method: '{extract_method}'; use {methods}"
        raise ValueError(msg)
    return extractor[extract_method](archive_data, path)


def extract_from_tar(archive_data: bytes, path: str) -> bytes:
    """Extract a file from a .tar.* archive.

    :param archive_data: an archive as bytes
    :param path: a relative path to the file in the archive
    :raises ValueError: wrong path
    :return: an extracted file as bytes
    """
    with io.BytesIO(archive_data) as archive:
        with tarfile.open(fileobj=archive) as tar_file:
            member = tar_file.extractfile(path)
            if member is None:
                raise ValueError(f"not an archive member: '{path}'")
            return member.read()


def extract_from_zip(archive_data: bytes, path: str) -> bytes:
    """Extract a file from a .zip archive.

    :param archive_data: an archive as bytes
    :param path: a relative path to the file in the archive
    :return: an extracted file as bytes
    """
    with io.BytesIO(archive_data) as archive:
        with zipfile.ZipFile(archive) as zip_file:
            return zip_file.read(path)


def read_pyproject() -> Dict[str, Any]:
    """Read a pyproject.toml from a client project root.

    :raises OSError: no pyproject.toml
    :return: the parsed pyproject.toml
    """
    pyproject_path = "pyproject.toml"
    if not os.path.isfile(pyproject_path):
        raise OSError(f"{pyproject_path} not found")
    with open(pyproject_path, "rb") as pyproject_file:
        return tomli.load(pyproject_file)


def get_download_config(pyproject: Dict[str, Any]) -> Dict[str, List[Distro]]:
    """Create a table of distros from the defined distribution options.

    :param pyproject: the parsed pyproject.toml
    :return: a table of distros
    """
    try:
        binaries = pyproject["tool"]["pre-commit-download"]["binaries"]
    except KeyError:
        return {}
    cfg = {}
    for name, distros in binaries.items():
        cfg[name] = [Distro(name=name, **distro) for distro in distros]
    return cfg


def get_install_root(pyproject: Dict[str, Any]) -> Union[str, None]:
    """Find an installation root in the pyproject.

    :param pyproject: the parsed pyproject.toml
    :raises ValueError: the installation root is not a directory
    :return: path or None (not defined)
    """
    try:
        path = pyproject["tool"]["pre-commit-download"]["install_root"]
    except KeyError:
        return None
    if not os.path.isdir(path):
        raise ValueError(f"not a directory: {path}")
    return path


def get_default_install_root(metadata_directory) -> str:
    """Try to calculate the default installation root.

    The default installation root is a top level directory of a client module.

    :param metadata_directory: the setuptools parsed metadata
    :raises OSError: an unexpected metadata/project structure
    :raises ValueError: multi-project source root
    :return: path
    """
    top_level_path = os.path.join(metadata_directory, "top_level.txt")
    if not os.path.isfile(top_level_path):
        raise OSError(f"file not found: {top_level_path}")
    with open(top_level_path) as top_level:
        top_levels = top_level.readlines()
    if len(top_levels) > 1:
        raise ValueError("multiple top levels are not allowed")
    module_name = top_levels[0].strip()
    paths = glob.glob(f"**/{module_name}", recursive=True)
    if not paths:
        raise OSError(f"unable to find '{module_name}' module")
    return paths[0]


def select_distro(distros: List[Distro]) -> Distro:
    """Select an appropriate distribution.

    :param distros: a list of defined distribution options
    :raises ValueError: no distribution options
    :raises OSError: no suitable distribution
    :return: the suitable distro
    """
    if not len(distros):
        raise ValueError("empty distro list")
    for distro in distros:
        if distro.is_suitable():
            return distro
    name = distros[0].name
    raise OSError(f"no '{name}' distribution for your platform")


def build_wheel(
    wheel_directory: str,
    config_settings: Optional[Mapping[str, Any]] = None,
    metadata_directory: Optional[str] = None,
) -> str:
    """Install required executables and build the wheel.

    :param wheel_directory: a build root
    :param config_settings: custom build options, defaults to None
    :param metadata_directory: the setuptools parsed metadata, defaults to None
    :return: the basename of the wheel
    """
    pyproject = read_pyproject()
    download_cfg = get_download_config(pyproject)
    install_root = get_install_root(pyproject)
    if not install_root:
        install_root = get_default_install_root(metadata_directory)
    for distros in download_cfg.values():
        distro = select_distro(distros)
        distro.install(install_root)
    return original_build_wheel(
        wheel_directory,
        config_settings,
        metadata_directory,
    )
