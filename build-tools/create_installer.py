#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装包制作脚本 - 为Mac和Windows创建专业的安装包
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
from pathlib import Path

def create_windows_installer():
    """创建Windows安装包"""
    print("🪟 创建Windows安装包...")
    
    # 检查是否有NSIS
    try:
        subprocess.run(["makensis", "/VERSION"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到NSIS，请安装NSIS来创建Windows安装包")
        print("下载地址: https://nsis.sourceforge.io/Download")
        return False
    
    # 创建NSIS脚本
    nsis_script = """
!define APPNAME "照片水印工具"
!define COMPANYNAME "Photo Watermark Tool"
!define DESCRIPTION "一个功能强大的照片水印添加工具"
!define VERSIONMAJOR 2
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/yourusername/Photo-Watermark-2"
!define UPDATEURL "https://github.com/yourusername/Photo-Watermark-2"
!define ABOUTURL "https://github.com/yourusername/Photo-Watermark-2"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "PhotoWatermark-Setup.exe"

!include LogicLib.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "需要管理员权限来安装此程序"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file "PhotoWatermark.exe"
    file "templates.json"
    file "README.md"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\PhotoWatermark.exe" "" "$INSTDIR\\PhotoWatermark.exe"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\卸载.lnk" "$INSTDIR\\uninstall.exe"
    
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\PhotoWatermark.exe" "" "$INSTDIR\\PhotoWatermark.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${COMPANYNAME} - ${APPNAME} - ${DESCRIPTION}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$\\"$INSTDIR$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "$\\"${COMPANYNAME}$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "$\\"${HELPURL}$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "$\\"${UPDATEURL}$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "$\\"${ABOUTURL}$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "$\\"${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}$\\""
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
    delete "$INSTDIR\\PhotoWatermark.exe"
    delete "$INSTDIR\\templates.json"
    delete "$INSTDIR\\README.md"
    delete "$INSTDIR\\uninstall.exe"
    
    rmDir "$INSTDIR"
    
    delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
    delete "$SMPROGRAMS\\${APPNAME}\\卸载.lnk"
    rmDir "$SMPROGRAMS\\${APPNAME}"
    
    delete "$DESKTOP\\${APPNAME}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
sectionEnd
"""
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    # 运行NSIS编译
    try:
        subprocess.run(["makensis", "installer.nsi"], check=True)
        print("✅ Windows安装包创建成功: PhotoWatermark-Setup.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows安装包创建失败: {e}")
        return False

def create_mac_installer():
    """创建Mac安装包"""
    print("🍎 创建Mac安装包...")
    
    # 检查是否有pkgbuild
    try:
        subprocess.run(["pkgbuild", "--help"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到pkgbuild，请确保在macOS上运行")
        return False
    
    # 创建应用包结构
    app_name = "PhotoWatermark.app"
    app_path = f"dist/{app_name}"
    
    # 创建.app包结构
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # 复制可执行文件
    if os.path.exists("dist/PhotoWatermark"):
        shutil.copy2("dist/PhotoWatermark", f"{app_path}/Contents/MacOS/")
        os.chmod(f"{app_path}/Contents/MacOS/PhotoWatermark", 0o755)
    
    # 复制资源文件
    if os.path.exists("templates.json"):
        shutil.copy2("templates.json", f"{app_path}/Contents/Resources/")
    if os.path.exists("README.md"):
        shutil.copy2("README.md", f"{app_path}/Contents/Resources/")
    
    # 创建Info.plist
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>PhotoWatermark</string>
    <key>CFBundleIdentifier</key>
    <string>com.photowatermark.app</string>
    <key>CFBundleName</key>
    <string>照片水印工具</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""
    
    with open(f"{app_path}/Contents/Info.plist", "w", encoding="utf-8") as f:
        f.write(info_plist)
    
    # 创建PKG安装包
    try:
        subprocess.run([
            "pkgbuild",
            "--root", "dist",
            "--identifier", "com.photowatermark.app",
            "--version", "2.0.0",
            "--install-location", "/Applications",
            "PhotoWatermark.pkg"
        ], check=True)
        print("✅ Mac安装包创建成功: PhotoWatermark.pkg")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Mac安装包创建失败: {e}")
        return False

def create_zip_packages():
    """创建ZIP压缩包"""
    print("📦 创建ZIP压缩包...")
    
    system = platform.system()
    arch = platform.machine()
    
    # 创建发布目录
    release_dir = f"PhotoWatermark-{system}-{arch}"
    os.makedirs(release_dir, exist_ok=True)
    
    # 复制文件
    exe_name = "PhotoWatermark.exe" if system == "Windows" else "PhotoWatermark"
    exe_path = f"dist/{exe_name}"
    
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_dir)
    
    # 复制其他文件
    files_to_copy = ["templates.json", "README.md"]
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
    
    # 创建启动脚本
    if system == "Windows":
        launcher_content = """@echo off
echo 正在启动照片水印工具...
PhotoWatermark.exe
pause
"""
        with open(f"{release_dir}/启动程序.bat", "w", encoding="gbk") as f:
            f.write(launcher_content)
    else:
        launcher_content = """#!/bin/bash
echo "正在启动照片水印工具..."
./PhotoWatermark
"""
        launcher_path = f"{release_dir}/启动程序.sh"
        with open(launcher_path, "w", encoding="utf-8") as f:
            f.write(launcher_content)
        os.chmod(launcher_path, 0o755)
    
    # 创建ZIP文件
    zip_name = f"PhotoWatermark-{system}-{arch}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, os.path.dirname(release_dir))
                zipf.write(file_path, arc_path)
    
    print(f"✅ ZIP压缩包创建成功: {zip_name}")
    return True

def main():
    """主函数"""
    print("📦 照片水印工具 - 安装包制作脚本")
    print(f"当前平台: {platform.system()} {platform.machine()}")
    
    # 检查dist目录是否存在
    if not os.path.exists("dist"):
        print("❌ 未找到dist目录，请先运行构建脚本")
        return False
    
    success = True
    
    # 创建ZIP压缩包（所有平台都支持）
    if not create_zip_packages():
        success = False
    
    # 根据平台创建专业安装包
    if platform.system() == "Windows":
        if not create_windows_installer():
            success = False
    elif platform.system() == "Darwin":  # macOS
        if not create_mac_installer():
            success = False
    else:
        print(f"⚠️  当前平台 {platform.system()} 不支持创建专业安装包，仅创建ZIP压缩包")
    
    if success:
        print("\n🎉 安装包制作完成！")
        print("📁 生成的文件:")
        for file in os.listdir("."):
            if file.endswith((".exe", ".pkg", ".zip")):
                print(f"  - {file}")
    else:
        print("\n❌ 安装包制作过程中出现错误")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
