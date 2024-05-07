"""
lo2
====
lo2state.py
"""
from enum import Enum

class NodeState(str, Enum):
    """
    NodeState 节点状态
    """
    Ok         = "OK"         # 匹配成功
    Error      = "Error"      # 匹配失败
    Warn       = "Warn"       # 匹配成功 但警告
    Pending    = "Pending"    # 正在匹配中
    NextStart  = "NextStart"  # 当前状态匹配结束 开始下一轮状态匹配
    Idle       = "Idle"       # 正在等待开始匹配
    Finish     = "Finish"     # 匹配结束
    ChildOk    = "ChildOk"    # 作为子oracle匹配成功 且其父oracle已经匹配完毕
    ChildError = "ChildError" # 作为子oracle匹配失败 且其父oracle已经匹配完毕
    ChildWarn  = "ChildWarn"  # 作为子oracle匹配成功但警告 且其父oracle已经匹配完毕

class VariablePatternState(str, Enum):
    """
    VariablePatternState 变量匹配状态
    """
    Access = "Access" # 匹配取值变量中
    Assign = "Assign" # 匹配赋值变量中

class PatternFailReason(str, Enum):
    """
    PatternFailReason 匹配失败原因
    """
    PatternRuleNotMatch   = "PatternRuleNotMatch: " # 匹配规则匹配失败
    NewPatternStart       = "NewPatternStart"       # 当前匹配未结束 但新一次匹配已开始
    WarningPatternSuccess = "WarningPatternSuccess" # 匹配成功但警告

MATCH_TYPE_ERROR = "error"
MATCH_TYPE_WARN = "warn"
MATCH_TYPE_OKAY = "okay"

MATCH_TYPE_MAP = {
    MATCH_TYPE_ERROR: NodeState.Error,
    MATCH_TYPE_WARN: NodeState.Warn,
    MATCH_TYPE_OKAY: NodeState.Ok,
}