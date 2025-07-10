# 📁 PDF Zipper 项目结构

## 🗂️ 目录结构

```
pdf-zipper/
├── 📄 README.md                    # 项目主要说明文档
├── 📄 LICENSE                      # MIT 许可证
├── 📄 pyproject.toml               # Python 项目配置
├── 📄 requirements.txt             # 依赖列表
├── 📄 Makefile                     # 构建和开发命令
├── 📄 .gitignore                   # Git 忽略文件配置
├── 📄 PROJECT_STRUCTURE.md         # 本文件
│
├── 📁 src/                         # 源代码目录
│   └── 📁 pdf_zipper/             # 主要 Python 包
│       ├── 📄 __init__.py          # 包初始化文件
│       ├── 📄 core.py              # 核心 PDF 处理功能
│       ├── 📄 cli.py               # 命令行界面
│       └── 📄 gui.py               # 图形用户界面 (Textual)
│
├── 📁 tests/                       # 测试文件
│   ├── 📄 __init__.py              # 测试包初始化
│   └── 📄 test_core.py             # 核心功能测试
│
├── 📁 scripts/                     # 构建和安装脚本
│   ├── 📄 build_executable.py      # 主要构建脚本
│   ├── 📄 build_gui_executable.py  # GUI 专用构建脚本
│   ├── 📄 build_windows.bat        # Windows 构建脚本
│   ├── 📄 install.sh               # Linux/macOS 安装脚本
│   ├── 📄 main.py                  # 完整版本入口点
│   └── 📄 main_cli_only.py         # CLI 版本入口点
│
├── 📁 docs/                        # 文档目录
│   ├── 📄 BUILD_EXECUTABLE.md      # 可执行文件构建指南
│   ├── 📄 EXECUTABLE_BUILD_SUCCESS.md # 构建成功总结
│   └── 📄 RELEASE_SUMMARY.md       # 发布总结
│
├── 📁 examples/                    # 示例和截图
│   ├── 📄 usage_examples.py        # 使用示例代码
│   ├── 🖼️ screenshot-cli.png       # CLI 界面截图
│   └── 🖼️ screenshot-gui.png       # GUI 界面截图
│
└── 📁 release/                     # 构建输出目录 (被 .gitignore 忽略)
    ├── 📄 pdf-zipper-cli-*         # CLI 可执行文件
    ├── 📄 pdf-zipper-gui-*         # GUI 可执行文件
    ├── 📁 *.app                    # macOS App Bundle
    └── 📄 README.txt               # 使用说明
```

## 📋 文件说明

### 🔧 核心文件

- **`src/pdf_zipper/core.py`** - PDF 压缩和转换的核心逻辑
- **`src/pdf_zipper/cli.py`** - 命令行界面实现 (Typer)
- **`src/pdf_zipper/gui.py`** - 图形界面实现 (Textual)

### 🏗️ 构建文件

- **`scripts/build_executable.py`** - 主要构建脚本，构建所有版本
- **`scripts/build_gui_executable.py`** - 专门构建 GUI 版本，解决 Textual 依赖问题
- **`scripts/main.py`** - 完整版本的入口点 (CLI + GUI)
- **`scripts/main_cli_only.py`** - CLI 版本的入口点 (仅 CLI)

### 📚 文档文件

- **`README.md`** - 项目主要文档，包含安装和使用说明
- **`docs/BUILD_EXECUTABLE.md`** - 详细的可执行文件构建指南
- **`docs/EXECUTABLE_BUILD_SUCCESS.md`** - 构建成功的技术总结
- **`docs/RELEASE_SUMMARY.md`** - PyPI 发布总结

### ⚙️ 配置文件

- **`pyproject.toml`** - Python 项目配置，包含依赖、构建设置等
- **`Makefile`** - 开发和构建命令的快捷方式
- **`.gitignore`** - Git 版本控制忽略文件配置

## 🚀 常用命令

### 开发命令
```bash
make install-dev    # 安装开发依赖
make test          # 运行测试
make lint          # 代码检查
make format        # 代码格式化
```

### 构建命令
```bash
make build-exe     # 构建所有可执行文件
make build-cli     # 只构建 CLI 版本
make build-gui     # 只构建 GUI 版本
make clean-exe     # 清理构建文件
```

### 发布命令
```bash
make build         # 构建 Python 包
make upload        # 上传到 PyPI
```

## 🎯 开发工作流

1. **安装开发环境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # 或 .venv\Scripts\activate  # Windows
   make install-dev
   ```

2. **开发和测试**
   ```bash
   make test          # 运行测试
   make lint          # 检查代码质量
   make format        # 格式化代码
   ```

3. **构建可执行文件**
   ```bash
   make build-exe     # 构建所有版本
   ```

4. **发布到 PyPI**
   ```bash
   make build         # 构建 Python 包
   make upload        # 上传到 PyPI
   ```

## 📦 输出产物

### Python 包 (PyPI)
- 通过 `pip install pdf-zipper` 安装
- 提供 `pdf-zipper` 和 `pdfzip` 命令

### 可执行文件
- **CLI 版本**: 约 42MB，包含所有 CLI 功能
- **GUI 版本**: 约 44MB，包含 CLI + GUI 功能
- **App Bundle**: macOS 专用，双击运行

### 支持平台
- ✅ macOS (Intel & Apple Silicon)
- ✅ Windows (x64)
- ✅ Linux (x64)

## 🔄 版本控制

项目使用语义化版本控制：
- `1.0.0` - 主要版本（重大变更）
- `1.1.0` - 次要版本（新功能）
- `1.0.1` - 补丁版本（bug 修复）

版本信息在 `src/pdf_zipper/__init__.py` 和 `pyproject.toml` 中维护。
