"""DearPyGui item error utilities."""
import inspect
import functools
from dearpygui import _dearpygui
from ._typing import Item, ItemCommand, Protocol, ParamSpec
from . import _parsing


_P = ParamSpec("_P")


class ItemError(Protocol[_P]):
    def __call__(self, item: Item, command: ItemCommand[_P, Item]) -> Exception | None: ...


# [ HELPER FUNCTIONS ]

def is_tag_valid(tag: Item) -> bool:
    return isinstance(tag, (int, str))


def is_item_interface(item: Item) -> bool:
    if type(item) in (str, int):
        return False
    elif is_tag_valid(item):
        return True
    return False


def does_item_exist(tag: Item) -> bool:
    if isinstance(tag, str):
        tag = _dearpygui.get_alias_id(tag)
    return tag in _dearpygui.get_all_items()


def command_signature(command: ItemCommand):
    variadics = (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
    signature = inspect.signature(command)
    return signature.replace(
        parameters=tuple(
            p for p in signature.parameters.values()
            if p.kind not in variadics
        )
    )


def command_itp_name(command: ItemCommand) -> str:
    from . import api

    for tp_def in _parsing.item_definitions().values():
        try:
            if command == tp_def.command1 or command == tp_def.command2:  # type: ignore
                return tp_def.name  # type: ignore
        except AttributeError:
            pass
    return '<unknown type>'




# [ ERROR FUNCTIONS ]

def err_tag_invalid(item: Item, command: ItemCommand, *args, **kwargs):
    if not is_tag_valid(item):
        return TypeError(f'`tag` expected as int or str, got {type(item)!r}.')


def err_item_nonexistant(item: Item, command: ItemCommand, *args, **kwargs):
    exists = does_item_exist(item)
    if exists:
        return

    invalid_id = err_tag_invalid(item, command, *args, **kwargs)
    if invalid_id:
        return invalid_id

    if isinstance(item, int):
        item = int(item)
        id_type = ' uuid'
    else:
        item = str(item)
        id_type = 'n alias'

    return ValueError(
        f"{item!r} is not currently in-use as a{id_type} for any "
        "existing item - perhaps the item using it was deleted?"
    )


def err_arg_unexpected(item: Item, command: ItemCommand, *args, **kwargs):
    signature = command_signature(command)
    # Python will automatically throw a TypeError for unexpected
    # positional args since `dearpygui.dearpygui` is valid code.
    # All item commands accept variadic keywords though, and
    # `mvPythonParser` will throw vague errors for them.
    bad_kwds = ', '.join(repr(k) for k in kwargs if k not in signature.parameters)
    if not bad_kwds:
        return
    if not is_tag_valid(item):
        return err_tag_invalid(item, command, *args, **kwargs)
    elif is_item_interface(item):
        callee = f'{type(item).__qualname__}()'
    else:
        callee = f'{command.__qualname__}()'  # type: ignore

    return TypeError(f'{callee!r} received unexpected keyword argument(s) {bad_kwds}.')


def err_arg_invalid(item: Item, command: ItemCommand, *args, **kwargs):
    # TODO
    ...





def _invld_p_err(parent_tp: str, parent: int | str, child_tp: str, *tp_list: str) -> ValueError:
    msg = f"incompatible parent {parent_tp}(tag={parent!r}) for child {child_tp!r} item{{}}"
    if tp_list:
        if isinstance(tp_list, str):
            tp_list = ''.join(tp_list),
        msg = msg.format(f", try {', '.join(repr(s) for s in tp_list)}.")
    return ValueError(msg)

def err_parent_invalid(item: Item, command: ItemCommand, *args, **kwargs):
    if "parent" not in command_signature(command).parameters:
        return

    cstack = _dearpygui.top_container_stack()
    parent = kwargs.get("parent", 0)

    # CASE 1: `parent` is not `int` nor `str` (also prevents error in CASE 2)
    if not is_tag_valid(parent):
        return ValueError(f"`parent` expected as int or str, got {type(parent)!r}")

    if parent:
        # CASE 2: the included parent does not exist
        if not does_item_exist(parent):
            return ValueError(f"`parent` item {parent!r} does not exist.")
        # CASE 3: is it even a container?
        if _dearpygui.get_item_info(parent)['container'] is False:
            return ValueError(f"`parent` item {parent!r} is not a container and cannot parent items")

    # CASE 4: did not include parent while the container stack is empty
    elif not parent and not cstack:
        return TypeError("no parent item available (container stack is empty).")


    parent = parent or cstack

    # CASE 5: a parent is available but maybe incompatible
    p_tp_name = _dearpygui.get_item_info(
        parent
    )["type"].removeprefix("mvAppItemType::")
    c_tp_name = command_itp_name(command).removeprefix('mvAppItemType::')

    err = functools.partial(_invld_p_err, p_tp_name, parent, c_tp_name)

    # these are supposed to be "universal" parents, but there are some exceptions
    if p_tp_name in ("mvStage", "mvTemplateRegistry"):
        return err()

    if c_tp_name.startswith("mvDraw") and "Drawlist" not in c_tp_name and p_tp_name not in ('mvDrawlist', 'mvViewportDrawlist', 'mvDrawLayer'):
        return err('mvDrawlist', 'mvViewportDrawlist', 'mvDrawLayer')
    if c_tp_name.startswith("mvThemeComponent") and p_tp_name not in ("mvTheme",):
        return err('mvTheme',)
    if c_tp_name in ("mvThemeColor", 'mvThemeStyle') and p_tp_name not in ("mvThemeComponent",):
        return err("mvThemeComponent",)
    if "Handler" in c_tp_name:
        if p_tp_name == "mvHandlerRegistry":
            return err("mvItemHandlerRegistry",)
        if p_tp_name == "mvItemHandlerRegistry":
            return err("mvItemHandlerRegistry",)
    if c_tp_name.endswith("Series") and p_tp_name != 'mvPlotAxis':
        return err('mvPlotAxis',)
    if c_tp_name in ('mvAnnotation', 'mvPlotLegend', 'mvPlotAxis') and p_tp_name != "mvPlot":
        return err("mvPlot",)
    if c_tp_name.startswith('mvNode'):
        if c_tp_name == 'mvNodeAttribute' and p_tp_name != 'mvNode':
            return err('mvNode',)
        if c_tp_name == 'mvNode' and p_tp_name != 'mvNodeEditor':
            return err('mvNodeEditor',)
    if c_tp_name in ('mvTableRow', 'mvTableCell') and p_tp_name != 'mvTable':
        return err('mvTable',)
    if c_tp_name == 'mvTableCell' and p_tp_name != 'mvTableRow':
        return err('mvTableRow',)


