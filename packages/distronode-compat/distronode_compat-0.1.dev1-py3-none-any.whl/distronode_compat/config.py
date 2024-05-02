"""Store configuration options as a singleton."""
from __future__ import annotations

import ast
import copy
import os
import re
import subprocess
from collections import UserDict
from typing import Literal

from packaging.version import Version

from distronode_compat.constants import DISTRONODE_MIN_VERSION
from distronode_compat.errors import InvalidPrerequisiteError, MissingDistronodeError
from distronode_compat.ports import cache


# do not use lru_cache here, as environment can change between calls
def distronode_collections_path() -> str:
    """Return collection path variable for current version of Distronode."""
    for env_var in [
        "DISTRONODE_COLLECTIONS_PATH",
        "DISTRONODE_COLLECTIONS_PATHS",
    ]:
        if env_var in os.environ:
            return env_var
    return "DISTRONODE_COLLECTIONS_PATH"


def parse_distronode_version(stdout: str) -> Version:
    """Parse output of 'distronode --version'."""
    # Distronode can produce extra output before displaying version in debug mode.

    # distronode-core 2.11+: 'distronode [core 2.11.3]'
    match = re.search(
        r"^distronode \[(?:core|base) (?P<version>[^\]]+)\]",
        stdout,
        re.MULTILINE,
    )
    if match:
        return Version(match.group("version"))
    msg = f"Unable to parse distronode cli version: {stdout}\nKeep in mind that only {DISTRONODE_MIN_VERSION } or newer are supported."
    raise InvalidPrerequisiteError(msg)


