#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:45:22 2023

@author: zhangte01
"""
from .lo2log import *
from .lo2print import *
from .lo2state import *
from .lo2text import *
from .Exception import SyntaxError, RuntimeError
import re
from math import inf
import copy
from . import lo2lang
import os
import json
import subprocess
import time

class Lo2IRExecutor:
    """
    Lo2中间语言解释器
    """
    def __init__(self, code_file='', log_path='',
                 detail_output=False, child_output=False, realtime_flag=False):

        if not os.path.exists(code_file):
            raise FileNotFoundError("code file not exists")

        code = None
        vars = None

        if code_file.endswith(".json"):
            with open(code_file, "r") as f:
                code = json.load(f)
        elif code_file.endswith(".lo2"):
            code, vars = lo2lang.to_ast(code_file)
            with open(code_file + ".json", "w") as f:
                json.dump(code, f)
        else:
            raise Exception("Syntax file must be a .json/.lo2 file")

        self.log_path = log_path
        self.log_type = check_log_path(log_path)
        if self.log_type != 1 and self.log_type != 0:
            raise Exception("log file is invalid")        

        # 正则表达式：取值范围
        self.pattern_sentence_count_1 = re.compile(r"^==\s*(\d+)$")                   # 匹配 ==x
        self.pattern_sentence_count_2 = re.compile(r"^\[\s*(\d+)\s*,\s*(\d+)\s*\]$")  # 匹配 [x1, x2]
        self.pattern_sentence_count_3 = re.compile(r"^>=\s*(\d+)$")                   # 匹配 >=x
        self.pattern_sentence_count_4 = re.compile(r"^(\d+)\s*<=$")                   # 匹配 x<=
        self.pattern_sentence_count_5 = re.compile(r"^<=\s*(\d+)$")                   # 匹配 <=x
        self.pattern_sentence_count_6 = re.compile(r"^(\d+)\s*>=$")                   # 匹配 x>=

        self.TOKEN_OPS_IDX = 0
        self.TOKEN_STAT_CNT_IDX = 1
        self.TOKEN_PATTERN = 2

        self.code = code
        self.vars = {}
        self.operable_vars = {}
        self.oracle_temp_vars = {}
        self.docs = {}
        self.omitprint = {} # 忽略打印的状态
        # 初始化self.operable_vars
        for k, v in vars.items():
            k = k.replace('$MACRO$', '')
            self.vars[k] = {
                **v,
                "type"   : v["type"],
                "value"  : [str(v["init_value"])],
                "monitor": v["monitor"],
                "global" : v["global"]
            }
            self.operable_vars[k] = {
                **v,
                "type"   : v["type"],
                "value"  : [str(v["init_value"])],
                "monitor": v["monitor"],
                "global" : v["global"],
                "time"   : ["init value"]
                # time用于存储value对应的更新时间
            }
        self.ast = None
        self.operable_ast = {}
        self.ops = ["is", "not"]
        self.rules = ["strict", "begin", "end", "$EMPTY_COND$"]
        self.re_timeformat = None
        self.timeformat = None
        self.lo2_src_name = None
        self.mismatched_type = {}
        self.matched_type = {}
        self.child_oracle_name = {}
        self.match_line = []
        self.realtime_flag = realtime_flag
        self.detail_output = detail_output
        self.child_output = child_output
        self.coverage = 0

        """
        {
            'root.tp': {"@plot": ["heatmap", "linear"], "@plot3D": ["heatmap3D", ]}
            'root.camera': {"@plot": ["heatmap", "linear"], "@plot3D": ["heatmap3D", ]}
        }
        """
        self.plugins_requirements = {}

        """
        {
            "@plot": {
                "heatmap":  heatmap.entry_point
            }
        }
        """
        self.plugins_registered = None

        # 内置变量
        self.buildin_var = ["interval_ms", "interval_s", "interval_m", "interval_h"]

    def plugin_register(self, plugins):
        """
        注册插件
        Args:
            plugins (dict): 插件字典
            {
                "@plot": {
                    "heatmap":  heatmap.entry_point
                }
            }
        """
        if self.plugins_registered:
            raise RuntimeError("plugin name already exists")
        self.plugins_registered = plugins

    @property
    def src_name(self):
        """ 获取源文件名 """
        return self.lo2_src_name

    def _parser_timeformat2regex(self, format):
        """
        解析时间格式
        "%y-%m-%d %H:%M:%S.%f"
        支持：
            %y: year
            %m: month
            %d: day
            %H: hour
            %M: minute
            %S: second
            %f: microsecond
        """
        # 解析正则表达式
        if isinstance(format, str):
            regex_pattern = re.sub(r"%[yYmMdDhHMSf]", r"(\\d+)", format)
            return re.compile(regex_pattern)

    def __check_ops_validate(self, op):
        """
        检查操作符的合法性 任何不合法都会抛出语法异常 合法则进行strip处理后返回

        Args:
            op: 待检查的操作符 字符串类型

        Returns:
            处理后的操作符 字符串类型

        Raises:
            RuntimeError: 操作符不合法时抛出异常 异常信息包含操作符内容
            RuntimeError: 操作符不是字符串类型时抛出异常
        """
        if isinstance(op, str):
            op = op.strip()
            if op not in self.ops:
                raise SyntaxError(f"Invalid operator: {op}")
            return op
        raise SyntaxError(f"operator must be a string: {op}")

    def __check_stat_cnt_validate(self, cnt):
        """
        检查模式次数匹配的合法性 任何不合法都会抛出语法异常 
        合法则转换为统一的模式次数匹配区间 然后返回

        Args:
            cnt (TYPE): 待检查的模式次数区间字符串

        Returns:
            TYPE: 转换后的统一的模式次数匹配区间

        Raises:
            RuntimeError: 模式次数区间不是字符串类型时会抛出语法异常Syntax error: interval of pattern occurrences must be a string
        """

        if isinstance(cnt, str):
            return self.parser_sentence_count(cnt)
        else:
            raise SyntaxError(
                f"interval of pattern occurrences must be a string"
            )

    def __check_pattern_validate(self, pattern):

        def single_pattern_parser(single_pattern: str):
            # 如果是字符串则去掉头后直接返回
            if single_pattern.startswith("$S$"):
                return single_pattern[3:]
            # 如果是正则表达式 则返回re.compile后的对象
            elif single_pattern.startswith("$R$"):
                return re.compile(single_pattern[3:])
            # 如果是带变量的匹配语句 则返回一个只有一个key-value对的字典
            elif single_pattern.startswith("$F$"):
                return {"variable": single_pattern[3:]}
            else:
                raise SyntaxError(
                    "pattern(str) must starts with '$S$', '$R$' or '$F$'"
                )

        if isinstance(pattern, str):
            return single_pattern_parser(pattern)

        pattern_mode = 0
        # 如果当前pattern是多个匹配或者子oracle
        if isinstance(pattern, list):
            if isinstance(pattern[0], str):
                if len(pattern) == 2:
                    pattern_mode = 1 # 多个匹配模式 但仅有一个匹配对象
                elif isinstance(pattern[1], str):
                    pattern_mode = 1 # 多个匹配模式
                elif isinstance(pattern[1], list):
                    pattern_mode = 2 # 子oracle

        if pattern_mode == 1:
            res = [pattern[0]] # 存储匹配式
            for e in pattern[1:]:
                if isinstance(e, str):
                    res.append(single_pattern_parser(e))
                else:
                    raise SyntaxError(
                        f"pattern must be a str or list[str], but got {pattern} which is {type(pattern)}"
                    )
            return res
        elif pattern_mode == 2:
            return {"child-oracle": pattern}
        else:
            raise SyntaxError(
                f"pattern must be a str or list[str], but got {pattern} which is {type(pattern)}"
            )

    def __check_rule_validate(self, rule):
        if not isinstance(rule, list):
            raise SyntaxError(
                f"pattern rule must be a list, but got {rule} which is {type(rule)}"
            )
        for r in rule:
            if isinstance(r, str):
                r = r.strip()
                if r not in self.rules:
                    raise SyntaxError(f"Invalid rule: {r}")
            else:
                raise SyntaxError(
                    f"pattern rule's member must be a str, but got {r} which is {type(r)}"
                )
        return rule

    def variable_check(self, variable_pattern_origin, variable_namespace, pattern_type):
        """ var变量检查 """
        variable_pattern = ''
        variable_cur = ''
        variable_list = []

        # 首先记录所有进行取值操作的变量 并将变量命名替换成完整变量名 方便后续匹配
        variable_flag = False
        for i in variable_pattern_origin:
            # 一个变量匹配完成
            if ((pattern_type is VariablePatternState.Access and i == '}') or
                (pattern_type is VariablePatternState.Assign and i == ')')):
                variable_flag = False
                # 检查将加入的变量是否被定义过
                if f"{variable_namespace}.{variable_cur}" in self.vars:
                    variable_cur = f"{variable_namespace}.{variable_cur}"
                elif f"root.{variable_cur}" in self.vars:
                    variable_cur = f"root.{variable_cur}"
                else:
                    raise SyntaxError(f"variable {variable_cur} was not defined")

                if ((pattern_type is VariablePatternState.Assign) or
                    (pattern_type == VariablePatternState.Access and variable_cur not in variable_list)):
                    variable_list.append(variable_cur)

                if pattern_type is VariablePatternState.Assign:
                    if self.vars[variable_cur]["type"] == "num":
                        variable_cur = r'[+-]?\d+\.\d*|[+-]?\d+'
                    elif self.vars[variable_cur]["type"] == "str":
                        variable_cur = ".*"

                variable_pattern += variable_cur

                variable_cur = ''

            if variable_flag:
                variable_cur += i
            else:
                variable_pattern += i

            if ((pattern_type is VariablePatternState.Access and i == '{') or
                (pattern_type is VariablePatternState.Assign and i == '(')):
                variable_flag = True

        return variable_pattern, variable_list

    def code_lexer(self, lo2_code, tokens={}, pattern_name="", child_oracle_flag=False):
        """
        child_oracle_flag: 标记是否是子oracle
        json log oracle to lo ir
        ----------
        lo_code : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        child_oracle_num = 1
        for k, v in lo2_code.items():
            # sub config
            # oracle的错误类型 子oracle不支持自定义mismatched_type

            # 含有$MACRO$标识的oracle不参与匹配
            if "$MACRO$" in k:
                continue

            if "@mismatched" == k and isinstance(v, str):
                self.mismatched_type[pattern_name] = v.strip()
            elif "@matched" == k and isinstance(v, str):
                self.matched_type[pattern_name] = v.strip()
            # 如果是在解析oracle或子oracle
            # TODO(zhangte01@baidu.com): 这里有一些缺陷：可以在任何地方定义时间戳格式 但是只支持一个时间戳 也就是
            # 如果存在多个时间戳 会发生覆盖 这里以后要改成
            elif "@timeformat" == k.strip():
                self.timeformat = v
                self.re_timeformat = self._parser_timeformat2regex(v)
            elif "@name" == k.strip():
                self.lo2_src_name = v
            elif "@doc" == k.strip():
                self.docs[pattern_name] = v.strip()
            elif "@omitprint" == k.strip():
                self.omitprint[pattern_name] = [MATCH_TYPE_MAP.get(e.strip(), "") for e in v.split(",")]
            elif self.plugins_registered and k.strip() in self.plugins_registered:
                """
                {
                    'root.tp': {"@plot": ["heatmap 1600 2560", "linear 1920 1080"], "@plot3D": ["heatmap3D", ]}
                    'root.camera': {"@plot": ["heatmap", "linear"], "@plot3D": ["heatmap3D", ]}
                }
                """
                plugin_type = k.strip()
                plugin_configs = [v.strip() for v in v.split(",") if len(v) > 0]
                plugin_names = [config.split(maxsplit=1)[0].strip() for config in plugin_configs]
                split_configs = [config.split(maxsplit=1) for config in plugin_configs]
                plugin_params = [params[1].strip() if len(params) > 1 else '' for params in split_configs]
                
                # 解析示例：
                # plugin_configs = ['heatmap 1600 2560", "linear 1920 1080']
                # plugin_name = ['heatmap', 'linear']
                # plugin_params = ['1600 2560', '1920 1080'] 参数可能为空，空时为空字符串

                # 检查plugin_name与plugin_params长度是否一致
                assert len(plugin_names) == len(plugin_params), "Mismatch in number of plugin names and params"
                
                for plugin, params in zip(plugin_names, plugin_params):
                    if pattern_name in self.plugins_requirements:
                        if plugin_type in self.plugins_requirements[pattern_name]:
                            self.plugins_requirements[pattern_name][plugin_type].append({plugin: params})
                        else:
                            self.plugins_requirements[pattern_name][plugin_type] = [{plugin: params}]
                    else:
                        self.plugins_requirements[pattern_name] = {plugin_type: [{plugin: params}]}
            elif k == "oracle" or child_oracle_flag:
                
                # 对于子oracle 序列第一项是一个str 标识该子oracle的名称
                if child_oracle_flag:
                    if not isinstance(v[0], str):
                        raise SyntaxError("child oracle must have its own name")
                    # 如果子oracle未命名 则继续使用父oracle.childOracle[数字]命名
                    if v[0] != "":
                        self.child_oracle_name[pattern_name] = v[0]
                    v = v[1:]
                
                if not isinstance(v, list):
                    raise SyntaxError("oracle or child-oracle must be a list")

                for item, rule in zip(v[::2], v[1::2]):
                    if not isinstance(item, list):
                        raise SyntaxError("members' value of oracle must be a list or a child-oracle")

                    op = self.__check_ops_validate(item[self.TOKEN_OPS_IDX])
                    cnt = self.__check_stat_cnt_validate(item[self.TOKEN_STAT_CNT_IDX])
                    pattern = self.__check_pattern_validate(item[self.TOKEN_PATTERN])
                    rule = self.__check_rule_validate(rule)

                    dict_type = 0 # 1: pattern是字典且是子oracle 2: pattern是字典且是variable语句
                    if isinstance(pattern, dict):
                        # 如果是子oracle
                        if 'child-oracle' in pattern:
                            dict_type = 1
                            child_oracle_items = pattern['child-oracle']
                            pattern = {f'{pattern_name}.childOracle{child_oracle_num}': child_oracle_items}
                        # 如果是带变量的匹配语句
                        elif 'variable' in pattern:
                            dict_type = 2

                            if child_oracle_flag is True:
                                variable_namespace = self.child_oracle_name[pattern_name]
                            else:
                                variable_namespace = pattern_name

                            # 首先记录所有进行取值操作的变量 并将变量命名替换成完整变量名 方便后续匹配
                            variable_pattern, variable_list_access = self.variable_check(
                                pattern['variable'],
                                variable_namespace,
                                VariablePatternState.Access
                            )
                            # 再记录所有进行赋值操作的变量 并根据变量类型替换其为数字匹配或者.* 方便正则匹配
                            variable_pattern, variable_list_assign = self.variable_check(
                                variable_pattern,
                                variable_namespace,
                                VariablePatternState.Assign
                            )

                            # 数字0仅为标识当前匹配是变量匹配
                            pattern = [variable_pattern, variable_list_access, variable_list_assign, 0]

                    # 如果是多条匹配模式 则需要再对list进行一次解析
                    elif isinstance(pattern, list):
                        for p_idx in range(1, len(pattern)):
                            if isinstance(pattern[p_idx], dict) and 'variable' in pattern[p_idx]:
                                if child_oracle_flag is True:
                                    variable_namespace = self.child_oracle_name[pattern_name]
                                else:
                                    variable_namespace = pattern_name

                                # 首先记录所有进行取值操作的变量 并将变量命名替换成完整变量名 方便后续匹配
                                variable_pattern, variable_list_access = self.variable_check(
                                    pattern[p_idx]['variable'],
                                    variable_namespace,
                                    VariablePatternState.Access
                                )
                                # 再记录所有进行赋值操作的变量 并根据变量类型替换其为数字匹配或者.* 方便正则匹配
                                variable_pattern, variable_list_assign = self.variable_check(
                                    variable_pattern,
                                    variable_namespace,
                                    VariablePatternState.Assign
                                )

                                # 数字0仅为标识当前匹配是变量匹配
                                pattern[p_idx] = [variable_pattern, variable_list_access, variable_list_assign, 0]

                    # 初始化tokens
                    if pattern_name not in tokens:
                        tokens[pattern_name] = [[op, cnt, pattern, rule]]
                    # 修改对应的value
                    else:
                        tokens[pattern_name].append([op, cnt, pattern, rule])

                    # 如果是子oracle 则迭代解析
                    if isinstance(pattern, dict) and dict_type == 1:
                        self.code_lexer(pattern, tokens,
                                        f"{pattern_name}.childOracle{child_oracle_num}", True)
                        child_oracle_num = child_oracle_num + 1

            # a module
            else:
                if isinstance(v, dict) and "@ignore" not in v:
                    self.code_lexer(v, tokens, f"{pattern_name}.{k}" if pattern_name else k)

        return tokens

    def parser_sentence_count(self, sentence):
        """
        转换lo2 lang 的次数判断语句到ir格式
        ----------
        sentence : TYPE
            pattern1, '==1': 1
            pattern2, '[1, 2]': [1, 2]

            pattern3, '>=1': [1, inf]
            pattern4, '1<=': [1, inf]

            pattern5, '<=5': [-inf, 5]
            pattern6, '5>=': [-inf, 5]

        Returns
        -------
        None.

        """
        sentence = sentence.strip()

        match = self.pattern_sentence_count_1.match(sentence)
        if match:
            return int(match.group(1))

        match = self.pattern_sentence_count_2.match(sentence)
        if match:
            return int(match.group(1)), int(match.group(2))

        match = self.pattern_sentence_count_3.match(sentence)
        if match:
            return int(match.group(1)), inf

        match = self.pattern_sentence_count_4.match(sentence)
        if match:
            return int(match.group(1)), inf

        match = self.pattern_sentence_count_5.match(sentence)
        if match:
            return -inf, int(match.group(1))

        match = self.pattern_sentence_count_6.match(sentence)
        if match:
            return -inf, int(match.group(1))

        raise SyntaxError(f"Invalid sentence count: {sentence}")

    def ast_syntax_check(self, tokens):
        """
        检查输入的tokens合法性 输入是已经转换为ir结构并且完成语句次数条件转换的tokens格式
        ----------
        tokens : TYPE
            DESCRIPTION.

        Raises
        ------
        RuntimeError
            DESCRIPTION.

        Returns
        -------
        tokens : TYPE
            DESCRIPTION.

        """
        # child-oracle 不能作为序列的起止条件
        for k, v in tokens.items():
            if len(v) > 1:
                # 第一个操作符必须是is 这样才有终止条件
                oracle = v[0]
                if oracle[self.TOKEN_OPS_IDX] != 'is':
                    raise SyntaxError(
                        f"Invalid operator, the first of ops must be is:{k}: {oracle[self.TOKEN_OPS_IDX]}"
                    )

                oracle = v[-1]
                # 最后一个操作符必须是is 这样才有终止条件
                if oracle[self.TOKEN_OPS_IDX] != 'is':
                    raise SyntaxError(
                        f"Invalid operator, the end of ops must be is:{k}: {oracle[self.TOKEN_OPS_IDX]}"
                    )

            # 对于只有一个操作符的序列 可以是is or not
            elif len(v) == 1:
                if v[0][self.TOKEN_OPS_IDX] not in ['is', 'not']:
                    raise SyntaxError(
                        f"Invalid operator, the ops, if a single, must in [is, not]:{k}: {v[0][self.TOKEN_OPS_IDX]}"
                    )

        return tokens

    def parser(self):
        """
        解析lo2 返回ast
        """
        if self.code:
            # 转换lo2为ir的格式
            tokenizer = self.code_lexer(self.code)

            # 检查合法性
            self.ast = self.ast_syntax_check(copy.deepcopy(tokenizer))

            # 构造一个镜像的ast 这个ast用于添加一些run时候的中间状态 不对原ast进行操作
            self.create_operable_ast(self.ast)
            return self.ast
        else:
            prompt_warn("No code here")

    def __check_is_child(self, child_key, father_key):
        """
        检查两个key值是否为父子关系

        Args:
            child_key father_key: 待检查是否为父子关系的两个key

        Returns:
            True: father_key为是child_key的父节点

        for example:
            father_key: "xxx"
            child_key:  "xxx.childOracle[任意数字]"
            return True
        """
        child_pattern = re.compile(r"%s\.childOracle\d+" % re.escape(father_key))
        if child_pattern.search(child_key):
            return True
        else:
            return False


    def __create_initialized_ast_node(self, oracle, father_oracle, child_oracle_list, 
                                      mismatched_type=MATCH_TYPE_ERROR, matched_type=MATCH_TYPE_OKAY):
        """
        创建初始化的ast节点 用于记录上下文状态
        oracle:            预言序列
        father_oracle:     父oracle(如果自己就是根oracle则为None)
        child_oracle_list: 子oracle列表(如果自己就是叶oracle则为[])
        match_states:      匹配状态
        match_next_states: 下一个状态的匹配情况 用于识别下一个状态已经开始
        last_state:        该事件之前匹配的状态
        state:             当前该事件匹配的状态
        ok total:          记录ok的次数
        last ok total      用于子oracle 记录之前一次ok的次数(用于判断是否有新增的匹配成功的子事件)
        fail total:        记录fail的次数
        """
        return {
            "oracle": oracle,
            "father": father_oracle,
            "child" : child_oracle_list,
            "match_states": [
                0 if e[0] == "not" else None for e in oracle
            ],
            "match_next_states": [
                0 if e[0] == "not" else None for e in oracle
            ],
            "last_state": NodeState.Idle,
            "state": NodeState.Idle,
            "mismatched_type": MATCH_TYPE_MAP.get(mismatched_type, NodeState.Error),
            "matched_type": MATCH_TYPE_MAP.get(matched_type, NodeState.Ok),
            "ok total": 0,
            "last ok total": 0,
            "fail total": 0,
            "fail reason": ""
        }

    def create_operable_ast(self, ast=None):
        """
        创建镜像ast 这个ast用于记录上下文状态
        """
        if not ast:
            ast = self.ast

        self.operable_ast = {}
        for k, v in ast.items():
            father_oracle = None
            child_oracle_list = []

            mismatched_type = self.mismatched_type[k] if k in self.mismatched_type else MATCH_TYPE_ERROR
            matched_type = self.matched_type[k] if k in self.matched_type else MATCH_TYPE_OKAY

            for k1, v1 in ast.items():
                if self.__check_is_child(k1, k):
                    child_oracle_list.append(k1)
                elif self.__check_is_child(k, k1):
                    father_oracle = k1

            self.operable_ast[k] = self.__create_initialized_ast_node(v, father_oracle, child_oracle_list,
                                                                      mismatched_type, matched_type)

        return self.operable_ast

    def print_ast(self):
        """
        打印ast ast用于记录上下文状态
        """
        for k, v in self.ast.items():
            prompt_info(k, indent=0)
            for e in v:
                prompt_info(e, indent=4)

    def print_operable_ast(self):
        """
        打印镜像ast 镜像ast用于记录上下文状态
        """
        for k, v in self.operable_ast.items():
            prompt_info(k, indent=0)
            for idx, o in enumerate(v["oracle"]):
                prompt_info(o, v["match_states"][idx], indent=4)

    def print_code_summary(self, code, indent=0):
        """
        打印代码摘要信息 用于调试和展示代码结构。

        Args:
            code (dict):            待打印的代码字典
            indent (int, optional): 缩进级别 默认为0

        Returns:
            None.
        """
        for k, v in code.items():
            # sub config
            if isinstance(v, dict) and "oracle" not in v:
                prompt_info(k, indent=indent * 4)
                self.print_code_summary(v, indent + 1)
            # a module.
            elif "oracle" in v:
                prompt_info(k, indent=indent * 4)
                self.print_code_summary(v, indent + 1)
            # a oracle
            elif "oracle" == k and isinstance(v, list):
                for e in v:
                    prompt_info(" " * indent * 4, e)

    def __reset_match_states(self, node_name):
        """
        重置指定模块的 match_states 状态列表

        Args:
            module_name: str类型 指定要重置 match_states 状态的模块名

        Returns:
            None
        """
        stat_list = self.operable_ast[node_name]["oracle"]
        self.operable_ast[node_name]["match_states"] = [
            0 if e[0] == "not" else None for e in stat_list
        ]

    def __reset_match_next_states(self, node_name):
        """
        重置指定模块的 match_states 状态列表

        Args:
            module_name: str类型 指定要重置 match_states 状态的模块名

        Returns:
            None
        """
        stat_list = self.operable_ast[node_name]["oracle"]
        self.operable_ast[node_name]["match_next_states"] = [
            0 if e[0] == "not" else None for e in stat_list
        ]

    def __copy_next_state_to_state(self, node_name):
        """
        将 match_next_states 状态列表中的值复制到 match_states 状态列表中
        """
        mod = self.operable_ast[node_name]
        self.__reset_match_states(node_name)
        mod["match_states"] = copy.deepcopy(mod["match_next_states"])
        self.__reset_match_next_states(node_name)

    def is_state_matching(self, node_name: str) -> NodeState:
        """ 一个模块的上下文状态是否匹配 """
        mod = self.operable_ast[node_name]
        for idx, count in enumerate(mod['match_states'][:-1]):
            op = mod['oracle'][idx][0]
            limit = mod['oracle'][idx][1]

            if isinstance(limit, int):
                if ((op == "is" and count != limit) or
                    (op == "not" and count == limit)):
                    return False, idx, count
            elif isinstance(limit, tuple):
                if ((op == "is" and not (limit[0] <= count <= limit[1])) or
                    (op == "not" and limit[0] <= count <= limit[1])):
                    return False, idx, count
        return True, -1, -1

    def __check_state(self, node_name: str) -> NodeState:
        """
        检查ast中每个子模块的上下文状态
        Args:
            node_name (str): 节点名称
        Returns:
            NodeState: 节点状态
        """

        mod = self.operable_ast[node_name]
        end_idx = len(mod["oracle"]) - 1
        oraclen_len = len(mod["oracle"])
        for idx, o in enumerate(mod["oracle"]):
            op = o[0]
            count = o[1]
            sentence = o[2]
            cur_cnt = mod["match_states"][idx]
            next_cnt = mod["match_next_states"][idx]

            if cur_cnt is None:
                continue

            if isinstance(count, int):
                lower_limit_cnt = upper_limit_cnt = count
            elif isinstance(count, tuple):
                lower_limit_cnt, upper_limit_cnt = count
            else:
                raise RuntimeError(f"unexcepted type {count}")

            # the condition of the end of pattern
            if (
                cur_cnt is not None
                and idx == end_idx
                and cur_cnt >= lower_limit_cnt
                and cur_cnt <= upper_limit_cnt
            ):
                if None not in mod["match_states"]:
                    if (
                        mod["state"] == NodeState.NextStart
                        or mod["state"] == NodeState.Pending
                    ):
                        state_match, fail_idx, fail_count = self.is_state_matching(node_name)
                        if state_match:
                            return mod["matched_type"] # 成功的状态 不会有None
                        else:
                            fail_sentence = self.operable_ast[node_name]['oracle'][fail_idx][2]
                            fail_limit = self.operable_ast[node_name]['oracle'][fail_idx][1]
                            fail_op = self.operable_ast[node_name]['oracle'][fail_idx][0]

                            fail_reason = PatternFailReason.PatternRuleNotMatch
                            fail_reason += f"Pattern rule '{fail_sentence}' requires '{fail_op} {fail_limit}' but got {fail_count}"

                            self.operable_ast[node_name]["fail reason"] = fail_reason
                            return mod["mismatched_type"]
                else:
                    if (
                        mod["state"] == NodeState.NextStart
                        or mod["state"] == NodeState.Pending
                    ):
                        for idx in range(len(mod["match_states"])):
                            if mod["match_states"][idx] is None:
                                fail_idx = idx
                                break

                        fail_sentence = self.operable_ast[node_name]['oracle'][fail_idx][2]
                        fail_reason = PatternFailReason.PatternRuleNotMatch
                        fail_reason += f"Pattern rule '{fail_sentence}' didn't get matched log"

                        self.operable_ast[node_name]["fail reason"] = fail_reason
                        return mod["mismatched_type"]

            # 下一个状态已经来临 如果当前当前状态是Pending 则当前状态失败
            if (
                next_cnt is not None
                and idx == 0
                and next_cnt >= lower_limit_cnt
                and next_cnt <= upper_limit_cnt
            ):
                if oraclen_len > 1:
                    # 对于起始匹配条件为 is >= 的情况进行特殊处理
                    if ((mod["state"] == NodeState.NextStart
                        or mod["state"] == NodeState.Pending)
                        and upper_limit_cnt == inf):
                        continue
                    return NodeState.NextStart
                elif oraclen_len == 1:
                    if op == "not":
                        self.operable_ast[node_name]["fail reason"] = PatternFailReason.WarningPatternSuccess
                        return mod["mismatched_type"]
                    elif op == "is":
                        return mod["matched_type"]

            if op == "not":
                if (
                    (cur_cnt >= lower_limit_cnt and upper_limit_cnt == inf) or
                    (cur_cnt <= upper_limit_cnt and lower_limit_cnt == inf)
                ):
                    if (
                        mod["state"] == NodeState.NextStart
                        or mod["state"] == NodeState.Pending
                    ):
                        fail_reason = PatternFailReason.PatternRuleNotMatch
                        fail_reason += f"Pattern rule '{sentence}' requires 'not {count}' but got {cur_cnt}"
                        self.operable_ast[node_name]["fail reason"] = fail_reason
                        return mod["mismatched_type"]
            elif op == "is":
                if cur_cnt > upper_limit_cnt:
                    if (
                        mod["state"] == NodeState.NextStart
                        or mod["state"] == NodeState.Pending
                    ):
                        fail_reason = PatternFailReason.PatternRuleNotMatch
                        fail_reason += f"Pattern rule '{sentence}' requires 'is {count}' but got {cur_cnt}"
                        self.operable_ast[node_name]["fail reason"] = fail_reason
                        return mod["mismatched_type"]
        else:
            # 必须是一个 NextStart 状态 或者 Pending 状态 才返回 Pending 状态
            if mod["state"] == NodeState.NextStart or mod["state"] == NodeState.Pending:
                return NodeState.Pending
            else:
                return NodeState.Idle

    def __update_state(self, node, idx):
        """
        更新指定模块的上下文状态

        Args:
            node: 模块
            idx: 当前匹配到的item在模块中的索引
        Returns:
            True: 更新成功
            False: 更新失败(strict规则)
        """

        # 判断当前匹配项是不是子oracle
        is_child_oracle_flag = isinstance(node["oracle"][idx][2], dict)
        # 如果是子oracle 获取子oracle的名称
        if is_child_oracle_flag:
            child_oracle = next(iter(node["oracle"][idx][2]))

        # 若匹配到终止规则 则可以直接更新状态
        if "strict" in node["oracle"][idx][3] and len(node["oracle"]) != idx + 1:
            for i in range(idx):
                op = node["oracle"][i][0]
                count = node["oracle"][i][1]
                if isinstance(count, int):
                    lower_limit_cnt = upper_limit_cnt = count
                elif isinstance(count, tuple):
                    lower_limit_cnt, upper_limit_cnt = count

                # 当前匹配项之前的语句如果没有匹配成功 则直接退出
                if node["match_states"][i] is None:
                    # 如果是子oracle 子oracle匹配的ok数量因为strict规则所以不作数 故减去1 下同
                    if is_child_oracle_flag:
                        self.operable_ast[child_oracle]["ok total"] -= 1
                        self.operable_ast[child_oracle]["last ok total"] -= 1
                    return False
                elif op == "is" and not lower_limit_cnt <= node["match_states"][i] <= upper_limit_cnt:
                    if is_child_oracle_flag:
                        self.operable_ast[child_oracle]["ok total"] -= 1
                        self.operable_ast[child_oracle]["last ok total"] -= 1
                    return False
                elif op == "not" and lower_limit_cnt <= node["match_states"][i] <= upper_limit_cnt:
                    if is_child_oracle_flag:
                        self.operable_ast[child_oracle]["ok total"] -= 1
                        self.operable_ast[child_oracle]["last ok total"] -= 1
                    return False

        # 如果当前匹配项不是子oracle 则直接更新
        if not is_child_oracle_flag:
            node["match_states"][idx] = (
                node["match_states"][idx] + 1
                if node["match_states"][idx] is not None
                else 1
            )
        else: # 如果当前匹配项是子oracle 则根据已匹配完毕的子oracle的数量更新当前匹配项的匹配状态
            node["match_states"][idx] = self.operable_ast[next(iter(node["oracle"][idx][2]))]["ok total"]

        # 对于下一个状态 只标记索引为 0 的模式 其他模式不处理 否则多个状态混合在一起
        # 完全无法判断一条语句应该向哪个状态标记
        # 必须是第一个匹配项已经出现多次才标记
        if idx == 0:
            node["match_next_states"][idx] = (
                node["match_next_states"][idx] + 1
                if node["match_next_states"][idx] is not None
                else 1
            )
        return True

    def read_timestamp_line(self, line: str) -> str:
        """
        从日志中读取时间戳
        """
        if self.re_timeformat:
            match = self.re_timeformat.search(line)
            if match:
                return match.group()

    def variable_list_update(self, oracle_name):
        """ 更新变量列表 """
        if oracle_name not in self.oracle_temp_vars:
            return

        for k, v in self.oracle_temp_vars[oracle_name].items():
            if self.operable_vars[k]["global"]:
                if self.operable_vars[k]["monitor"]:
                    self.operable_vars[k]["value"] += v["value"]
                    self.operable_vars[k]["time"] += v["time"]
                else:
                    self.operable_vars[k]["value"] = [v["value"][-1]]
                    self.operable_vars[k]["time"] = [v["time"][-1]]

        del self.oracle_temp_vars[oracle_name]

    def summary_list_update(self, oracle_name, state,
                            stamp: str, line_number: int,
                            fail_reason: str, oracle_vars: dict):

        """用于统计覆盖率"""
        self.match_line.append(line_number)

        # 非 Idle 状态 则记录成功匹配的行号及当前log时间(匹配开始时间)
        if state is not NodeState.Idle:
            if oracle_name in self.temp_state_summary:
                self.temp_state_summary[oracle_name].append(line_number)
            else:
                self.temp_state_summary[oracle_name] = [line_number]
            if oracle_name not in self.temp_begin_time:
                self.temp_begin_time[oracle_name] = stamp # 记录匹配开始时间

        # 遍历仍未和父oracle匹配的子oracle 删除其中和当前父节点匹配的oracle
        idx = 0
        while idx < len(self.child_no_match_father):
            if self.child_no_match_father[idx]["name"] in self.operable_ast[oracle_name]["child"]:
                if oracle_name not in self.temp_state_summary:
                    self.temp_state_summary[oracle_name] = []

                self.temp_state_summary[oracle_name] = list(
                                                            set(
                                                                self.temp_state_summary[oracle_name] + 
                                                                self.child_no_match_father[idx]["line"]
                                                            )
                                                        )
                self.temp_state_summary[oracle_name].sort()

                del self.child_no_match_father[idx]

            else:
                idx += 1

        if (
            state == NodeState.Ok
            or state == NodeState.Warn
            or state == NodeState.Error
        ):

            # 对于已经匹配的子oracle 且其父亲还未匹配的oracle 其father_match_flag为False
            father_match_flag = True
            if self.operable_ast[oracle_name]["father"] is not None:
                father_match_flag = False
            oracle_match_finish = {"name": oracle_name,
                                   "state": state,
                                   "omitprint": self.omitprint.get(oracle_name, []),
                                   "time": [self.temp_begin_time[oracle_name], stamp],
                                   "line": copy.deepcopy(self.temp_state_summary[oracle_name]),
                                   "fail_reason" : fail_reason,
                                   "vars": copy.deepcopy(oracle_vars)}

            # 实时模式下 不输出子oracle
            if self.realtime_flag:
                if oracle_name not in self.child_oracle_name:
                    self.lo2print.print_oracle(oracle_match_finish)
            else:
                self.summary_list.append(oracle_match_finish)

            if father_match_flag is False and state == NodeState.Ok:
                self.child_no_match_father.append(
                    {
                        "name": oracle_name,
                        "line": copy.deepcopy(self.temp_state_summary[oracle_name])
                    }
                )

            # 对于匹配完成的事件 更新其变量值到self.operable_vars
            self.variable_list_update(oracle_name)

            del self.temp_begin_time[oracle_name]
            del self.temp_state_summary[oracle_name]

    def line_sentence_match(self, sentence_pattern, line, oracle_name, is_begin_pattern=False):
        """
        用于判断当前匹配语句和行是否匹配 (匹配语句不包括子事件)
        同时获取当前行中所有匹配变量的情况
        """

        line_temp_vars = {}

        def line_sentence_match_variable(sentence_pattern, line):
            line_temp_vars = {}
            variable_pattern = sentence_pattern[0]
            for i in sentence_pattern[1]: # 遍历所有做取值操作的变量 替换其数值
                variable_cur = "{" + i + "}"
                if is_begin_pattern and not self.vars[i]["global"]:
                    value_cur = self.vars[i]["value"][0]
                elif oracle_name in self.oracle_temp_vars and i in self.oracle_temp_vars[oracle_name]:
                    value_cur = self.oracle_temp_vars[oracle_name][i]["value"][-1]
                else:
                    value_cur = self.operable_vars[i]["value"][-1]
                variable_pattern = variable_pattern.replace(variable_cur, str(value_cur))

                # 依次更新所有变量值的匹配值和匹配时间
                if i in line_temp_vars:
                    line_temp_vars[i].append(str(value_cur))
                else:
                    line_temp_vars[i] = [str(value_cur)]

            variable_pattern_re = re.compile(variable_pattern)
            match = re.search(variable_pattern_re, line)

            if match:
                for i in range(len(sentence_pattern[2])):
                    access_value = match.group(i + 1)

                    # 依次更新所有变量值的匹配值和匹配时间
                    var_name = sentence_pattern[2][i]
                    if var_name in line_temp_vars:
                        line_temp_vars[var_name].append(access_value)
                    else:
                        line_temp_vars[var_name] = [access_value]

            return match, line_temp_vars

        if isinstance(sentence_pattern, re.Pattern):
            return sentence_pattern.search(line), {}
        elif isinstance(sentence_pattern, str):
            return sentence_pattern in line, {}
        elif isinstance(sentence_pattern, list):
            # 如果是变量匹配语句
            if (len(sentence_pattern) == 4 and
                isinstance(sentence_pattern[0], str) and
                isinstance(sentence_pattern[1], list) and
                isinstance(sentence_pattern[2], list) and
                sentence_pattern[3] == 0):
                    return line_sentence_match_variable(sentence_pattern, line)
            # 如果是多条匹配规则(或匹配规则)
            else:
                sentence_expression = sentence_pattern[0]
                for s in sentence_pattern[1:]:
                    match = False
                    if isinstance(s, re.Pattern):
                        match = s.search(line)
                    elif isinstance(s, str):
                        match = s in line
                    elif isinstance(s, list):
                        if (len(s) == 4 and
                            isinstance(s[0], str) and
                            isinstance(s[1], list) and
                            isinstance(s[2], list) and
                            s[3] == 0):
                            line_temp_vars_expression = {}
                            match, line_temp_vars_expression = line_sentence_match_variable(s, line)
                            if match:
                                for k, v in copy.deepcopy(line_temp_vars_expression).items():
                                    if k not in line_temp_vars:
                                        line_temp_vars[k] = v
                                    else:
                                        line_temp_vars[k] += v
                            line_temp_vars_expression = {}
                    else:
                        raise SyntaxError(
                            f"Invalid sentence: {s} in or condition"
                        )
                    sentence_expression = sentence_expression.replace("#", str(bool(match)), 1)
                match = eval(sentence_expression)
                return match, line_temp_vars
        else:
            raise SyntaxError(
                f"Invalid sentence: {sentence_pattern}"
            )

    def run_line(self, line: str, line_number: int):
        """ run 1 line of log """
        is_match = False

        if not self.operable_ast:
            raise SyntaxError("There is no ast")

        summary_update_list = []
        stamp = self.read_timestamp_line(line) # 当前行的时间戳

        # 用于存储各个oracle在当前行中匹配到的变量值
        line_temp_vars_oracle = {}

        for k, v in reversed(self.operable_ast.items()):
            is_curr_pattern_match = False
            for idx, o in enumerate(v["oracle"]):
                op = o[0]
                count = o[1]
                sentence_pattern = o[2]

                is_begin_pattern = False

                if "begin" in o[3]:
                    is_begin_pattern = True

                is_var_update = False

                # 如果当前匹配规则不是子事件
                if (isinstance(sentence_pattern, re.Pattern) or
                    isinstance(sentence_pattern, str) or
                    isinstance(sentence_pattern, list)):
                    match, line_temp_vars = self.line_sentence_match(sentence_pattern, line, k, is_begin_pattern)
                    if match:
                        is_var_update = self.__update_state(v, idx)
                        is_match = True
                        is_curr_pattern_match = True
                # 如果当前匹配规则是子事件
                elif isinstance(sentence_pattern, dict):
                    child_oracle = next(iter(sentence_pattern))
                    # 子事件匹配成功数较之前有变化
                    if (self.operable_ast[child_oracle]["ok total"] > 
                        self.operable_ast[child_oracle]["last ok total"]):
                        self.operable_ast[child_oracle]["last ok total"] = self.operable_ast[child_oracle]["ok total"]
                        self.__update_state(v, idx)
                        is_curr_pattern_match = True
                else:
                    raise SyntaxError(
                        f"Invalid sentence: {sentence_pattern}"
                    )

                # 如果当前匹配语句匹配成功 且未受到strict规则约束 则更新变量值
                if is_var_update and line_temp_vars is not {}:
                    if k not in self.oracle_temp_vars:
                        self.oracle_temp_vars[k] = {}
                        for k1, v1 in line_temp_vars.items():
                            self.oracle_temp_vars[k][k1] = {"value": v1, "time": [stamp] * len(v1)}
                    else:
                        for k1, v1 in line_temp_vars.items():
                            if k1 not in self.oracle_temp_vars[k]:
                                self.oracle_temp_vars[k][k1] = {"value": v1, "time": [stamp] * len(v1)}
                            else:
                                self.oracle_temp_vars[k][k1]["value"] += v1
                                self.oracle_temp_vars[k][k1]["time"] += [stamp] * len(v1)
                    if k not in line_temp_vars_oracle:
                        line_temp_vars_oracle[k] = {}
                        for k1, v1 in line_temp_vars.items():
                            line_temp_vars_oracle[k][k1] = {"value": v1, "time": [stamp] * len(v1)}
                    else:
                        for k1, v1 in line_temp_vars.items():
                            if k1 not in line_temp_vars_oracle[k]:
                                line_temp_vars_oracle[k][k1] = {"value": v1, "time": [stamp] * len(v1)}
                            else:
                                line_temp_vars_oracle[k][k1]["value"] += v1
                                line_temp_vars_oracle[k][k1]["time"] += [stamp] * len(v1)

            if not is_curr_pattern_match:
                continue

            state = self.__check_state(k)
            v["last_state"] = v["state"]
            v["state"] = state

            if v["last_state"] == NodeState.Pending and v["state"] == NodeState.NextStart:
                # 对于新匹配开始且当前匹配未结束的oracle 需要直接更新状态
                self.summary_list_update(k, v["mismatched_type"],
                                         stamp, line_number,
                                         PatternFailReason.NewPatternStart,
                                         self.oracle_temp_vars[k])
                self.oracle_temp_vars[k] = line_temp_vars_oracle[k]
                # 需要重新修改self.operable_vars 否则会把下一行匹配行的变量重复统计一次
                for k1, v1 in line_temp_vars_oracle[k].items():
                    self.operable_vars[k1]["value"] = self.operable_vars[k1]["value"][:-len(v1["value"])]
                    self.operable_vars[k1]["time"] = self.operable_vars[k1]["time"][:-len(v1["time"])]

                # 状态匹配结束后 清空子oracle的ok total计数
                for child in self.operable_ast[k]["child"]:
                    self.operable_ast[child]["match_states"] = [None] * len(self.operable_ast[child]["match_states"])
                    self.operable_ast[child]["match_next_states"] = [None] * len(self.operable_ast[child]["match_next_states"])
                    self.operable_ast[child]["ok total"] = 0
                    self.operable_ast[child]["last ok total"] = 0

            if state in [
                NodeState.Warn,
                NodeState.Error,
                NodeState.Ok,
                NodeState.NextStart,
            ]:
                if state == NodeState.Warn or state == NodeState.Error:
                    v["state"] = NodeState.Finish
                    # 状态匹配结束后 清空之前的匹配计数
                    v["match_states"] = [None] * len(v["match_states"])
                    v["match_next_states"] = [None] * len(v["match_next_states"])
                    # 状态匹配结束后 清空子状态的计数
                    for child in self.operable_ast[k]["child"]:
                        self.operable_ast[child]["match_states"] = [None] * len(self.operable_ast[child]["match_states"])
                        self.operable_ast[child]["match_next_states"] = [None] * len(self.operable_ast[child]["match_next_states"])
                        self.operable_ast[child]["ok total"] = 0
                        self.operable_ast[child]["last ok total"] = 0
                elif state == NodeState.Ok:
                    v["ok total"] += 1
                    v["state"] = NodeState.Finish
                    # 状态匹配结束后 清空之前的匹配计数
                    v["match_states"] = [None] * len(v["match_states"])
                    v["match_next_states"] = [None] * len(v["match_next_states"])
                    # 状态匹配结束后 清空子状态的计数
                    for child in self.operable_ast[k]["child"]:
                        self.operable_ast[child]["match_states"] = [None] * len(self.operable_ast[child]["match_states"])
                        self.operable_ast[child]["match_next_states"] = [None] * len(self.operable_ast[child]["match_next_states"])
                        self.operable_ast[child]["ok total"] = 0
                        self.operable_ast[child]["last ok total"] = 0
                elif state == NodeState.NextStart:
                    # NextStart标志开始一个状态的匹配
                    # 会将匹配到的开头复制给当前状态匹配的上下文
                    # 这会导致上下文变量发生变化 因此需要再次检查状态
                    self.__copy_next_state_to_state(k)
                    state = self.__check_state(k)
                    v["state"] = state

            # 状态需要更新 将其加入summary_update_list
            if is_match:
                if k not in self.oracle_temp_vars:
                    self.oracle_temp_vars[k] = {}
                summary_update_list.append([k, state, 
                                            stamp, line_number,
                                            self.operable_ast[k]["fail reason"],
                                            self.oracle_temp_vars[k]])

        # 每一行匹配完成后 对于如下的情况进行处理:
        # 若父oracle的状态为Idle 即没有开始匹配 则将所有子oracle的状态重置为Idle
        # 当子oracle为父oracle的初始匹配语句时 不执行该部分
        for k, v in self.operable_ast.items():
            if v["state"] == NodeState.Idle:
                for child in self.operable_ast[k]["child"]:
                    if isinstance(v["oracle"][0][2], dict) and child in v["oracle"][0][2]:
                        continue
                    self.operable_ast[child]["state"] = NodeState.Idle
                    self.operable_ast[child]["match_states"] = [None] * len(self.operable_ast[child]["match_states"])
                    self.operable_ast[child]["match_next_states"] = [None] * len(self.operable_ast[child]["match_next_states"])
                    self.operable_ast[child]["ok total"] = 0
                    self.operable_ast[child]["last ok total"] = 0
                    summary_update_list = [i for i in summary_update_list if i[0] != child]

        for k, v in self.operable_ast.items():
            if v["state"] == NodeState.Finish:
                v["state"] = NodeState.Idle

        # 更新summary_list
        for i in summary_update_list:
            self.summary_list_update(i[0], i[1], i[2], i[3], i[4], i[5])

    def run_log(self):
        """ run log """
        line_number = 0
        self.match_line = []

        # 结果汇总
        self.summary_list = []   
        # 父事件未匹配完成的子事件的汇总       
        self.child_no_match_father = []
        # 父事件匹配成功的子事件的汇总
        self.child_match_father = []

        self.temp_state_summary = {}
        self.temp_begin_time = {}

        self.lo2print = Lo2OraclePrint(self.detail_output,
                                       self.child_output,
                                       self.timeformat,
                                       self.child_oracle_name)
        
        if self.log_type == 1:
            with open(self.log_path, "r", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    line_number += 1
                    self.run_line(line, line_number)
        else:
            try:
                adb_log = get_realtime_log(self.log_path)
                for line in adb_log:
                    line_number += 1
                    self.run_line(line, line_number)
            except ADBProcessTerminatedError:
                print(f"adb process for device {self.log_path} terminated")
            except Exception as e:
                print(f"An error occurred: {e}")

        if not self.realtime_flag:
            for i in self.summary_list:
                if i["name"] in self.child_oracle_name:
                    if i["state"] is NodeState.Ok:
                        i["state"] = NodeState.ChildOk
                    elif i["state"] is NodeState.Error:
                        i["state"] = NodeState.ChildError
                    elif i["state"] is NodeState.Warn:
                        i["state"] = NodeState.ChildWarn

            self.coverage = round(len(set(self.match_line)) / line_number * 100, 1)

            return self.summary_list

        # 实时模式下不保存self.summary_list
        else:
            return None

    def pending(self):
        """ pending """
        pass


if __name__ == "__main__":
    import unittest

    class TestMathOperations(unittest.TestCase):
        """ TestMathOperations """
        def setUp(self):
            self.lo2lang = Lo2IRExecutor()

        def test_lo2_tokens_to_parser_sentence_count(self):
            """ test_lo2_tokens_to_parser_sentence_count """
            self.assertEqual(self.lo2lang.parser_sentence_count(" ==1"), 1)
            self.assertEqual(self.lo2lang.parser_sentence_count(" == 1"), 1)
            self.assertEqual(self.lo2lang.parser_sentence_count(" == 12"), 12)
            self.assertEqual(self.lo2lang.parser_sentence_count("== 8  "), 8)
            with self.assertRaises(SyntaxError) as context:
                self.assertEqual(self.lo2lang.parser_sentence_count("=12"), None)
            self.assertEqual(
                str(context.exception), "Invalid sentence count: =12"
            )

            self.assertEqual(self.lo2lang.parser_sentence_count(">= 8  "), (8, inf))
            self.assertEqual(self.lo2lang.parser_sentence_count("8 <= "), (8, inf))

            self.assertEqual(self.lo2lang.parser_sentence_count("8 >=   "), (-inf, 8))
            self.assertEqual(self.lo2lang.parser_sentence_count("<= 8"), (-inf, 8))

            self.assertEqual(self.lo2lang.parser_sentence_count(" [12, 56 ]"), (12, 56))
            with self.assertRaises(SyntaxError) as context:
                self.assertEqual(
                    self.lo2lang.parser_sentence_count(" [sdf12, 56 ]"), None
                )
            self.assertEqual(
                str(context.exception),
                "Invalid sentence count: [sdf12, 56 ]",
            )

        def test_multiply(self):
            """ test_multiply """
            pass
            """
            self.assertEqual(multiply(2, 3), 6)
            self.assertEqual(multiply(4, 0), 0)
            self.assertEqual(multiply(-1, -1), 1)
            """

    unittest.main()
