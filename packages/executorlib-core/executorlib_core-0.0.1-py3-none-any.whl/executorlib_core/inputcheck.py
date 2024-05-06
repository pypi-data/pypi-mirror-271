import inspect


def check_resource_dict(function):
    if "resource_dict" in inspect.signature(function).parameters.keys():
        raise ValueError(
            "The parameter resource_dict is used internally in pympipool, "
            "so it cannot be used as parameter in the submitted functions."
        )


def check_resource_dict_is_empty(resource_dict):
    if len(resource_dict) > 0:
        raise ValueError(
            "When block_allocation is enabled, the resource requirements have to be defined on the executor level."
        )