@cache
def distronode_version(version: str = "") -> Version:
    """Return current Version object for Distronode.

    If version is not mentioned, it returns current version as detected.
    When version argument is mentioned, it return converts the version string
    to Version object in order to make it usable in comparisons.
    """
    if version:
        return Version(version)

    proc = subprocess.run(
        ["distronode", "--version"],  # noqa: S603
        text=True,
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise MissingDistronodeError(proc=proc)

    return parse_distronode_version(proc.stdout)


class DistronodeConfig(UserDict[str, object]):  # pylint: disable=too-many-ancestors
    """Interface to query Distronode configuration.

    This should allow user to access everything provided by `distronode-config dump` without having to parse the data himself.
    """

    _aliases = {
        "COLLECTIONS_PATH": "COLLECTIONS_PATHS",  # 2.9 -> 2.10
    }
    # Expose some attributes to enable auto-complete in editors, based on
    # https://docs.distronode.com/distronode/latest/reference_appendices/config.html
    action_warnings: bool = True
    agnostic_become_prompt: bool = True
    allow_world_readable_tmpfiles: bool = False
    distronode_connection_path: str | None = None
    distronode_cow_acceptlist: list[str]
    distronode_cow_path: str | None = None
    distronode_cow_selection: str = "default"
    distronode_force_color: bool = False
    distronode_nocolor: bool = False
    distronode_nocows: bool = False
    distronode_pipelining: bool = False
    any_errors_fatal: bool = False
    become_allow_same_user: bool = False
    become_plugin_path: list[str] = [
        "~/.distronode/plugins/become",
        "/usr/share/distronode/plugins/become",
    ]
    cache_plugin: str = "memory"
    cache_plugin_connection: str | None = None
    cache_plugin_prefix: str = "distronode_facts"
    cache_plugin_timeout: int = 86400
    callable_accept_list: list[str] = []
    callbacks_enabled: list[str] = []
    collections_on_distronode_version_mismatch: Literal["warning", "ignore"] = "warning"
    collections_paths: list[str] = [
        "~/.distronode/collections",
        "/usr/share/distronode/collections",
    ]
    collections_scan_sys_path: bool = True
    color_changed: str = "yellow"
    color_console_prompt: str = "white"
    color_debug: str = "dark gray"
    color_deprecate: str = "purple"
    color_diff_add: str = "green"
    color_diff_lines: str = "cyan"
    color_diff_remove: str = "red"
    color_error: str = "red"
    color_highlight: str = "white"
    color_ok: str = "green"
    color_skip: str = "cyan"
    color_unreachable: str = "bright red"
    color_verbose: str = "blue"
    color_warn: str = "bright purple"
    command_warnings: bool = False
    conditional_bare_vars: bool = False
    connection_facts_modules: dict[str, str]
    controller_python_warning: bool = True
    coverage_remote_output: str | None
    coverage_remote_paths: list[str]
    default_action_plugin_path: list[str] = [
        "~/.distronode/plugins/action",
        "/usr/share/distronode/plugins/action",
    ]
    default_allow_unsafe_lookups: bool = False
    default_ask_pass: bool = False
    default_ask_vault_pass: bool = False
    default_become: bool = False
    default_become_ask_pass: bool = False
    default_become_exe: str | None = None
    default_become_flags: str
    default_become_method: str = "sudo"
    default_become_user: str = "root"
    default_cache_plugin_path: list[str] = [
        "~/.distronode/plugins/cache",
        "/usr/share/distronode/plugins/cache",
    ]
    default_callback_plugin_path: list[str] = [
        "~/.distronode/plugins/callback",
        "/usr/share/distronode/plugins/callback",
    ]
    default_cliconf_plugin_path: list[str] = [
        "~/.distronode/plugins/cliconf",
        "/usr/share/distronode/plugins/cliconf",
    ]
    default_connection_plugin_path: list[str] = [
        "~/.distronode/plugins/connection",
        "/usr/share/distronode/plugins/connection",
    ]
    default_debug: bool = False
    default_executable: str = "/bin/sh"
    default_fact_path: str | None = None
    default_filter_plugin_path: list[str] = [
        "~/.distronode/plugins/filter",
        "/usr/share/distronode/plugins/filter",
    ]
    default_force_handlers: bool = False
    default_forks: int = 5
    default_gathering: Literal["smart", "explicit", "implicit"] = "smart"
    default_gather_subset: list[str] = ["all"]
    default_gather_timeout: int = 10
    default_handler_includes_static: bool = False
    default_hash_behaviour: str = "replace"
    default_host_list: list[str] = ["/etc/distronode/hosts"]
    default_httpapi_plugin_path: list[str] = [
        "~/.distronode/plugins/httpapi",
        "/usr/share/distronode/plugins/httpapi",
    ]
    default_internal_poll_interval: float = 0.001
    default_inventory_plugin_path: list[str] = [
        "~/.distronode/plugins/inventory",
        "/usr/share/distronode/plugins/inventory",
    ]
    default_jinja2_extensions: list[str] = []
    default_jinja2_native: bool = False
    default_keep_remote_files: bool = False
    default_libvirt_lxc_noseclabel: bool = False
    default_load_callback_plugins: bool = False
    default_local_tmp: str = "~/.distronode/tmp"
    default_log_filter: list[str] = []
    default_log_path: str | None = None
    default_lookup_lugin_path: list[str] = [
        "~/.distronode/plugins/lookup",
        "/usr/share/distronode/plugins/lookup",
    ]
    default_managed_str: str = "Distronode managed"
    default_module_args: str
    default_module_compression: str = "ZIP_DEFLATED"
    default_module_name: str = "command"
    default_module_path: list[str] = [
        "~/.distronode/plugins/modules",
        "/usr/share/distronode/plugins/modules",
    ]
    default_module_utils_path: list[str] = [
        "~/.distronode/plugins/module_utils",
        "/usr/share/distronode/plugins/module_utils",
    ]
    default_netconf_plugin_path: list[str] = [
        "~/.distronode/plugins/netconf",
        "/usr/share/distronode/plugins/netconf",
    ]
    default_no_log: bool = False
    default_no_target_syslog: bool = False
    default_null_representation: str | None = None
    default_poll_interval: int = 15
    default_private_key_file: str | None = None
    default_private_role_vars: bool = False
    default_remote_port: str | None = None
    default_remote_user: str | None = None
    default_roles_path: list[str] = [
        "~/.distronode/roles",
        "/usr/share/distronode/roles",
        "/etc/distronode/roles",
    ]
    default_selinux_special_fs: list[str] = [
        "fuse",
        "nfs",
        "vboxsf",
        "ramfs",
        "9p",
        "vfat",
    ]
    default_stdout_callback: str = "default"
    default_strategy: str = "linear"
    default_strategy_plugin_path: list[str] = [
        "~/.distronode/plugins/strategy",
        "/usr/share/distronode/plugins/strategy",
    ]
    default_su: bool = False
    default_syslog_facility: str = "LOG_USER"
    default_task_includes_static: bool = False
    default_terminal_plugin_path: list[str] = [
        "~/.distronode/plugins/terminal",
        "/usr/share/distronode/plugins/terminal",
    ]
    default_test_plugin_path: list[str] = [
        "~/.distronode/plugins/test",
        "/usr/share/distronode/plugins/test",
    ]
    default_timeout: int = 10
    default_transport: str = "smart"
    default_undefined_var_behavior: bool = True
    default_vars_plugin_path: list[str] = [
        "~/.distronode/plugins/vars",
        "/usr/share/distronode/plugins/vars",
    ]
    default_vault_encrypt_identity: str | None = None
    default_vault_identity: str = "default"
    default_vault_identity_list: list[str] = []
    default_vault_id_match: bool = False
    default_vault_password_file: str | None = None
    default_verbosity: int = 0
    deprecation_warnings: bool = False
    devel_warning: bool = True
    diff_always: bool = False
    diff_context: int = 3
    display_args_to_stdout: bool = False
    display_skipped_hosts: bool = True
    docsite_root_url: str = "https://docs.distronode.com/distronode/"
    doc_fragment_plugin_path: list[str] = [
        "~/.distronode/plugins/doc_fragments",
        "/usr/share/distronode/plugins/doc_fragments",
    ]
    duplicate_yaml_dict_key: Literal["warn", "error", "ignore"] = "warn"
    enable_task_debugger: bool = False
    error_on_missing_handler: bool = True
    facts_modules: list[str] = ["smart"]
    galaxy_cache_dir: str = "~/.distronode/galaxy_cache"
    galaxy_display_progress: str | None = None
    galaxy_ignore_certs: bool = False
    galaxy_role_skeleton: str | None = None
    galaxy_role_skeleton_ignore: list[str] = ["^.git$", "^.*/.git_keep$"]
    galaxy_server: str = "https://galaxy.distronode.com"
    galaxy_server_list: str | None = None
    galaxy_token_path: str = "~/.distronode/galaxy_token"
    host_key_checking: bool = True
    host_pattern_mismatch: Literal["warning", "error", "ignore"] = "warning"
    inject_facts_as_vars: bool = True
    interpreter_python: str = "auto_legacy"
    interpreter_python_distro_map: dict[str, str]
    interpreter_python_fallback: list[str]
    invalid_task_attribute_failed: bool = True
    inventory_any_unparsed_is_failed: bool = False
    inventory_cache_enabled: bool = False
    inventory_cache_plugin: str | None = None
    inventory_cache_plugin_connection: str | None = None
    inventory_cache_plugin_prefix: str = "distronode_facts"
    inventory_cache_timeout: int = 3600
    inventory_enabled: list[str] = [
        "host_list",
        "script",
        "auto",
        "yaml",
        "ini",
        "toml",
    ]
    inventory_export: bool = False
    inventory_ignore_exts: str
    inventory_ignore_patterns: list[str] = []
    inventory_unparsed_is_failed: bool = False
    localhost_warning: bool = True
    max_file_size_for_diff: int = 104448
    module_ignore_exts: str
    netconf_ssh_config: str | None = None
    network_group_modules: list[str] = [
        "eos",
        "nxos",
        "ios",
        "iosxr",
        "junos",
        "enos",
        "ce",
        "vyos",
        "sros",
        "dellos9",
        "dellos10",
        "dellos6",
        "asa",
        "aruba",
        "aireos",
        "bigip",
        "ironware",
        "onyx",
        "netconf",
        "exos",
        "voss",
        "slxos",
    ]
    old_plugin_cache_clearing: bool = False
    paramiko_host_key_auto_add: bool = False
    paramiko_look_for_keys: bool = True
    persistent_command_timeout: int = 30
    persistent_connect_retry_timeout: int = 15
    persistent_connect_timeout: int = 30
    persistent_control_path_dir: str = "~/.distronode/pc"
    playbook_dir: str | None
    playbook_vars_root: Literal["top", "bottom", "all"] = "top"
    plugin_filters_cfg: str | None = None
    python_module_rlimit_nofile: int = 0
    retry_files_enabled: bool = False
    retry_files_save_path: str | None = None
    run_vars_plugins: str = "demand"
    show_custom_stats: bool = False
    string_conversion_action: Literal["warn", "error", "ignore"] = "warn"
    string_type_filters: list[str] = [
        "string",
        "to_json",
        "to_nice_json",
        "to_yaml",
        "to_nice_yaml",
        "ppretty",
        "json",
    ]
    system_warnings: bool = True
    tags_run: list[str] = []
    tags_skip: list[str] = []
    task_debugger_ignore_errors: bool = True
    task_timeout: int = 0
    transform_invalid_group_chars: Literal[
        "always",
        "never",
        "ignore",
        "silently",
    ] = "never"
    use_persistent_connections: bool = False
    variable_plugins_enabled: list[str] = ["host_group_vars"]
    variable_precedence: list[str] = [
        "all_inventory",
        "groups_inventory",
        "all_plugins_inventory",
        "all_plugins_play",
        "groups_plugins_inventory",
        "groups_plugins_play",
    ]
    verbose_to_stderr: bool = False
    win_async_startup_timeout: int = 5
    worker_shutdown_poll_count: int = 0
    worker_shutdown_poll_delay: float = 0.1
    yaml_filename_extensions: list[str] = [".yml", ".yaml", ".json"]

    def __init__(
        self,
        config_dump: str | None = None,
        data: dict[str, object] | None = None,
    ) -> None:
        """Load config dictionary."""
        super().__init__()

        if data:
            self.data = copy.deepcopy(data)
            return

        if not config_dump:
            env = os.environ.copy()
            # Avoid possible ANSI garbage
            env["DISTRONODE_FORCE_COLOR"] = "0"
            config_dump = subprocess.check_output(
                ["distronode-config", "dump"],  # noqa: S603
                universal_newlines=True,
                env=env,
            )

        for match in re.finditer(
            r"^(?P<key>[A-Za-z0-9_]+).* = (?P<value>.*)$",
            config_dump,
            re.MULTILINE,
        ):
            key = match.groupdict()["key"]
            value = match.groupdict()["value"]
            try:
                self[key] = ast.literal_eval(value)
            except (NameError, SyntaxError, ValueError):
                self[key] = value

    def __getattribute__(self, attr_name: str) -> object:
        """Allow access of config options as attributes."""
        _dict = super().__dict__  # pylint: disable=no-member
        if attr_name in _dict:
            return _dict[attr_name]

        data = super().__getattribute__("data")
        if attr_name == "data":  # pragma: no cover
            return data

        name = attr_name.upper()
        if name in data:
            return data[name]
        if name in DistronodeConfig._aliases:
            return data[DistronodeConfig._aliases[name]]

        return super().__getattribute__(attr_name)

    def __getitem__(self, name: str) -> object:
        """Allow access to config options using indexing."""
        return super().__getitem__(name.upper())

    def __copy__(self) -> DistronodeConfig:
        """Allow users to run copy on Config."""
        return DistronodeConfig(data=self.data)

    def __deepcopy__(self, memo: object) -> DistronodeConfig:
        """Allow users to run deeepcopy on Config."""
        return DistronodeConfig(data=self.data)


__all__ = [
    "distronode_collections_path",
    "parse_distronode_version",
    "distronode_version",
    "DistronodeConfig",
]
