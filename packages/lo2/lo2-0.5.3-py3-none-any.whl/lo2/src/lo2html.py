"""
lo2
====
lo2html.py
"""
import jinja2
import os

# from  numpy import inf
from .lo2parser import NodeState


def create_directory(directory_path):
    """
    创建指定路径的目录，如果该目录已存在，则不进行任何操作。
    
    Args:
        directory_path (str): 要创建的目录路径。
    
    Returns:
        None
    
    """
    # 判断目录是否存在
    if not os.path.exists(directory_path):
        # 如果不存在，则创建目录
        os.makedirs(directory_path)
        print(f"目录 {directory_path} 创建成功")
    else:
        print(f"目录 {directory_path} 已存在")


class MVC:
    """
    generate html with MVC
    """
    def __init__(self):
        """
        初始化方法，用于创建一个新的视图对象。
        """
        self.data = {}
        self._view = {}

    def model(self, data):
        """
        将数据保存到模型中，并返回模型对象本身。
        
        Args:
            data: 需要保存到模型中的数据。
        
        Returns:
            返回模型对象本身，以便进行链式操作。
        
        """
        self.data = data
        return self

    def _to_overview(self):
        """
        将当前对象中的data属性存储到self._view字典的"overview"键中。
        """
        self._view["overview"] = self.data

    def _to_timeline(self):
        """
        将当前视图的数据存储到时间线中。
        """
        self._view["timeline"] = self.data

    def to_controller(self, view_type):
        """
        timeline
        overview
        """
        if view_type == "timeline":
            self._to_timeline()
        elif view_type == "overview":
            self._to_overview()
        return self

    # get this file directory
    def _get_path(self):
        """
        获取当前文件所在的目录路径。
        Returns:
            str: 当前文件所在的目录路径。
        
        """
        return os.path.dirname(os.path.realpath(__file__))

    # 获取path2相对于path1的相对路径
    def _get_relative_path(self, path1, path2):
        """
        获取两个文件路径之间的相对路径。
        
        Args:
            path1 (str): 起始文件路径。
            path2 (str): 目标文件路径。
        
        Returns:
            str: 起始路径到目标路径的相对路径。
        
        """
        return os.path.relpath(path2, path1)

    def _to_index_html(self, path):
        """
        将页面转换为静态的 HTML 文件
        
        Args:
            path (str): 目标路径
        """
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        # 从path相对路径获取模板
        temp = env.get_template(
            self._get_relative_path(
                path, f"{self._get_path()}/template/statics/index.html"
            )
        )
        out_dir = os.path.join(path, "html-out")
        create_directory(out_dir)

        out = temp.render(views=self._view.keys())
        with open(
            os.path.join(path, out_dir, f"index.html"), "w", encoding="utf-8"
        ) as f:
            f.writelines(out)
            f.close()

    def _result_to_overview_html(self, result, path):
        """
        将结果转化为HTML格式并保存到指定路径
        
        Args:
            result: 结果对象，包含需要展示的信息
            path: 保存HTML文件的路径  
        """
        pass

    def _result_to_timeline_html(self, result, path):
        """
        将结果转换为timeline的html文件
        Args:
            result: 结果数据
            path: 存放结果的路径
        """
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        # 从path相对路径获取模板
        temp = env.get_template(
            self._get_relative_path(
                path, f"{self._get_path()}/template/statics/timeline.html"
            )
        )

        out_dir = os.path.join(path, "html-out")

        create_directory(out_dir)
        out = temp.render(**self._view["timeline"])
        with open(
            os.path.join(path, out_dir, f"timeline.html"), "w", encoding="utf-8"
        ) as f:
            f.writelines(out)
            f.close()

    def _resource_copy(self, path):
        """
        复制静态资源到指定路径
        
        Args:
            path (str): 目标路径
        """
        # 复制静态资源
        static_dir = os.path.join(path, "html-out")
        create_directory(static_dir)
        # 复制 png 图片到 static_dir
        for file in os.listdir(os.path.join(self._get_path(), "template", "statics")):
            if file.endswith(".png"):
                os.system(
                    f"cp -r {self._get_path()}/template/statics/{file} {static_dir}"
                )

    def to_html(self, outdir="./"):
        """
        将报告转换成 HTML 文件并保存到指定目录。
        
        Args:
            outdir (str): 保存 HTML 文件的目录，默认为当前目录。
        
        Returns:
            self: 返回对象本身。
        """
        print(self._view.keys())
        for k, v in self._view.items():
            if k == "timeline":
                self._result_to_timeline_html(v, outdir)
            elif k == "overview":
                self._result_to_overview_html(v, outdir)

        self._to_index_html(outdir)
        self._resource_copy(outdir)
        return self
