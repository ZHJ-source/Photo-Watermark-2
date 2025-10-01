# 照片水印工具 - 构建和发布指南

本指南将帮助您为Mac和Windows平台创建点开即用的release版本。

## 📋 目录

- [快速开始](#快速开始)
- [构建方案](#构建方案)
- [详细步骤](#详细步骤)
- [自动化构建](#自动化构建)
- [发布流程](#发布流程)
- [故障排除](#故障排除)

## 🚀 快速开始

### 方法一：一键构建（推荐）

```bash
# 1. 安装构建依赖
pip install pyinstaller>=5.0

# 2. 运行构建脚本
python build.py

# 3. 创建安装包（可选）
python create_installer.py
```

### 方法二：手动构建

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install pyinstaller>=5.0

# 2. 构建可执行文件
pyinstaller build.spec

# 3. 查看结果
ls dist/
```

## 🛠️ 构建方案

### 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **PyInstaller** | 简单易用，支持多平台 | 文件较大 | 快速发布 |
| **GitHub Actions** | 自动化，多平台同时构建 | 需要GitHub账号 | 持续集成 |
| **专业安装包** | 用户体验好，可卸载 | 需要额外工具 | 正式发布 |

### 推荐方案

1. **开发测试**: 使用 `build.py` 快速构建
2. **正式发布**: 使用 GitHub Actions 自动构建
3. **专业分发**: 使用 `create_installer.py` 创建安装包

## 📝 详细步骤

### 1. 环境准备

#### Windows环境
```bash
# 安装Python 3.7+
# 安装Git
# 安装NSIS（可选，用于创建安装包）
# 下载地址: https://nsis.sourceforge.io/Download
```

#### Mac环境
```bash
# 安装Python 3.7+
# 安装Xcode Command Line Tools
xcode-select --install

# 安装Homebrew（可选）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 项目配置

#### 检查依赖
```bash
# 确保requirements.txt包含所有依赖
cat requirements.txt
```

#### 创建图标文件（可选）
- Windows: 创建 `icon.ico` 文件
- Mac: 创建 `icon.icns` 文件
- 推荐尺寸: 256x256 像素

### 3. 构建可执行文件

#### 使用构建脚本
```bash
python build.py
```

#### 手动构建
```bash
# 安装PyInstaller
pip install pyinstaller>=5.0

# 构建
pyinstaller build.spec

# 检查结果
ls dist/
```

### 4. 测试构建结果

```bash
# Windows
dist/PhotoWatermark.exe

# Mac/Linux
dist/PhotoWatermark
```

## 🤖 自动化构建

### GitHub Actions配置

1. **推送代码到GitHub**
2. **创建Release标签**
   ```bash
   git tag v2.0.0
   git push origin v2.0.0
   ```
3. **自动构建开始**
   - 构建Windows x64版本
   - 构建Mac Intel版本
   - 构建Mac Apple Silicon版本

### 构建产物

每次构建会生成：
- `PhotoWatermark-windows-latest-x64.zip`
- `PhotoWatermark-macos-latest-x64.zip`
- `PhotoWatermark-macos-latest-arm64.zip`

## 📦 发布流程

### 1. 本地发布

```bash
# 1. 构建所有版本
python build.py

# 2. 创建安装包
python create_installer.py

# 3. 打包发布
zip -r PhotoWatermark-Release.zip release/
```

### 2. GitHub发布

```bash
# 1. 创建Release标签
git tag v2.0.0
git push origin v2.0.0

# 2. 在GitHub上创建Release
# 3. 上传构建产物
# 4. 发布Release
```

### 3. 分发方式

#### 方式一：ZIP压缩包
- 优点：简单，无需安装
- 缺点：需要手动解压
- 适用：快速测试

#### 方式二：安装包
- 优点：专业，可卸载
- 缺点：需要额外工具
- 适用：正式发布

#### 方式三：便携版
- 优点：绿色软件
- 缺点：文件较大
- 适用：U盘携带

## 🔧 故障排除

### 常见问题

#### 1. PyInstaller构建失败

**问题**: `ModuleNotFoundError: No module named 'PIL'`

**解决**:
```bash
pip install Pillow>=10.0.0
pyinstaller build.spec
```

#### 2. 可执行文件无法运行

**问题**: 双击无反应

**解决**:
```bash
# 检查控制台输出
# Windows: 在命令行运行
dist/PhotoWatermark.exe

# Mac: 在终端运行
dist/PhotoWatermark
```

#### 3. 中文显示问题

**问题**: 水印文字显示为方块

**解决**:
- 确保系统安装了中文字体
- 在代码中指定字体路径

#### 4. 文件路径问题

**问题**: 找不到templates.json

**解决**:
- 确保templates.json在可执行文件同目录
- 检查build.spec中的datas配置

### 调试技巧

#### 1. 启用控制台输出
```python
# 在build.spec中设置
console=True
```

#### 2. 查看详细构建信息
```bash
pyinstaller --log-level DEBUG build.spec
```

#### 3. 检查依赖
```bash
pyinstaller --collect-all pillow build.spec
```

## 📊 构建配置说明

### build.spec文件解析

```python
# 主程序入口
a = Analysis(['main.py'], ...)

# 数据文件
datas=[('templates.json', '.'), ...]

# 隐藏导入
hiddenimports=['PIL._tkinter_finder', ...]

# 可执行文件配置
exe = EXE(..., console=False, ...)
```

### 关键配置项

- `console=False`: 隐藏控制台窗口
- `upx=True`: 启用UPX压缩
- `strip=False`: 保留调试信息
- `icon='icon.ico'`: 设置应用图标

## 🎯 最佳实践

### 1. 版本管理
- 使用语义化版本号
- 为每个版本创建Git标签
- 维护CHANGELOG.md

### 2. 测试策略
- 在目标平台测试
- 测试不同图片格式
- 验证所有功能

### 3. 发布策略
- 先发布测试版本
- 收集用户反馈
- 修复问题后发布正式版

### 4. 文档维护
- 更新README.md
- 记录已知问题
- 提供使用教程

## 📞 技术支持

如果您在构建过程中遇到问题：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 提交新的Issue描述问题
4. 提供详细的错误信息和系统环境

## 🔄 更新日志

- **v2.0.0**: 初始版本，支持基本构建
- **v2.1.0**: 添加GitHub Actions支持
- **v2.2.0**: 添加安装包制作功能

---

**注意**: 本指南基于Python 3.7+和PyInstaller 5.0+编写，其他版本可能需要调整配置。
