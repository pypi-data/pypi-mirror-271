import os
import platform
import subprocess
from typing import Optional

import hbox.config as config
from hbox.logger import get_logger
from hbox.utils import execute_command, resolve_path

log = get_logger(__name__)


def add_shim(name: str):
    shims_file_path = resolve_path(os.path.join(config.shims_path, name))
    if not os.path.exists(shims_file_path):
        os.makedirs(os.path.dirname(shims_file_path), exist_ok=True)
        with open(shims_file_path, 'w') as shim_file:
            shim_file.write('#!/bin/sh\n')
            shim_file.write('hbox run ' + name + ' "$@"\n')

        # Set the permissions of the new shim script to be executable (0o755 gives rwx for user and rx for group/others)
        os.chmod(shims_file_path, 0o755)


def remove_shim(name: str):
    shims_file_path = resolve_path(os.path.join(config.shims_path, name))
    if os.path.exists(shims_file_path):
        os.remove(shims_file_path)


def get_container_image_url(name: str, version: str, set_as_default: bool):
    cfg = config.load_config()
    versions_cfg = config.load_versions()
    found = False
    for current_package in versions_cfg.packages:
        if current_package.name == name:
            if version in current_package.versions:
                log.info(f"'{name}' version {version} already exists.")
                return None, versions_cfg
            else:
                current_package.versions.append(version)
                if set_as_default:
                    log.info(f"'{name}' version {version} set as default.")
                    current_package.current = version
                found = True
            break
    if not found:
        package = config.Package(name=name, versions=[version], current=version)
        versions_cfg.packages.append(package)

    if name in cfg.packages:
        image = cfg.packages[name].image
    else:
        image = name

    return f"{image}:{version}", versions_cfg


def add_package(name, version: Optional[str] = "latest", set_as_default: Optional[bool] = False):
    image_url, versions_cfg = get_container_image_url(name, version, set_as_default)
    if image_url:
        full_command = ["docker", "pull", image_url]
        exit_code = execute_command(full_command)
        if exit_code and exit_code != 0:
            log.error(f"Failed to add package '{name}' at version {version}.")
        else:
            config.save_versions(versions_cfg)
            log.info(f"Added '{name}' version {version}.")
            add_shim(name)


def remove_package(name: str, version: Optional[str] = None):
    versions_cfg = config.load_versions()
    for current_package in versions_cfg.packages:
        if current_package.name == name:
            if version:
                if version in current_package.versions:
                    # Check if version to be removed is the current one and if there are multiple versions
                    if version == current_package.current and len(current_package.versions) > 1:
                        log.error(
                            f"Cannot remove the current active version '{version}' of '{name}'.")
                        return
                    current_package.versions.remove(version)
                    log.info(f"Removed version '{version}' of '{name}'.")
                else:
                    log.error(f"Version '{version}' of '{name}' does not exist.")

            if not version or not current_package.versions:
                versions_cfg.packages.remove(current_package)
                remove_shim(name)
                log.info(f"Removed package '{name}'.")
            break
    else:
        log.error(f"Package '{name}' does not exist.")

    config.save_versions(versions_cfg)


def run_package(name: str, command: list):
    cfg = config.load_config()
    versions_cfg = config.load_versions()

    image = name
    version = "latest"

    volumes_command = []
    if name in cfg.packages:
        package = cfg.packages[name]
        image = package.image
        for volume in package.volumes:
            source = resolve_path(volume.source)
            target = volume.target
            if os.path.exists(source):
                log.debug(f"Mounting volume {source} to {target}")
                volumes_command.extend(["-v", f"{source}:{target}"])
            else:
                log.debug(f"Volume {source} not found. Skipping.")
    else:
        log.debug(f"No configuration found for package '{name}'. Using {name} as the image name.")

    for current_package in versions_cfg.packages:
        if current_package.name == name:
            version = current_package.current

    full_image_url = f"{image}:{version}"

    full_command = ["docker", "run", "--rm", full_image_url] + volumes_command + command
    try:
        execute_command(full_command, can_be_interactive=True)
    except subprocess.CalledProcessError as e:
        log.debug(f"Failed to run command {' '.join(full_command)}")


def set_package_version(name: str, version: str):
    versions_cfg = config.load_versions()
    for current_package in versions_cfg.packages:
        if current_package.name == name:
            if version in current_package.versions:
                current_package.current = version
                config.save_versions(versions_cfg)
                log.info(f"'{name}' set to version {version}")
            else:
                log.error(f"'{name}' version {version} not found. Add the version first via 'add' command.")


def show_info():
    log.info("OS:")
    os_info = ' '.join(platform.uname())
    log.info(os_info)

    log.info("\nHBOX VERSION:")
    log.info(config.get_library_version())

    log.info("\nHBOX ENVIRONMENT VARIABLES:")
    log.info(f"HBOX_DIR={config.base_dir}")


def show_version():
    log.info(config.get_library_version())


def print_package(package):
    log.info(f"- {package.name}:")
    sorted_versions = sorted(package.versions)
    for version in sorted_versions:
        msg = f"  - {version}"
        if version == package.current:
            msg += " ✔"
        log.info(msg)


def list_packages(name: Optional[str] = None):
    versions_cfg = config.load_versions()
    if name:
        found = False
        for package in versions_cfg.packages:
            if package.name == name:
                print_package(package)
                found = True
                break
        if not found:
            log.error(f"Package '{name}' was not found. Add the package first via 'add' command.")
    else:
        for package in sorted(versions_cfg.packages, key=lambda pkg: pkg.name):
            print_package(package)
