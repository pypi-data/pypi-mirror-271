"""
lo2
====
lo2-lang front end
"""
import ply.yacc as yacc
import ply.lex as lex

import os
import copy
import json

ANSI_RED = "\033[1;31m"
ANSI_YELLOW = "\033[0;33m"
ANSI_GREEN = "\033[0;32m"
ANSI_NORMAL = "\033[0m"


def __color_warp__(color, text):
    """
    将文本添加颜色
    
    Args:
        color (str): 文本颜色
        text (str): 要添加颜色的文本
    
    Returns:
        str: 添加颜色后的文本
    
    """
    return f"{color}{text}{ANSI_NORMAL}"


class SyntaxError(Exception):
    """
    语法错误 Exception
    """
    def __init__(self, message="", file_name="", line_number=0):
        try:
            raise Exception
        except Exception as e:
            frame = e.__traceback__.tb_frame.f_back

        self.message = __color_warp__(ANSI_RED, f" {message}\n")
        self.message += "File: " + __color_warp__(
            ANSI_RED, f"{file_name}:{line_number}"
        )
        super().__init__(self.message)


class Lo2Lexer:
    """
    lo2-lang 词法分析器
    """
    def __init__(self):
        """定义词法分析器"""
        self.tokens = [
            "ID",
            "EQUALS",
            "NUMBER",
            "STRING",
            "RSTRING",  # regex 字符串
            "FSTRING",  # format 字符串
            "LESS_THAN",
            "GREAT_THAN",
            "BEGIN",
            "END",
            "NO",
            "STRICT",
            "LBRACE",
            "RBRACE",
            "LPAREN",
            "RPAREN",
            "OR",
            "AND",
            "MATCH",
            "MACRO",
            "REF",
            "MATE",
            "LET",
            "LETM",
            "VAR",
            "TYPE_NUM",
            "TYPE_STR",
            "ASSIGN",
            "IMPORT",
            "AS",
            "NEWLINE",
        ]

        self.t_ignore = " \t"

    def t_OR(self, t):
        r"or[^\S]"
        return t

    def t_AND(self, t):
        r"and[^\S]"
        return t

    def t_IMPORT(self, t):
        r"import\s"
        return t

    def t_AS(self, t):
        r"as[^\S]"
        return t

    def t_ASSIGN(self, t):
        r"=[^=]"
        return t

    def t_TYPE_NUM(self, t):
        r"num[^\S]"
        return t

    def t_TYPE_STR(self, t):
        r"str[^\S]"
        return t

    def t_LET(self, t):
        r"let[^\S]"
        return t

    def t_LETM(self, t):
        r"letm[^\S]"
        return t

    def t_VAR(self, t):
        r"var[^\S]"
        return t

    def t_MATE(self, t):
        r"@[a-zA-Z_][a-zA-Z0-9_]*"
        return t

    def t_EQUALS(self, t):
        r"==[^=]"
        return t

    def t_LESS_THAN(self, t):
        r"<="
        return t

    def t_GREAT_THAN(self, t):
        r">="
        return t

    def t_LBRACE(self, t):
        r"{"
        return t

    def t_RBRACE(self, t):
        r"}"
        return t

    def t_LPAREN(self, t):
        r"\("
        return t

    def t_RPAREN(self, t):
        r"\)"
        return t

    def t_NO(self, t):
        r"no\s"
        return t

    def t_BEGIN(self, t):
        r"begin\s"
        return t

    def t_STRICT(self, t):
        r"strict\s"
        return t

    def t_REF(self, t):
        r"ref\s"
        return t

    def t_END(self, t):
        r"end\s"
        return t

    def t_MATCH(self, t):
        r"match\s"
        return t

    def t_MACRO(self, t):
        r"macro\s"
        return t

    def t_NUMBER(self, t):
        r"\.?\d+\.?\d*"
        try:
            t.value = int(t.value)
        except:
            # maybe a float
            t.value = float(t.value)
        return t

    def t_STRING(self, t):
        r"(?<!rf)\".*?\""
        t.value = "$S$" + t.value[1:-1]  # 去掉引号
        return t

    def t_RSTRING(self, t):
        r"r\".*?\""
        t.value = "$R$" + t.value[2:-1]  # 去掉引号
        return t

    def t_FSTRING(self, t):
        r"f\".*?\" "
        t.value = "$F$" + t.value[2:-1]  # 去掉引号
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9.]*"
        return t

    def t_COMMENT(self, t):
        r"\#.*"
        pass

    def t_error(self, t):
        """ 当词法分析器遇到无法识别的字符时，调用该函数 """
        # print(f"无法识别的字符：{t.value[0:5]}, {t.value[0]}")
        t.lexer.skip(1)

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def build(self, **kwargs):
        """
        构建词法分析器。

        Args:
            **kwargs: 传递给词法分析器构建函数的参数。

        Returns:
            None
        """
        self.lexer = lex.lex(module=self, **kwargs)


