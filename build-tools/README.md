# 构建工具目录

这个目录包含了所有与构建和打包相关的文件和工具。

## 🚀 快速使用

### 1. 快速构建（推荐）
```bash
cd build-tools
python quick_build.py
```

### 2. 完整构建
```bash
cd build-tools
python build.py
```

### 3. 创建安装包
```bash
cd build-tools
python build.py
python create_installer.py
```

## 📁 文件说明

- `quick_build.py` - 一键快速构建脚本
- `build.py` - 完整构建脚本
- `create_installer.py` - 安装包制作脚本
- `build.spec` - PyInstaller配置文件
- `BUILD_GUIDE.md` - 详细构建指南
- `RELEASE_README.md` - 发布说明
- `.github/workflows/build.yml` - GitHub Actions自动构建配置
- `PhotoWatermark-v1.0.0-macos-arm64.zip` - 已构建的发布包

## 🎯 使用建议

- **开发测试**: 使用 `quick_build.py`
- **正式发布**: 使用 `build.py`
- **专业分发**: 使用 `create_installer.py`

## 📖 详细文档

查看 `BUILD_GUIDE.md` 获取完整的构建和发布指南。
