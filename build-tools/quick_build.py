#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速构建脚本 - 一键为当前平台创建可执行文件
"""

import os
import sys
import platform
import subprocess
import shutil

def main():
    """快速构建主函数"""
    print("🚀 照片水印工具 - 快速构建")
    print(f"当前平台: {platform.system()} {platform.machine()}")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    # 安装依赖
    print("\n📦 安装依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0"], check=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    
    # 清理旧构建
    print("\n🧹 清理旧构建...")
    for folder in ["dist", "build", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✅ 清理 {folder}")
    
    # 构建可执行文件
    print("\n🔨 构建可执行文件...")
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "build.spec"], check=True)
        print("✅ 构建完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    
    # 检查结果
    exe_name = "PhotoWatermark.exe" if platform.system() == "Windows" else "PhotoWatermark"
    exe_path = os.path.join("dist", exe_name)
    
    if os.path.exists(exe_path):
        print(f"\n🎉 构建成功！")
        print(f"📁 可执行文件: {exe_path}")
        print(f"💡 双击运行即可使用")
        
        # 创建便携版
        print("\n📦 创建便携版...")
        portable_dir = "PhotoWatermark-Portable"
        os.makedirs(portable_dir, exist_ok=True)
        
        # 复制文件
        shutil.copy2(exe_path, portable_dir)
        if os.path.exists("templates.json"):
            shutil.copy2("templates.json", portable_dir)
        if os.path.exists("README.md"):
            shutil.copy2("README.md", portable_dir)
        
        # 创建启动脚本
        if platform.system() == "Windows":
            launcher = os.path.join(portable_dir, "启动程序.bat")
            with open(launcher, "w", encoding="gbk") as f:
                f.write("@echo off\necho 正在启动照片水印工具...\nPhotoWatermark.exe\npause\n")
        else:
            launcher = os.path.join(portable_dir, "启动程序.sh")
            with open(launcher, "w", encoding="utf-8") as f:
                f.write("#!/bin/bash\necho \"正在启动照片水印工具...\"\n./PhotoWatermark\n")
            os.chmod(launcher, 0o755)
        
        print(f"✅ 便携版已创建: {portable_dir}/")
        print(f"💡 可以将整个 {portable_dir} 文件夹复制到其他电脑使用")
        
        return True
    else:
        print(f"❌ 构建失败: 未找到 {exe_path}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎊 快速构建完成！现在可以运行程序了。")
    else:
        print("\n💥 构建失败，请检查错误信息。")
    sys.exit(0 if success else 1)
