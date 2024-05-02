"""
This processes the directory main/unc/materials/shared/actions_registry and emits actions_registry/action_definitions.tsx
"""

import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import TypeVar

from main.base.types import actions_registry_t
from pkgs.type_spec import builder

from ...argument_parser import CachedParser
from ..emit_typescript_util import ts_name
from ..util import rewrite_file
from .emit_typescript import emit_action_definitions

key_name = "name"
key_icon = "icon"
key_short_description = "short_description"
key_description = "description"


TypeT = TypeVar("TypeT")


class InvalidSpecException(Exception):
    pass


@dataclass(kw_only=True)
class ActionRegistryFileInfo:
    directories: list[str]
    filename: str
    filepath: str


ACTIONS_REGISTRY_ROOT = "main/unc/materials/shared/actions_registry/"
action_definition_parser = CachedParser(
    dict[str, actions_registry_t.ActionDefinitionYaml]
)


def get_action_registry_files_info() -> list[ActionRegistryFileInfo]:
    files_info = []
    for dirname, _, files in os.walk(ACTIONS_REGISTRY_ROOT):
        directories = dirname.replace(ACTIONS_REGISTRY_ROOT, "").split("/")
        for filename in files:
            filepath = os.path.join(dirname, filename)
            if os.path.isfile(filepath) and filepath.endswith(".yaml"):
                files_info.append(
                    ActionRegistryFileInfo(
                        directories=directories,
                        filename=filename.replace(".yaml", ""),
                        filepath=filepath,
                    )
                )
    return files_info


def main() -> None:
    files_info = get_action_registry_files_info()
    action_definitions: defaultdict[str, list[actions_registry_t.ActionDefinition]] = (
        defaultdict(list)
    )
    all_action_definitions: list[actions_registry_t.ActionDefinition] = []

    for file_info in files_info:
        in_action_definitions = action_definition_parser.parse_yaml_file(
            file_info.filepath
        )
        if len(in_action_definitions) == 0:
            continue
        for ref_name, definition in in_action_definitions.items():
            modules = [*file_info.directories]
            # if the actions are stored in index.yaml, parent dir should be treated as module
            if file_info.filename != "index":
                modules.append(file_info.filename)

            module_str = "_".join(modules)
            all_action_definitions.append(
                actions_registry_t.ActionDefinition(
                    name=definition.name,
                    short_description=definition.short_description,
                    description=definition.description,
                    icon=definition.icon,
                    ref_name=ref_name,
                    module=actions_registry_t.ActionsRegistryModule(
                        ts_name(module_str, name_case=builder.NameCase.convert)
                    ),
                    visibility_scope=[
                        actions_registry_t.ActionDefinitionVisibilityScope(item)
                        for item in definition.visibility_scope
                    ]
                    if definition.visibility_scope is not None
                    else None,
                )
            )
    all_action_definitions = sorted(
        all_action_definitions, key=lambda item: (item.module, item.ref_name)
    )
    for action_definition in all_action_definitions:
        action_definitions[action_definition.module].append(action_definition)
    ts_content = emit_action_definitions(action_definitions)
    rewrite_file(
        "main/site/js/materials/base/actions_registry/action_definitions.tsx",
        ts_content,
    )

    sys.exit(0)


main()
