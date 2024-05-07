"""
lo2
====
linear.py
"""
def group_var(operable_vars: dict):
    """ 将变量按照命名空间分组 """
    value_groups = {}
    def split_var_symbol(symbol):
        """ 拆分变量名为命名空间和名称 """
        split = symbol.split('.')
        name = split[-1]
        namespace = '.'.join(split[:-1])
        return namespace, name

    for k, v in operable_vars.items():
        if v["type"] == 'str' or not v["monitor"]:
            continue
        ns, na = split_var_symbol(k)
        val, time, label = v['value'], v['time'], k
        # matplot 显示中文需要特殊处理，doc可能会有中文，所以先不显示
        #if '@doc' in v:
        #    label += f": {v['@doc']}"
        if val[0] == "inf" or time[0] == "init value":
            val, time = val[1:], time[1:]

        val = list(map(float, val))
        if ns not in value_groups:
            value_groups[ns] = {na: [time, val]}
        else:
            value_groups[ns][na] = [time, val]

    return value_groups

def var_plot(operable_vars: dict, timeformat, scatter=False):
    """ 绘制变量 """
    values = group_var(operable_vars)

    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter
    from matplotlib.ticker import MaxNLocator
    import datetime

    #plt.figure(dpi=500)
    for group, contain in values.items():
        for var, val in contain.items():
            x_val = val[0]
            y_val = val[1]
            dates = [datetime.datetime.strptime(t, timeformat) for t in x_val]
            if scatter:
                plt.scatter(dates, y_val, label=var, s=5)
            else:
                plt.plot(dates, y_val, label=var)

        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=25, min_n_ticks=5))
        plt.gca().xaxis.set_major_formatter(DateFormatter(timeformat))
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.title(f'[lo2] {group}')
        plt.show()
def linear_entry_point(*args, **kwargs):
    """ 线性图入口 """
    vars = kwargs.get('vars', None)
    _ = kwargs.get('states', None)
    timeformat = kwargs.get('timeformat', None)
    var_plot(vars, timeformat)

def scatter_entry_point(*args, **kwargs):
    """ 散点图入口 """
    vars = kwargs.get('vars', None)
    _ = kwargs.get('states', None)
    timeformat = kwargs.get('timeformat', None)
    var_plot(vars, timeformat, scatter=True)