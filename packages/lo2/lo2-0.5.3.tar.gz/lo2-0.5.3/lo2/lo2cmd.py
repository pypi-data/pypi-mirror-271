# -*- coding: utf-8 -*-
"""
lo2 cmd
"""
import argparse
import os

if __name__ == "__main__":
    import src as lo2
    from plugins import dispatch, plugins
else:
    import lo2
    from lo2.plugins import dispatch, plugins

def print_error(text):
    """ 使用红色字体来打印错误信息 """
    print(f'\033[31m{text}\033[0m')

def html_output(state_list, lo2lang, lines):
    """ 输出html格式的页面 """
    for e in state_list:
        e["state"] = e["state"].name

    render_data = {
        "state_list": state_list,
        "textlog": lines,
        "coverage": lo2lang.coverage,
        "lo2_fn": lo2lang.lo2_src_name,
    }
    out_dir = os.getcwd()
    html_mvc = lo2.html.MVC()
    html_mvc.model(render_data).to_controller("timeline").to_html(outdir=out_dir)

def parse_arguments():
    """ 解析命令行参数 """
    # 创建一个解析器对象
    parser = argparse.ArgumentParser(description="LogOracle 2.0")
    # 添加命令行参数 -s/--syntax   表示语法文件的路径 文件应以.json或.lo2结尾
    parser.add_argument('-s', '--syntax', required=True, help="Path to the syntax file")
    # 添加命令行参数 -l/--log      表示日志文件的路径
    parser.add_argument('-l', '--log', required=True, help="Path to the log file or adb device name")
    # 添加命令行参数 -r/--realtime 表示当前是否处于实时模式 实时模式下将直接输出结果
    parser.add_argument('-r', '--realtime', action='store_true', help="Enable real-time mode")
    # 添加命令行参数 -d/--details  表示是否开启详细输出 该参数是可选的
    parser.add_argument('-d', '--details', action='store_true', help="Enable details output")
    # 添加命令行参数 -c/--child    表示是否输出子oracle的匹配结果 该参数是可选的
    parser.add_argument('-c', '--child', action='store_true', help="Enable child oracle output")
    # 添加命令行参数 -v/--variable 表示是否开启输出monitor变量的变化过程 该参数是可选的
    parser.add_argument('-v', '--variable', action='store_true', help="Enable monitor variable output")
    # 添加命令行参数 -p/--page     表示是否输出html格式的可视化网页 该参数是可选的
    parser.add_argument('-p', '--page', action='store_true', help="Enable page output")
    # 添加命令行参数 -o/--doc     表示是否输出模式的文档内容 该参数是可选的
    parser.add_argument('-o', '--doc', action='store_true', help="Print Document")
    # 添加命令行参数 -f/--f   log文件类型，包括lernle与logcat，携带该参数，则--log应该为一个目录
    parser.add_argument('-f', '--ftype', help="File type of argument in --log")
    # 添加命令行参数 --plugin   使能插件功能
    parser.add_argument('-g', '--plugin', help="Enable Plugins", action='store_true')
    return parser.parse_args()

def preprocess_log(log_path, type="kernel"):
    """ 预处理日志文件 """
    CONCATED_KERNEL_FILE = "concat_kernel.log"
    CONCATED_LOGCAT_FILE = "concat_logcat.log"
    if os.path.isfile(log_path):
        #utils.preprocess_file_in_place(log_path)
        return log_path
    else:
        folder = log_path

    if type == "kernel":
        kernel_files = lo2.utils.get_kernel_file(folder)
        concat_kernel_file = os.path.join(folder, CONCATED_KERNEL_FILE)
        if not os.path.exists(concat_kernel_file):
            lo2.utils.concatenate_files(concat_kernel_file, file_list=kernel_files)
        return concat_kernel_file
    else:
        logcat_files = lo2.utils.get_logcat_file(folder)
        concat_logcat_file = os.path.join(folder, CONCATED_LOGCAT_FILE)
        if not os.path.exists(concat_logcat_file):
            lo2.utils.concatenate_files(concat_logcat_file, file_list=logcat_files)
        return concat_logcat_file

def main():
    """
    该函数用于解析语法文件并处理日志文件，根据参数执行不同的操作
    """
    args = parse_arguments()

    log_path = preprocess_log(args.log, args.ftype) if args.ftype else args.log

    # 使用lo2模块解析语法文件并处理日志文件
    lo2lang = lo2.parser.Lo2IRExecutor(args.syntax,
                                 log_path,
                                 args.details,
                                 args.child,
                                 args.realtime)
    # 注册插件
    lo2lang.plugin_register(plugins)
    ast = lo2lang.parser()
    if args.realtime:
        lo2lang.run_log()
    else:
        state_list = lo2lang.run_log()
        for i in state_list:
            lo2lang.lo2print.print_oracle(i, lo2lang.docs if args.doc else None)
        print()
        lo2lang.lo2print.print_coverage(lo2lang.src_name, lo2lang.coverage)

    print("Start process ...")
    if not args.realtime and args.page:
        with open(log_path, "r", errors="replace") as f:
            lines = [line.strip() for line in f]
        html_output(state_list, lo2lang, lines)
        
    if args.variable:
        lo2lang.lo2print.var_output(lo2lang.operable_vars)

    if args.plugin:
        dispatch(lo2lang.plugins_requirements,
                state_list,
                lo2lang.operable_vars,
                timeformat=lo2lang.timeformat)

if __name__ == "__main__":
    main()
