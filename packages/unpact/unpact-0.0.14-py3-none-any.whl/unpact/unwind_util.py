import itertools
from typing import Any, Dict, List, Optional, Sequence, Set, Union

from .tree import Tree, get_keys_nested_dict, load_tree_rep
from .types import ColumnDef, ColumnSpec

__all__ = ["unwind"]


def _unwind_list(data: List, tree: Tree, level_list: List) -> None:
    for item in data:
        item_output_dict = {}
        item_accum: List[dict] = []
        for child in tree.children:
            value: Union[dict, list] = _unwind(item, child)
            if isinstance(value, list):
                if item_accum and len(item_accum) == len(value):  # Handle adjacents
                    item_accum = [{**a, **b} for a, b in zip(item_accum, value)]
                else:
                    item_accum.extend(value)
            else:
                item_output_dict.update(value)
        if len(item_accum) > 0:
            level_list.extend([{**item_output_dict, **item} for item in item_accum])
        else:
            level_list.append(item_output_dict)


def _get_value(data: dict, tree: Tree) -> Any:
    tree_data = data.get(tree.path)
    if isinstance(data, list):
        return [_unwind(d, tree) for d in data]
    if isinstance(tree_data, list):
        return [tree.get_value(x, idx) for idx, x in enumerate(tree_data)]
    return tree.get_value(tree_data)


def _unwind(data: dict, tree: Tree) -> Union[List, List[Dict[str, Any]], Dict[str, Any], dict, List[dict]]:
    if not tree.children:
        return _get_value(data, tree)

    level_list: List[dict] = []
    level_dict: dict = {}

    tree_data = data.get(tree.path)
    tree_data = {} if tree_data is None else tree_data
    if isinstance(tree_data, list):
        _unwind_list(tree_data, tree, level_list)
    else:
        for child in tree.children:
            value = _unwind(tree_data, child)
            if isinstance(value, list):
                level_list.extend(value)
            else:
                level_dict.update(value)

    if len(level_list) == 0:
        return level_dict

    appended = [{**level_dict, **list_value} for list_value in level_list]
    return appended


def __remove_redundant_paths(keys: List[str]):
    # Sort the keys
    sorted_keys = sorted(keys)

    # List to hold the final set of keys
    final_keys = []

    # Iterate through the sorted list of keys
    for i in range(len(sorted_keys)):
        # Ensure this isn't the last element to avoid IndexError
        if i + 1 < len(sorted_keys):
            # Check if the next key starts with the current key followed by a dot (indicating a parent-child relationship)
            if not sorted_keys[i + 1].startswith(sorted_keys[i] + "."):
                final_keys.append(sorted_keys[i])
        else:
            # Always add the last key since it can't be a prefix of any key that follows
            final_keys.append(sorted_keys[i])

    return final_keys


def __get_keys_from_sample(sample: List[Dict[Any, Any]]) -> Set[str]:
    keys: Set[str] = set()
    for item in sample:
        keys.update(get_keys_nested_dict(item))
    return keys


def unwind(
    data: Union[Dict[Any, Any], List[Dict[Any, Any]]],
    columns: Sequence[ColumnDef],
    allow_extra: bool = False,
    infer_length: Optional[int] = 10,
) -> List[Dict[str, Any]]:
    column_defs = [ColumnSpec.from_def(c) for c in columns]

    if allow_extra:
        keys = get_keys_nested_dict(data) if isinstance(data, dict) else __get_keys_from_sample(data[:infer_length])
        specified_keys = [k[0] if isinstance(k, tuple) else k for k in columns]
        extra_paths = [k for k in keys if k not in specified_keys]
        extra_defs: List[ColumnSpec] = [ColumnSpec(path=k, name=k) for k in extra_paths]
        column_defs.extend(extra_defs)
        path_list = [c.path for c in column_defs]
        unique_paths = __remove_redundant_paths(path_list)

        column_defs = [c for c in column_defs if c.path in unique_paths]

    tree = load_tree_rep(column_defs)

    def apply_unwind(d: Dict, tree: Tree) -> List[Dict[str, Any]]:
        unwound = _unwind({"root": d}, tree)
        if not isinstance(unwound, list):
            return [unwound]
        return unwound

    if isinstance(data, dict):
        return apply_unwind(data, tree)
    else:
        return list(itertools.chain(*[apply_unwind(d, tree) for d in data]))
