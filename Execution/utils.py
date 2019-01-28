from Execution.RuntimeWarnings import BaseWarn
from typing import Callable, Any, List


def apply_repeatedly(items: List, applying_items:List, func:Callable[[Any, Any], Any], warning:BaseWarn):
    res = []
    ln = len(items)
    _max = len(applying_items)
    for i in range(ln):
        r = func(items[i], applying_items[i % _max])
        res.append(r)
    if ln % _max != 0:
        warning.warn()
    return res
