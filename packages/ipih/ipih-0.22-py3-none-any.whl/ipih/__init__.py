import sys
import os
import importlib.util
import platform


NAME: str = "ipih"
VERSION: str = "0.22"

ROOT_MODULE_NAME: str = "pih"
FACADE_FOLDER_NAME: str = "facade"
BUILD_FOLDER_NAME: str = ".build"
BUILD_FILES_FOLDER_NAME: str = ".files"
WINDOWS_SHARE_DOMAIN_NAME: str = ROOT_MODULE_NAME
WINDOWS_SHARE_DOMAIN_ALIAS: str = "fmv"

SERVICE_ADMIN_HOST_NAME: str = "fmvdc1"
SERVICE_ADMIN_GRPC_PORT: int = 20


def get_path(is_linux: bool = False) -> str:
    if is_linux:
        return f"//mnt/{FACADE_FOLDER_NAME}"
    return f"//{WINDOWS_SHARE_DOMAIN_ALIAS}/{FACADE_FOLDER_NAME}"


def get_build_path() -> str:
    return f"//{WINDOWS_SHARE_DOMAIN_NAME}/{FACADE_FOLDER_NAME}/{BUILD_FOLDER_NAME}"


def import_pih() -> None:
    is_build: bool = (
        len(
            list(
                filter(
                    lambda item: item.find(f"{os.sep}{BUILD_FOLDER_NAME}{os.sep}")
                    != -1,
                    __path__,
                )
            )
        )
        > 0
    )
    if is_build:
        sys.path.append(get_path())
    else:
        module_is_exists = importlib.util.find_spec(ROOT_MODULE_NAME) is not None
        if not module_is_exists:
            sys.path.append(get_path(platform.system() == "Linux"))


import_pih()
