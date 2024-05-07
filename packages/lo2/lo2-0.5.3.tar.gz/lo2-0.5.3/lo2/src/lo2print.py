#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liermeng
"""

from .lo2state import *
from .lo2log import *
from datetime import datetime

class Lo2OraclePrint:
    """ Lo2Oracle 打印类"""
    def __init__(self,
                verbose=False,
                child_output=False,
                timeformat: str = '',
                child_oracle_name: dict = {}
                ):
        self.verbose = verbose
        self.timeformat = timeformat
        self.child_output = child_output
        self.child_oracle_name = child_oracle_name

    def time_diff(self, start: str, end: str) -> int:
        """
        计算两个时间戳的差值
        Args:
            start: 开始时间
            end: 结束时间
        Returns:
            时间差
        """
        elapsed_type = ["%S.%f"]

        if self.timeformat in elapsed_type:
            #elapsed type
            return round(float(end) - float(start), 4)
        else:
            # date type
            return (datetime.strptime(end, self.timeformat) - datetime.strptime(start, self.timeformat)).total_seconds()


    def print_oracle(self, oracle, docs=None):
        """ 打印oracle """
        if oracle["state"] == NodeState.Ok or oracle["state"] == NodeState.ChildOk:
            pr = prompt_success
        elif oracle["state"] == NodeState.Warn or oracle["state"] == NodeState.ChildWarn:
            pr = prompt_warn
        elif oracle["state"] == NodeState.Error or oracle["state"] == NodeState.ChildError:
            pr = prompt_error
        else:
            pr = prompt_info

        # 如果是子oracle 则打印其对应的名称
        name_width = 35
        state_width = 10
        doc_width = 25
        state_str = oracle["state"].name

        oracle["duration"] = self.time_diff(*oracle["time"])

        def get_format_doc(name):
            """ 获取文档格式化字符串 """
            if docs and oracle["rname"] in docs:
                return f'  {docs[oracle["rname"]]:<{doc_width}}'
            return ""

        msgs = []
        if oracle["name"] in self.child_oracle_name:
            oracle["rname"] = self.child_oracle_name[oracle["name"]]
            if self.child_output == True:
                msgs.append(f'\t|- {self.child_oracle_name[oracle["name"]]:<{name_width}} {state_str:<{state_width}} Time: {oracle["time"][0]} ~ {oracle["time"][1]}' + get_format_doc(oracle["rname"]))
                if oracle["state"] == NodeState.ChildError:
                    msgs.append(f'\t|\t|- Line: {oracle["line"]}')
                    if oracle["fail_reason"] != "":
                        msgs.append(f'\t|\t|- {oracle["fail_reason"]}')
                    else:
                        msgs.append(f'\t|\t|- {PatternFailReason.WarningPatternSuccess}')
                else:
                    if self.verbose:
                        msgs.append(f'\t|\t|- Line: {oracle["line"]}')
        else:
            oracle["rname"] = oracle["name"]
            if oracle["state"] in oracle["omitprint"]:
                return
            msgs.append(f'|- {oracle["name"]:<{name_width}} {state_str:<{state_width}} Time: {oracle["time"][0]} ~ {oracle["time"][1]}' + get_format_doc(oracle["rname"]))
            if oracle["state"] == NodeState.Error or oracle["state"] == NodeState.Warn:
                msgs.append(f'|\t|- Line: {oracle["line"]}')
                if oracle["fail_reason"] != "":
                    msgs.append(f'|\t|- {oracle["fail_reason"]}')
                else:
                    msgs.append(f'|\t|- {PatternFailReason.WarningPatternSuccess}')
            else:
                if self.verbose:
                    msgs.append(f'|\t|- Line: {oracle["line"]}')

        for m in msgs: pr(m)

    def var_output(self, operable_vars: dict):
        """ 打印变量 """
        variable_list = [[], []]
        for k, v in operable_vars.items():
            monitor_flag = int(v["monitor"])
            if v["global"]:
                variable_list[monitor_flag].append('')

                msg = f"Variable {v['type']} {k[5:]}"
                if '@doc' in v: msg += f"\t{v['@doc']}"
                variable_list[monitor_flag].append(msg)
                if v["type"] == 'num':
                    for i in range(len(v['value'])):
                        if i == 0 and v["value"][i] == str(float("inf")):
                            continue
                        try:
                            value = float(v['value'][i])
                        except:
                            value = "Not Match Found"
                        variable_list[monitor_flag].append(f"{v['time'][i]}\t{value}")
                elif v["type"] == 'str':
                    for i in range(len(v['value'])):
                        if i == 0 and v["value"][i] == "$undefined$":
                            continue
                        variable_list[monitor_flag].append(f"{v['time'][i]}\t{str(v['value'][i])}")

        for i in variable_list[0]: print(i)
        print()
        for i in variable_list[1]: print(i)

    def print_coverage(self, src_name: str, coverage: float):
        """ 打印覆盖率 """
        print(f"Name: {src_name}, Coverage: {coverage} %")