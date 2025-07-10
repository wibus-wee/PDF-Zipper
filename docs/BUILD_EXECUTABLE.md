# 🔨 构建可执行文件指南

PDF Zipper 支持构建为独立的可执行文件，用户无需安装 Python 环境即可使用。

## 📋 支持的平台

- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Windows** (x64)
- ✅ **Linux** (x64) - 理论支持，需要在 Linux 环境中构建

## 🚀 快速开始

### macOS / Linux

```bash
# 1. 安装构建依赖
pip install -e ".[build]"

# 2. 运行构建脚本
python build_executable.py

# 3. 查看输出
ls -la release/
```

### Windows

```cmd
REM 1. 运行 Windows 构建脚本
build_windows.bat

REM 2. 查看输出
dir release\
```

## 📦 构建输出

构建完成后，`release/` 目录将包含：

- `pdf-zipper-cli-{platform}-{arch}` - CLI 版本（推荐）
- `pdf-zipper-full-{platform}-{arch}` - 完整版本（包含 GUI，可能不稳定）
- `README.txt` - 使用说明

### 文件大小

- **CLI 版本**: ~42MB
- **完整版本**: ~44MB

## 🔧 手动构建

如果自动构建脚本有问题，可以手动构建：

### CLI 版本（推荐）

```bash
# 构建 CLI 版本
pyinstaller --onefile --name pdf-zipper-cli main_cli_only.py

# 测试
./dist/pdf-zipper-cli --version
```

### 完整版本

```bash
# 构建完整版本（可能失败）
pyinstaller --onefile --name pdf-zipper-full main.py

# 测试
./dist/pdf-zipper-full --version
```

## 🐛 常见问题

### 1. Textual GUI 构建失败

**问题**: 完整版本构建时出现 `ModuleNotFoundError: No module named 'textual.widgets._tab_pane'`

**解决方案**: 
- 使用 CLI 版本，功能完整且稳定
- GUI 版本的依赖比较复杂，PyInstaller 可能无法正确打包所有模块

### 2. 文件过大

**问题**: 生成的可执行文件很大（40MB+）

**解决方案**:
- 这是正常的，因为包含了完整的 Python 运行时和所有依赖
- 可以使用 UPX 压缩（已在 spec 文件中启用）

### 3. 启动速度慢

**问题**: 首次运行需要几秒钟

**解决方案**:
- 这是正常的，PyInstaller 打包的程序需要解压和初始化
- 后续运行会更快

## 🔄 跨平台构建

要为不同平台构建，需要在对应的操作系统上运行构建：

### GitHub Actions 自动构建

可以使用 GitHub Actions 自动为多个平台构建：

```yaml
# .github/workflows/build.yml
name: Build Executables

on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e ".[build]"
    
    - name: Build executable
      run: |
        python build_executable.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: pdf-zipper-${{ matrix.os }}
        path: release/
```

## 📝 构建脚本说明

### `build_executable.py`

主要构建脚本，支持：
- 自动检测平台
- 构建 CLI 和完整版本
- 整理输出文件
- 生成说明文档

### `main_cli_only.py`

CLI 版本的入口点，包含：
- 所有 CLI 功能
- 不依赖 Textual GUI
- 更稳定的构建

### `main.py`

完整版本的入口点，包含：
- CLI 和 GUI 功能
- 依赖 Textual
- 构建可能不稳定

## 🎯 推荐使用

1. **开发者**: 使用 `pip install pdf-zipper`
2. **最终用户**: 下载 CLI 可执行文件
3. **企业部署**: 使用可执行文件，无需 Python 环境

## 📊 性能对比

| 方式 | 启动时间 | 文件大小 | 依赖 |
|------|----------|----------|------|
| pip 安装 | 快 | 小 | Python 环境 |
| CLI 可执行文件 | 中等 | 42MB | 无 |
| 完整可执行文件 | 中等 | 44MB | 无 |

## 🔗 相关链接

- [PyInstaller 文档](https://pyinstaller.readthedocs.io/)
- [构建问题反馈](https://github.com/your-username/pdf-zipper/issues)
- [发布页面](https://github.com/your-username/pdf-zipper/releases)
