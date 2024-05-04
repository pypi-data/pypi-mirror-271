
def _fill_namespace():
    from . import _interface, _parsing, _mkstub

    exported = _mkstub.Exported(__name__)

    namespace = dict(
        exp for exp in _mkstub.Exported.fetch(_interface).items()
    )
    for tp_def in _parsing.item_definitions().values():
        if not tp_def:
            continue

        itp = exported(_interface.create_itemtype(tp_def))
        itp.__module__ = __name__
        namespace[itp.__qualname__] = itp
        # set an alias
        if itp.__qualname__ == "mvWindowAppItem":
            namespace['mvWindow'] = namespace['Window'] = itp
            exported(itp, 'mvWindow')
            exported(itp, 'Window')
        elif itp.__qualname__  == 'mvAnnotation':
            namespace['PlotAnnotation'] = itp
            exported(itp, 'PlotAnnotation')
        else:
            alias = itp.__qualname__.removeprefix('mv')
            if alias[0].isdigit():
                alias = f'{alias[2:]}{alias[0]}{alias[1].upper()}'
            assert alias not in namespace
            namespace[alias] = itp
            exported(itp, alias)

    globals().update(namespace)


_fill_namespace()