# 代码生成器
class Lo2Yaccer:
    """
    Lo2Yaccer 上下文无关文法
    """
    def __init__(self, lexer):
        self.tokens = lexer.tokens
        self.lexer = lexer.lexer
        self.parser = yacc.yacc(module=self, start="full_input")
        self.sub_condition = [["strict"], ["begin"], ["end"]]
        self.file_name = ""

    def p_full_input(self, p):
        """full_input : content_list"""
        p[0] = p[1]

    def p_content_list(self, p):
        """content_list : content
        | content_list content
        """
        p[0] = p[1]

    def p_content(self, p):
        """content : namespace_list
        | match_macro_list
        | declaration_list
        | content match_macro_list
        | content namespace_list
        | content declaration_list
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = {**p[1], **p[2]}

    def p_namespace_list(self, p):
        """namespace_list : namespace
        | namespace_list namespace
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = {**p[1], **p[2]}

    def p_namespace(self, p):
        "namespace : ID LBRACE content RBRACE"
        p[0] = {p[1]: p[3]}

    def p_match_macro_list(self, p):
        """match_macro_list : macro
        | match
        | strict_macro
        | strict_match
        | match_macro_list macro
        | match_macro_list match
        | match_macro_list strict_macro
        | match_macro_list strict_match
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {**p[1], **p[2]}

    def p_string(self, p):
        """string : STRING
        | RSTRING
        | FSTRING
        """
        p[0] = p[1]

    def p_string_tuple_items(self, p):
        """string_tuple_items : string
        | string_tuple_items OR string
        | string_tuple_items OR string_tuple
        | string_tuple_items AND string
        | string_tuple_items AND string_tuple
        | string_tuple
        """
        if len(p) == 2:
            p[0] = [p[1], ]
        elif len(p) == 4:
            if p[2].strip() == "or":
                p[0] = p[1] + ['$OR$', p[3]]
            elif p[2].strip() == "and":
                p[0] = p[1] + ['$AND$', p[3]]

    def p_string_tuple(self, p):
        """string_tuple : string
        | LPAREN string_tuple_items RPAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]

    def p_declaration_list(self, p):
        """declaration_list : declaration
        | declaration_list declaration
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {**p[1], **p[2]}

    def p_declaration(self, p):
        """declaration : mate
        | variable
        | import
        """
        p[0] = p[1]

    def p_import(self, p):
        """import : IMPORT ID AS ID
        | IMPORT ID
        """
        if len(p) == 3:
            p[0] = {f"$IMPORT${p[2]}": None}
        elif len(p) == 5:
            p[0] = {f"$IMPORT${p[2]}": p[4]}

    def p_variable(self, p):
        """variable : variable_1
        | variable_1 mate
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            # 这里p[1]字典只有1个key，将注解添加到变量的信息里。
            label = list(p[1].keys())[0]
            p[1][label].update(p[2])
            p[0] = p[1]

    def p_variable_1(self, p):
        """variable_1 : LET ID TYPE_NUM
        | LET ID TYPE_NUM ASSIGN NUMBER
        | LETM ID TYPE_NUM
        | LETM ID TYPE_NUM ASSIGN NUMBER
        | LET ID TYPE_STR
        | LET ID TYPE_STR ASSIGN string
        | LETM ID TYPE_STR
        | LETM ID TYPE_STR ASSIGN string
        | VAR ID TYPE_STR
        | VAR ID TYPE_STR ASSIGN string
        | VAR ID TYPE_NUM
        | VAR ID TYPE_NUM ASSIGN NUMBER
        """
        scope_type = "$VAR$" if "var" in p[1] else "$LET$"
        label = f"{scope_type}.{p[2]}"
        null = "$undefined$" if "str" in p[3] else float('inf')

        if len(p) == 4:
            p[0] = {label: {"type": p[3].strip(), "init_value": null}}
        elif len(p) == 6:
            val = p[5][3:] if "str" in p[3] else p[5]
            p[0] = {label: {"type": p[3].strip(), "init_value": val}}

        p[0][label]["monitor"] = "letm" in p[1]
        p[0][label]["global"] = "$VAR$" not in scope_type

    def p_mate(self, p):
        """mate : MATE
        | MATE string
        """
        if len(p) == 2:
            p[0] = {p[1]: True}
        elif len(p) == 3:
            p[0] = {p[1]: p[2][3:]}  # remove the string prefix

    def p_macro(self, p):
        """macro : MACRO ID LBRACE oracle RBRACE
        | MACRO ID LBRACE declaration_list oracle RBRACE
        """
        if len(p) == 6:
            p[0] = {f"{p[2]}$MACRO$": {"oracle": p[4]}}
        elif len(p) == 7:
            # add the only mate data
            p[0] = {f"{p[2]}$MACRO$": {**p[4], "oracle": p[5]}}

    def p_strict_macro(self, p):
        """strict_macro : STRICT MACRO ID LBRACE oracle RBRACE
        | STRICT MACRO ID LBRACE declaration_list oracle RBRACE
        """
        if len(p) == 7:
            p[0] = {f"{p[3]}$MACRO$$STRICT$": {"oracle": p[5]}}
        elif len(p) == 8:
            p[0] = {f"{p[3]}$MACRO$$STRICT$": {**p[5], "oracle": p[6]}}

    def p_match(self, p):
        """match : MATCH ID LBRACE oracle RBRACE
        | MATCH ID LBRACE declaration_list oracle RBRACE
        """
        if len(p) == 6:
            p[0] = {p[2]: {"oracle": p[4]}}
        elif len(p) == 7:
            # add the only mate data
            p[0] = {p[2]: {**p[4], "oracle": p[5]}}

    def p_strict_match(self, p):
        """strict_match : STRICT MATCH ID LBRACE oracle RBRACE
        | STRICT MATCH ID LBRACE declaration_list oracle RBRACE"""
        if len(p) == 7:
            p[0] = {f"{p[3]}$STRICT$": {"oracle": p[5]}}
        elif len(p) == 8:
            p[0] = {f"{p[3]}$STRICT$": {**p[5], "oracle": p[6]}}

    def p_oracle(self, p):
        """oracle : condition_list"""
        p[0] = p[1]

    def p_condition_list(self, p):
        """condition_list : condition_list condition
        | condition
        """
        if len(p) == 2:
            if len(p[1]) == 2 and p[1][1] in self.sub_condition:
                p[0] = p[1]
            else:
                p[0] = [p[1], ["$EMPTY_COND$"]]
        elif len(p) == 3:
            if len(p[2]) == 2 and p[2][1] in self.sub_condition:
                p[0] = p[1] + p[2]
            else:
                p[0] = p[1] + [p[2], ["$EMPTY_COND$"]]

    def p_condition(self, p):
        """condition : num_string_condition
        | string_num_condition
        | num_string_num_lt_condition
        | num_string_num_gt_condition
        | no_string_condition
        | strict
        | end_condition
        | begin_condition
        | strict_condition
        | only_string_condition
        | only_ref_condition
        """
        p[0] = p[1]

    def p_begin_condition(self, p):
        """begin_condition : BEGIN  condition"""
        p[0] = [p[2], [p[1].strip()]]

    def p_end_condition(self, p):
        """end_condition : END condition"""
        p[0] = [p[2], [p[1].strip()]]

    def p_strict_condition(self, p):
        """strict_condition : STRICT condition"""
        p[0] = [p[2], [p[1].strip()]]

    def p_no_string_condition(self, p):
        """no_string_condition : NO string_tuple
        | NO REF ID
        """
        if len(p) == 3:
            p[0] = ["not", "==1", p[2]]
        elif len(p) == 4:
            p[0] = ["not", "==1", {"ref": f"{p[3]}"}]

    def p_strict(self, p):
        """strict : STRICT"""
        p[0] = [p[1]]

    def p_only_string_condition(self, p):
        "only_string_condition : string_tuple"
        p[0] = ["is", "==1", p[1]]

    def p_only_ref_condition(self, p):
        "only_ref_condition : REF ID"
        p[0] = ["is", "==1", {"ref": f"{p[2]}"}]

    def p_num_string_condition(self, p):
        """num_string_condition : NUMBER EQUALS string_tuple
        | NUMBER LESS_THAN string_tuple
        | NUMBER GREAT_THAN string_tuple
        | NUMBER EQUALS REF ID
        | NUMBER LESS_THAN REF ID
        | NUMBER GREAT_THAN REF ID
        """

        reversed_op = {"<=": ">=", ">=": "<="}
        if p[2] in reversed_op:
            p[2] = reversed_op[p[2]]

        if len(p) == 4:
            p[0] = ["is", f"{p[2]}{p[1]}", p[3]]
        elif len(p) == 5:
            p[0] = ["is", f"{p[2]}{p[1]}", {"ref": f"{p[4]}"}]

    def p_string_num_condition(self, p):
        """string_num_condition : string_tuple EQUALS NUMBER
        | string_tuple LESS_THAN NUMBER
        | string_tuple GREAT_THAN NUMBER
        | REF ID EQUALS NUMBER
        | REF ID LESS_THAN NUMBER
        | REF ID GREAT_THAN NUMBER
        """
        if len(p) == 4:
            p[0] = ["is", f"{p[2]}{p[3]}", p[1]]
        elif len(p) == 5:
            p[0] = ["is", f"{p[3]}{p[4]}", {"ref": f"{p[2]}"}]

    def p_num_string_num_lt_condition(self, p):
        """num_string_num_lt_condition :  NUMBER LESS_THAN string_tuple LESS_THAN NUMBER
        | NUMBER LESS_THAN REF ID LESS_THAN NUMBER
        """
        if len(p) == 6:
            p[0] = ["is", f"[{p[1]}, {p[5]}]", p[3]]
        elif len(p) == 7:
            p[0] = ["is", f"[{p[1]}, {p[6]}]", {"ref": f"{p[4]}"}]

    def p_num_string_num_gt_condition(self, p):
        """num_string_num_gt_condition :  NUMBER GREAT_THAN string_tuple GREAT_THAN NUMBER
        | NUMBER GREAT_THAN REF ID GREAT_THAN NUMBER
        """
        if len(p) == 6:
            p[0] = ["is", f"[{p[5]}, {p[1]}]", p[3]]
        elif len(p) == 7:
            p[0] = ["is", f"[{p[6]}, {p[1]}]", p[4]]

    def p_error(self, p):
        """ 语法错误 """
        if p:
            raise SyntaxError(f"Syntax error at token {p.type}, value: {p.value}",
                            self.file_name, line_number=f"{p.lineno}")
        else:
            raise SyntaxError("Syntax error at EOF")

    def parse(self, lo2_code):
        """ 语法解析入口 """
        result = self.parser.parse(lo2_code, lexer=self.lexer, debug=False)
        # if not result:
        #    raise Exception("Syntax error!")
        return result


