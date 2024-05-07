"""
lo2
====
heatmap.py
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

        val, time, label, init_val = v['value'], v['time'], k, v['init_value']

        # matplot 显示中文需要特殊处理，doc可能会有中文，所以先不显示
        # if '@doc' in v:
        #     label += f": {v['@doc']}"
        if val[0] == "inf" or time[0] == "init value":
            val, time = val[1:], time[1:]

        val = list(map(float, val))
        if ns not in value_groups:
            value_groups[ns] = {na: [time, val, init_val]}
        else:
            value_groups[ns][na] = [time, val, init_val]
    return value_groups

def var_plot(operable_vars: dict, timeformat, params, scatter=False):
    """ 绘制变量 """
    values = group_var(operable_vars)

    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter
    from matplotlib.ticker import MaxNLocator
    import datetime

    # plt.figure(dpi=500)

    for group, contain in values.items():
        x = contain['x'][1]
        y = contain['y'][1]
        params_list = list(map(int, params.split()))
        scaling_factor = 50

        # plot_bins为热点图绘图x, y方向分隔的bin数，由传入长宽参数计算
        if len(params_list) == 2:
            plot_bins = tuple(abs(num) // scaling_factor for num in params_list)
            if (plot_bins[0]) > 100 or (plot_bins[1]) > 100:
                plot_bins = tuple(num // 10 for num in plot_bins)
        else:
            plot_bins = (40, 20) #default 

        plt.figure(figsize=(8, 6))

        # 正常情况下平板状态x_max > y_max, 如果log中x_max < y_max, 反转一下坐标xy
        if len(params_list) == 2:
            x_max, y_max = params_list
            if abs(x_max) < abs(y_max):
                x, y = y, x
                plot_bins = tuple(plot_bins[::-1])

        plt.hist2d(x, y, cmin=0.5, bins=plot_bins, cmap='Wistia')
        plt.colorbar(label='Counts in bin')
        plt.xlabel('X')
        plt.ylabel('Y')

        if len(params_list) == 2:
            x_max, y_max = params_list
            # 正常情况下平板状态x_max > y_max, 如果log中x_max < y_max, 反转一下图参数xy
            if abs(x_max) < abs(y_max):
                x_max, y_max = y_max, x_max
                plt.xlabel('Y')
                plt.ylabel('X')
            plt.xlim([0, abs(x_max)])
            plt.ylim([0, abs(y_max)])

            # x_max或ymax为负值时，反转坐标轴，以确保log中坐标画出的热点图与实际方向一致
            if x_max < 0:
                plt.gca().invert_xaxis()
            if y_max < 0:
                plt.gca().invert_yaxis()

        plt.gca().set_aspect('equal', adjustable='box')
        plt.title(f'[lo2] {group}')
        plt.show()

def entry_point(*args, **kwargs):
    """ 入口函数 """
    vars = kwargs.get('vars', None)
    _ = kwargs.get('states', None)
    timeformat = kwargs.get('timeformat', None)
    params = kwargs.get('params', None)
    var_plot(vars, timeformat, params, scatter=True)