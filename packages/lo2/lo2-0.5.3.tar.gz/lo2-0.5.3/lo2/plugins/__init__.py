"""
lo2
====
__init__.py
"""
import copy
from .plot import (
    heatmap,
    linear,
)

plugins = {
    "@plot": {
        "linear":  linear.linear_entry_point,
        "scatter": linear.scatter_entry_point,
        "heatmap": heatmap.entry_point
    },
}

def dispatch(plugins_requirements, states, variables, *args, **kwargs):
    """ only support variable  """
    for namespace, pl in plugins_requirements.items():
        #if ptype in plugins:
        for ptype, pconfigs in pl.items():
            if ptype in plugins:
                for pconfig in pconfigs:
                    pname, params = list(pconfig.items())[0]
                    if pname in plugins[ptype]:
                        # 过滤出和当前插件相关的变量
                        arg_vars = copy.deepcopy(variables) 
                        for k in variables:
                            if namespace not in k:
                                del arg_vars[k] # 删除无关变量
                        stat = [ s for s in states if s['rname'] == namespace]
                        # 调用插件
                        plugins[ptype][pname](states=stat, vars=arg_vars, params=params, *args, **kwargs)
                    else:
                        print(f"Warning: not found this plugin: {namespace}:{ptype}:{pconfig}")
            else:
                print(f"Warning: not found this plugin type: {namespace}:{ptype}")
                

    #for k, v in variables.items():
    #    split_name = k.split(".")
    #    namespace, names = '.'.join(split_name[:-1]), split_name[-1]

    #    if namespace in plugins_requirements:
    #        print(namespace)



__all__ = ["plugins", "dispatch"]