# 后处理器，用于处理代码生成器生成的语法树
class Lo2PostProcessor:
    """
    在AST上做上下文有关语法处理
    """
    # 处理宏替换
    def __init__(self, lo2_js) -> None:
        self.lo2_js = lo2_js
        self.variables_collect = {}

    def __find_ref(self, match_name):
        """
        查找引用对象
        """
        oracle = self.lo2_js
        try:
            for e in match_name:
                oracle = oracle[e]
            return oracle["oracle"]
        except:
            return None

    def __recursion_process_macro(self, node):
        if not isinstance(node, dict):
            return

        for k, v in node.items():
            if isinstance(v, dict):
                if "oracle" in v:
                    for idx, cmd in enumerate(v["oracle"]):
                        # 奇数行，附加条件行
                        if idx % 2 == 0 and len(cmd) == 3:
                            if isinstance(cmd[2], dict) and "ref" in cmd[2]:
                                ref_name = f'root.{cmd[2]["ref"]}'
                                split_name = ref_name.split(".")

                                ref_oracles = self.__find_ref(split_name)
                                if not ref_oracles:
                                    split_name[-1] = f"{split_name[-1]}$MACRO$"
                                    ref_oracles = self.__find_ref(split_name)

                                if not ref_oracles:
                                    raise Exception(f"ref {ref_name} not found")
                                # attach the ref name to the head of oracle
                                v["oracle"][idx][2] = [ref_name] + ref_oracles
                else:
                    self.__recursion_process_macro(node[k])

    def process_macro(self):
        """ 递归处理宏，将宏引用替换为实际内容"""
        for k, v in self.lo2_js.items():
            if isinstance(v, dict):
                self.__recursion_process_macro(v)

    def __recursion_process_strict(self, node):
        if not isinstance(node, dict):
            return

        for k, v in node.items():
            if isinstance(v, dict):
                if "oracle" in v and "$STRICT$" in k:
                    for idx, cmd in enumerate(v["oracle"]):
                        # 奇数行，附加条件行
                        if idx % 2 == 1 and cmd == ["$EMPTY_COND$"]:
                            v["oracle"][idx] = ["strict"]
                else:
                    self.__recursion_process_strict(node[k])

    def process_strict(self):
        """
        递归处理strict块，将strict块中，附加条件为"$EMPTY_COND$"的行，替换为"strict"
        """
        for k, v in self.lo2_js.items():
            if isinstance(v, dict):
                self.__recursion_process_strict(v)

    def __recursion_and_or_stat(self, str_list, expr, newcmd):
        """
        将and or块，转换为if块
        """
        replace = {"$OR$": "or ", "$AND$": "and "}
        for i, e in enumerate(str_list):
            if isinstance(e, list):
                expr += "( "
                expr = self.__recursion_and_or_stat(e, expr, newcmd)
                expr += ") "
            elif i % 2 == 1:
                if e in replace:
                    expr += replace[e]
                else:
                    raise SyntaxError(f"got a unexcept symbol: {e}")
            else:
                expr += "# "
                newcmd.append(e)
        return expr

    def __recursion_process_and_or_stat(self, node):
        if not isinstance(node, dict):
            return

        for k, v in node.items():
            if isinstance(v, dict):
                if "oracle" in v:
                    for idx, cmd in enumerate(v["oracle"]):
                        if idx % 2 == 0 and len(cmd) == 3 and isinstance(cmd[2], list):
                            newcmd = []
                            expr = self.__recursion_and_or_stat(cmd[2], "(", newcmd)
                            expr += ")"
                            newcmd.insert(0, expr)
                            cmd[2] = newcmd
                else:
                    self.__recursion_process_and_or_stat(node[k])

    def process_and_or_stat(self):
        """
        递归处理and or块"
        """
        for k, v in self.lo2_js.items():
            if isinstance(v, dict):
                self.__recursion_process_and_or_stat(v)

    def __recursion_collect_let_variable(self, prev_k, node, marks=["$LET$", "$VAR$"]):
        if not isinstance(node, dict):
            return

        for k, v in node.items():
            if isinstance(v, dict):
                for mark in marks:
                    if len(k) > len(mark) and mark == k[:5]:
                        var_name = k.replace(mark, prev_k)
                        if var_name in self.variables_collect:
                            raise Exception(f"redefine {var_name}.")
                        self.variables_collect[var_name] = v
                self.__recursion_collect_let_variable(f"{prev_k}.{k}", node[k])

    def process_collect_variable(self):
        """
        递归处理let variable，将$LET$声明变量，添加变量pool
        """
        for k, v in self.lo2_js.items():
            if isinstance(v, dict):
                self.__recursion_collect_let_variable(k, v)

    def recursion_mask_suffixs(self, dictionary, suffixs):
        """ 递归处理字典，将字典中包含suffixs的键，替换为去掉suffixs后的键"""
        keys_to_remove = []  # 存储要删除的键
        keys_to_update = {}  # 存储要更新的键值对

        for key, value in dictionary.items():
            # 如果键包含"$XX$"
            update = False
            new_key = key
            for suffix in suffixs:
                if suffix in new_key:
                    # 删除"$XX$"
                    new_key = new_key.replace(suffix, "")
                    update = True

            if update:
                keys_to_remove.append(key)
                keys_to_update[new_key] = value

            # 如果值是字典类型，递归调用
            if isinstance(value, dict):
                self.recursion_mask_suffixs(value, suffixs=suffixs)

        # 删除和更新字典
        for key in keys_to_remove:
            dictionary.pop(key)
        dictionary.update(keys_to_update)

    def process(self):
        """ 处理入口"""
        self.process_strict()
        self.recursion_mask_suffixs(self.lo2_js, ["$STRICT$"])
        self.process_and_or_stat()
        self.process_collect_variable()
        self.process_macro()
        return self.lo2_js, self.variables_collect

