#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化构建脚本 - 为Mac和Windows平台创建可执行文件
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def install_dependencies():
    """安装构建依赖"""
    dependencies = [
        "pyinstaller>=5.0",
        "pillow>=10.0.0",
        "tkinter-tooltip>=2.0.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"安装 {dep}"):
            return False
    return True

def create_icon():
    """创建应用图标（如果不存在）"""
    icon_path = "icon.ico" if platform.system() == "Windows" else "icon.icns"
    if not os.path.exists(icon_path):
        print(f"⚠️  未找到图标文件 {icon_path}，将使用默认图标")
        return False
    return True

def build_executable():
    """构建可执行文件"""
    system = platform.system()
    arch = platform.machine()
    
    print(f"\n🏗️  开始构建 {system} {arch} 版本...")
    
    # 清理之前的构建
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # 构建命令
    build_cmd = "pyinstaller build.spec"
    
    if not run_command(build_cmd, "构建可执行文件"):
        return False
    
    # 检查构建结果
    exe_name = "PhotoWatermark.exe" if system == "Windows" else "PhotoWatermark"
    exe_path = os.path.join("dist", exe_name)
    
    if os.path.exists(exe_path):
        print(f"✅ 构建成功: {exe_path}")
        return True
    else:
        print(f"❌ 构建失败: 未找到 {exe_path}")
        return False

def create_release_package():
    """创建发布包"""
    system = platform.system()
    arch = platform.machine()
    
    # 创建发布目录
    release_dir = f"release/PhotoWatermark-{system}-{arch}"
    os.makedirs(release_dir, exist_ok=True)
    
    # 复制可执行文件
    exe_name = "PhotoWatermark.exe" if system == "Windows" else "PhotoWatermark"
    exe_path = os.path.join("dist", exe_name)
    
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_dir)
        print(f"✅ 复制可执行文件到 {release_dir}")
    
    # 复制必要文件
    files_to_copy = ["templates.json", "README.md"]
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"✅ 复制 {file} 到 {release_dir}")
    
    # 创建启动脚本
    if system == "Windows":
        create_windows_launcher(release_dir)
    else:
        create_mac_launcher(release_dir)
    
    print(f"\n🎉 发布包已创建: {release_dir}")
    return True

def create_windows_launcher(release_dir):
    """创建Windows启动脚本"""
    launcher_content = """@echo off
echo 正在启动照片水印工具...
PhotoWatermark.exe
pause
"""
    with open(os.path.join(release_dir, "启动程序.bat"), "w", encoding="gbk") as f:
        f.write(launcher_content)
    print("✅ 创建Windows启动脚本")

def create_mac_launcher(release_dir):
    """创建Mac启动脚本"""
    launcher_content = """#!/bin/bash
echo "正在启动照片水印工具..."
./PhotoWatermark
"""
    launcher_path = os.path.join(release_dir, "启动程序.sh")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # 设置执行权限
    os.chmod(launcher_path, 0o755)
    print("✅ 创建Mac启动脚本")

def main():
    """主函数"""
    print("🚀 照片水印工具 - 自动化构建脚本")
    print(f"当前平台: {platform.system()} {platform.machine()}")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败")
        return False
    
    # 创建图标（可选）
    create_icon()
    
    # 构建可执行文件
    if not build_executable():
        print("❌ 构建失败")
        return False
    
    # 创建发布包
    if not create_release_package():
        print("❌ 创建发布包失败")
        return False
    
    print("\n🎉 构建完成！")
    print("📁 发布文件位于 release/ 目录")
    print("💡 可以将整个发布目录打包成ZIP文件分发给用户")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
