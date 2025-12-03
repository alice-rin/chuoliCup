import sys
import os
from cx_Freeze import setup, Executable
import shutil

# 先清理现有构建目录
def clean_build_dirs():
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"已删除目录: {dir_name}")
            except Exception as e:
                print(f"删除目录 {dir_name} 失败: {e}")

# 执行清理
clean_build_dirs()

# 构建选项
build_exe_options = {
    "packages": [
        "os", "sys", "json", "math", "random", "enum",
        "pandas", "numpy", "flask", "werkzeug", "configparser",
        "logging", "typing", "re", "datetime", "time", "io",
        "urllib", "shutil", "http", "sys"
    ],
    "includes": [
        "BasicDataStruct", "BasicFuncClass", "Chromosome",
        "GA_Algorithm", "Node", "ScenarioGenerator"
    ],
    "include_files": [
        "config.ini",
        "templates/",
        "uploads/"
    ],
    "excludes": [
        "tkinter", "test", "unittest", "email", "http",
        "xml", "pydoc", "pdb", "curses", "multiprocessing"
    ],
    "path": sys.path + ["."],
    "optimize": 2,
    "silent": True  # 减少输出信息
}

# 应用程序入口点
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="FirePlanningSystem",
        # icon="icon.ico"  # 暂时注释掉图标，避免文件不存在的问题
    )
]

setup(
    name="火力规划系统",
    version="1.0.0",
    description="基于遗传算法的火力规划系统",
    options={"build_exe": build_exe_options},
    executables=executables
)