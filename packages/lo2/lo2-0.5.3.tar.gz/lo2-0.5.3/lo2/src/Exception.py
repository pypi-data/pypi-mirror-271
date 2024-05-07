"""
lo2
====
Exception.py
"""
ANSI_RED = "\033[1;31m"
ANSI_YELLOW = "\033[0;33m"
ANSI_GREEN = "\033[0;32m"
ANSI_NORMAL = "\033[0m"


def __color_warp__(color, text):
    return f"{color}{text}{ANSI_NORMAL}"


class SyntaxError(Exception):
    """
    语法错误 Exceptions
    """
    def __init__(self, message=""):
        """
        初始化一个自定义异常对象
        获取当前调用位置的文件名和行号
        
        Args:
            message (str, optional): 异常信息. Defaults to "".
        """
        try:
            raise Exception
        except Exception as e:
            frame = e.__traceback__.tb_frame.f_back

        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno

        self.message = __color_warp__(ANSI_RED, f" {message}\n")
        self.message += "File: " + __color_warp__(
            ANSI_RED, f"{file_name}:{line_number}"
        )
        super().__init__(self.message)

    def __str__(self):
        print("-" * 20)
        return self.message


class RuntimeError(Exception):
    """
    RuntimeError Exception
    """
    def __init__(self, message=""):
        """
        初始化函数，用于生成带有文件名和行号的异常信息
        
        Args:
            message (str, optional): 异常信息。默认为空字符串。
        """
        try:
            raise Exception
        except Exception as e:
            frame = e.__traceback__.tb_frame.f_back

        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno

        self.message = __color_warp__(ANSI_RED, f" {message}\n")
        self.message += "File: " + __color_warp__(
            ANSI_RED, f"{file_name}:{line_number}"
        )
        super().__init__(self.message)

    def __str__(self):
        """
        返回对象的字符串表示形式，包括一条由20个减号组成的分隔线和消息内容。
        
        Returns:
            str: 对象的字符串表示形式，包括一条由20个减号组成的分隔线和消息内容。
        
        """
        print("-" * 20)
        return self.message