class Linker:
    """
    linker: 链接器，将多个通过import关键字关联的lo2文件合并为一个lo2文件
    """
    def __init__(self, root_code, work_dir="./"):
        self.lo2_code = root_code
        self.lo2_js = {"root": {}}
        self.variables_collect = None
        self.work_dir = work_dir
        self.lo2_fn_dir = work_dir

        self.find_dirs = [self.work_dir]

        if root_code.endswith(".lo2"):
            self.lo2_fn = os.path.basename(root_code)
            if os.path.isabs(self.lo2_code):
                self.lo2_fn_dir = os.path.dirname(self.lo2_code)
            else:
                self.lo2_fn_dir = os.path.join(self.work_dir, os.path.dirname(root_code))
            self.find_dirs.append(self.lo2_fn_dir)

    def find_lo2(self, fn):
        """work_dir and fn merges to a absolute path"""
        for e in self.find_dirs:
            abs_fn = os.path.join(e, fn)
            if os.path.exists(abs_fn):
                return abs_fn
        raise Exception(f"file not found: {fn}")

    def link(self):
        """ link: 链接入口"""
        lo2_js = self._lo2file_to_ast(self.lo2_code)
        self.lo2_js["root"] = copy.deepcopy(lo2_js)
        root = self.lo2_js["root"]

        for k, v in lo2_js.items():
            if "$IMPORT$" in k:
                module = k
                fn = alias = module.replace("$IMPORT$", "")
                if v:
                    alias = v
                abs_fn = self.find_lo2(f"{fn}.lo2")
                root[alias] = {}
                self._recursion_link(abs_fn, root[alias])
            else:
                root[k] = v
        return self.lo2_js

    def _recursion_link(self, lo2_code, prenode):
        lo2_js = self._lo2file_to_ast(lo2_code)

        independent_lo2_js = copy.deepcopy(lo2_js)
        for k, v in independent_lo2_js.items():
            if "$IMPORT$" in k:
                module = k
                fn = alias = module.replace("$IMPORT$", "")
                if v:
                    alias = v
                abs_fn = self.find_lo2(f"{fn}.lo2")
                prenode[alias] = {}
                self._recursion_link(abs_fn, prenode[alias])
            else:
                prenode[k] = v

    def _lo2file_to_ast(self, lo2_code):
        lexer_instance = Lo2Lexer()
        lexer_instance.build()
        parser_instance = Lo2Yaccer(lexer_instance)

        if lo2_code.endswith(".lo2"):
            with open(lo2_code, "r", encoding='utf-8') as f:
                lo2code = f.read()
                parser_instance.file_name = lo2_code
                lo2_js = parser_instance.parse(lo2code)
        else:
            lo2code = lo2_code
            lo2_js = parser_instance.parse(lo2code)

        return lo2_js

