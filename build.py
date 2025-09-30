#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本 - 创建可执行文件
"""

import os
import sys
import subprocess
import shutil
import platform

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller安装失败: {e}")
        return False

def build_executable():
    """构建可执行文件"""
    system = platform.system().lower()
    # 使用 os.pathsep 獲取跨平台的正確分隔符
    separator = os.pathsep 
    # 基本命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 单文件模式
        # "--windowed",  # 注释掉避免macOS问题
        "--name=PhotoWatermark",  # 可执行文件名
        f"--add-data=requirements.txt{separator}.",  # 包含requirements.txt
        "main.py"
    ]
    
    # 不包含图标，避免文件不存在错误
    
    try:
        print("开始构建可执行文件...")
        subprocess.check_call(cmd)
        print("构建成功！")
        
        # 移动可执行文件到根目录
        dist_dir = "dist"
        if os.path.exists(dist_dir):
            exe_name = "PhotoWatermark.exe" if system == "windows" else "PhotoWatermark"
            exe_path = os.path.join(dist_dir, exe_name)
            
            if os.path.exists(exe_path):
                shutil.move(exe_path, exe_name)
                print(f"可执行文件已创建: {exe_name}")
                
                # 清理临时文件
                if os.path.exists("build"):
                    shutil.rmtree("build")
                if os.path.exists("dist"):
                    shutil.rmtree("dist")
                if os.path.exists("PhotoWatermark.spec"):
                    os.remove("PhotoWatermark.spec")
                
                return True
        
        print("构建失败：未找到可执行文件")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def create_release_package():
    """创建发布包"""
    print("创建发布包...")
    
    # 创建发布目录
    release_dir = "PhotoWatermark_Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制必要文件
    files_to_copy = [
        "PhotoWatermark.exe" if platform.system().lower() == "windows" else "PhotoWatermark",
        "使用说明.md",
        "README.md",
        "requirements.txt"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"已复制: {file}")
    
    # 创建启动脚本
    if platform.system().lower() == "windows":
        with open(os.path.join(release_dir, "启动程序.bat"), "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("PhotoWatermark.exe\n")
            f.write("pause\n")
    else:
        with open(os.path.join(release_dir, "启动程序.sh"), "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n")
            f.write("./PhotoWatermark\n")
        os.chmod(os.path.join(release_dir, "启动程序.sh"), 0o755)
    
    print(f"发布包已创建: {release_dir}/")
    return True

def main():
    print("照片水印工具 - 构建脚本")
    print("=" * 40)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    print(f"Python版本: {sys.version}")
    print(f"操作系统: {platform.system()} {platform.release()}")
    
    # 安装PyInstaller
    if not install_pyinstaller():
        print("无法安装PyInstaller，请手动安装: pip install pyinstaller")
        sys.exit(1)
    
    # 构建可执行文件
    if not build_executable():
        print("构建失败")
        sys.exit(1)
    
    # 创建发布包
    if not create_release_package():
        print("创建发布包失败")
        sys.exit(1)
    
    print("\n构建完成！")
    print("可执行文件已创建，可以分发给其他用户使用。")

if __name__ == "__main__":
    main()
