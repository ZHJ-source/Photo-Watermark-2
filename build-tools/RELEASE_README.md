# 照片水印工具 - 发布说明

## 🎯 快速开始

### 方法一：一键构建（推荐新手）

```bash
python quick_build.py
```

### 方法二：完整构建（推荐开发者）

```bash
python build.py
```

### 方法三：创建安装包（推荐正式发布）

```bash
python build.py
python create_installer.py
```

## 📦 构建产物

构建完成后，您将获得：

### 1. 可执行文件
- **Windows**: `dist/PhotoWatermark.exe`
- **Mac**: `dist/PhotoWatermark`

### 2. 便携版（推荐分发）
- **Windows**: `PhotoWatermark-Portable/` 文件夹
- **Mac**: `PhotoWatermark-Portable/` 文件夹

### 3. 专业安装包（可选）
- **Windows**: `PhotoWatermark-Setup.exe`
- **Mac**: `PhotoWatermark.pkg`

## 🚀 发布流程

### 本地发布
1. 运行 `python quick_build.py`
2. 将 `PhotoWatermark-Portable` 文件夹打包成ZIP
3. 分发给用户

### GitHub自动发布
1. 推送代码到GitHub
2. 创建Release标签：`git tag v2.0.0 && git push origin v2.0.0`
3. GitHub Actions自动构建多平台版本
4. 在GitHub Releases页面下载构建产物

## 💡 使用建议

### 对于开发者
- 使用 `build.py` 进行完整构建
- 使用 `create_installer.py` 创建专业安装包
- 配置GitHub Actions实现自动化构建

### 对于普通用户
- 直接下载便携版ZIP文件
- 解压后双击启动程序即可使用
- 无需安装Python环境

## 🔧 故障排除

### 常见问题

1. **构建失败**
   - 确保Python版本 >= 3.7
   - 运行 `pip install -r requirements.txt`

2. **程序无法运行**
   - 检查是否缺少依赖文件
   - 在命令行运行查看错误信息

3. **中文显示问题**
   - 确保系统安装了中文字体
   - 检查字体路径配置

## 📞 技术支持

如遇问题，请：
1. 查看 `BUILD_GUIDE.md` 详细文档
2. 检查GitHub Issues
3. 提交新的Issue

---

**注意**: 首次构建可能需要下载依赖，请确保网络连接正常。