def to_ast(lo2_code):
    """
    将lo2代码转化为ast"""
    work_dir = os.getcwd()
    lo2_js = Linker(root_code=lo2_code, work_dir=work_dir).link()
    with open(f"{lo2_code}.json", "w") as f:
        json.dump(lo2_js, f)
    return Lo2PostProcessor(lo2_js).process()



if __name__ == "__main__":
    # 测试字符串
    input_str = """
    custom_namespace {
        custom_sub_namespace {
            match custom_match {
                12 <= "losdf2" <= 89
                "123" == 14
                no "l2o2"
            }
            
            macro custom_match2 {
                begin no "lo2"
                no "l2o2"
                strict
                "yess ok" <= 10
                end 80 <= "oo" <= 90
            }
        }
        
        custom_sub_namespace2 {
            strict match custom_match2 {
                12 <= "losdf2" <= 89
            }
            
            macro custom_match3 {
                12 <= "losdf2" <= 89
            }
        }

        macro custom_match3 {
            12 <= "losdf2" <= 89
        }
        
        match custom_match3 {
            12 <= "losdf2" <= 89
        }
        
        custom_sub_namespace3 {
            match custom_match2 {
                begin 12 <= "losdf2" <= 89
                "ooook" <= 100
                "ooook" <= 1002
                end no "l2o2"
            }
        }
    }
    """
    import sys
    import os
    import json

    # 用 os.path 判断文件是否存在
    if os.path.exists(sys.argv[1]):
        result, vars = to_ast(sys.argv[1])
    else:
        result, vars = to_ast(input_str)
    formatted_json = json.dumps(result, indent=4)
    print(formatted_json)
    formatted_json = json.dumps(vars, indent=4)
    print(formatted_json)
