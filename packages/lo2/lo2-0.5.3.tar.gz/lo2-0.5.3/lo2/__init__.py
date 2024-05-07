"""
lo2
======
Sub-packages
------------
-   html: To generate log viewer with HTML.
-   json: To generate log viewer with JSON.
-   print: To generate log viewer with Python.
-   parser: To executing lo2-IR to analysis log.
-   utils: Concat logs to a file.
"""
from .src import (
    parser,
    html,
    json,
    print,
    utils
)

from .plugins import (
    plugins,
)

__author__ = "DUHP BSP Team"
__copyright__ = "Copyright 2023 Xiaodu Inc. All Rights Reserved."
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Zhang Te, Li ermeng"
__email__ = "zhangte01, liermeng (at) baidu.com"
__status__ = "Experiment"
__doc__ = "Parser for log2 lang."

__all__ = ["parser", "html", "json", "print", "utils", "plugins"]