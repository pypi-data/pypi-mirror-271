import io
from collections import defaultdict

from main.base.types import actions_registry_t

from ...type_spec import builder
from ..emit_typescript_util import INDENT, MODIFY_NOTICE, ts_name
from ..util import encode_common_string


def _action_symbol_name(action_definition: actions_registry_t.ActionDefinition) -> str:
    return f"{ts_name(action_definition.ref_name, name_case=builder.NameCase.convert)}"


def _action_module_name_base(module: str) -> str:
    return f"{ts_name(module, name_case=builder.NameCase.convert)}"


def _action_module_name_obj(module: str) -> str:
    return f"{_action_module_name_base(module)}Actions"


def _action_module_name(module: str) -> str:
    return f"ActionsRegistryT.ActionsRegistryModule.{_action_module_name_base(module)}"


def emit_action_definitions(
    action_definitions: defaultdict[str, list[actions_registry_t.ActionDefinition]],
) -> str:
    out = io.StringIO()
    out.write(MODIFY_NOTICE)
    out.write("\n")
    out.write('import { ActionsRegistryT } from "unc_mat/types"\n\n')
    out.write(MODIFY_NOTICE)
    modules = []
    for key, values in action_definitions.items():
        out.write(MODIFY_NOTICE)
        modules.append(key)
        out.write(f"export const {_action_module_name_obj(key)} = {{\n")
        for action_definition in values:
            out.write(MODIFY_NOTICE)
            out.write(_emit_action_definition(action_definition, INDENT))
        out.write("}\n")

    out.write(MODIFY_NOTICE)
    out.write("\n")
    out.write("export const actionDefinitions = {\n")
    for module in modules:
        out.write(
            f"{INDENT}[{_action_module_name(module)}]: {_action_module_name_obj(module)},\n"
        )

    out.write("}\n")
    out.write(_emit_action_definition_types(modules, indent=""))
    out.write(MODIFY_NOTICE)
    out.write("\n")

    return out.getvalue()


def _emit_action_definition(
    action_definition: actions_registry_t.ActionDefinition, indent: str
) -> str:
    out = io.StringIO()

    sub_indent = indent + INDENT
    out.write(f"{indent}{_action_symbol_name(action_definition)}: {{\n")
    out.write(f"{sub_indent}name: {encode_common_string(action_definition.name)},\n")
    if action_definition.icon is not None:
        out.write(f"{sub_indent}icon: {encode_common_string(action_definition.icon)},\n")
    out.write(
        f"{sub_indent}shortDescription: {encode_common_string(action_definition.short_description)},\n"
    )
    out.write(
        f"{sub_indent}description: {encode_common_string(action_definition.description)},\n"
    )
    out.write(
        f"{sub_indent}refName: {encode_common_string(action_definition.ref_name)},\n"
    )
    out.write(f"{sub_indent}module: {_action_module_name(action_definition.module)},\n")
    if (
        action_definition.visibility_scope is not None
        and len(action_definition.visibility_scope) > 0
    ):
        out.write(
            f"{sub_indent}visibilityScope: {_emit_visibility_scope(action_definition.visibility_scope)},\n"
        )
    out.write(f"{indent}}},\n")
    return out.getvalue()


def _emit_action_definition_types(modules: list[str], indent: str) -> str:
    out = io.StringIO()

    sub_indent = indent + INDENT
    out.write(
        f"{indent}type RefNameKeys<M extends ActionsRegistryT.ActionsRegistryModule> = keyof (typeof actionDefinitions)[M]\n"
    )
    out.write(
        f"{indent}type ActionDefinitionIdentifierGetter<M extends ActionsRegistryT.ActionsRegistryModule> = {{ module: M; refName: RefNameKeys<M> }}\n"
    )
    out.write(f"{indent}export type ActionDefinitionIdentifier =\n")
    for module in modules:
        out.write(
            f"{sub_indent}| ActionDefinitionIdentifierGetter<{_action_module_name(module)}>\n"
        )
    out.write("\n")
    return out.getvalue()


def _emit_visibility_scope(
    visibility_scope: list[actions_registry_t.ActionDefinitionVisibilityScope],
) -> str:
    visibility_scope_types = ",".join([
        f"ActionsRegistryT.ActionDefinitionVisibilityScope.{ts_name(visibility_item, name_case=builder.NameCase.convert)}"
        for visibility_item in visibility_scope
        if visibility_item is not None
    ])

    return f"[ {visibility_scope_types} ]"
