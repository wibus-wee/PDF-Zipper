# 🚀 PDF Zipper 部署指南

## 📦 打包和分发

### 1. 本地安装（开发模式）
```bash
# 克隆项目
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper

# 安装为可编辑包
pip install -e .

# 或使用安装脚本
./install.sh
```

### 2. 构建分发包
```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 生成的文件在 dist/ 目录：
# - pdf_zipper-1.0.0-py3-none-any.whl (wheel 包)
# - pdf_zipper-1.0.0.tar.gz (源码包)
```

### 3. 发布到 PyPI
```bash
# 测试上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 正式上传到 PyPI
python -m twine upload dist/*
```

## 🖥️ CLI 使用方法

安装后，你可以使用以下命令：

### 基本命令
```bash
# 显示帮助
pdf-zipper --help
pdfzip --help  # 简短别名

# 显示版本
pdf-zipper --version
```

### GUI 模式
```bash
# 启动图形界面
pdf-zipper gui
```

### 压缩 PDF
```bash
# 自动压缩到指定大小
pdf-zipper compress input.pdf --target-size 5.0

# 手动压缩（指定 DPI）
pdf-zipper compress input.pdf --dpi 150

# 指定输出文件
pdf-zipper compress input.pdf -o compressed.pdf --dpi 100

# 静默模式（无输出）
pdf-zipper compress input.pdf --quiet
```

### 转换为 PowerPoint
```bash
# 转换为 PPT
pdf-zipper convert input.pdf

# 指定输出文件和 DPI
pdf-zipper convert input.pdf -o presentation.pptx --dpi 200
```

### 查看 PDF 信息
```bash
# 显示 PDF 详细信息
pdf-zipper info document.pdf
```

## 🛠️ 开发工具

### Makefile 命令
```bash
make help           # 显示所有可用命令
make install        # 安装包
make install-dev    # 安装开发依赖
make test           # 运行测试
make lint           # 代码检查
make format         # 格式化代码
make clean          # 清理构建文件
make build          # 构建包
make demo           # 运行演示
make dev-setup      # 设置开发环境
```

### 项目结构
```
pdf-zipper/
├── src/pdf_zipper/          # 主要源码
│   ├── __init__.py          # 包初始化
│   ├── core.py              # 核心 PDF 处理逻辑
│   ├── cli.py               # 命令行界面
│   └── gui.py               # 图形用户界面
├── tests/                   # 测试文件
├── dist/                    # 构建输出
├── pyproject.toml           # 项目配置
├── Makefile                 # 开发工具
├── install.sh               # 安装脚本
├── README.md                # 项目说明
└── LICENSE                  # 许可证
```

## 🔧 高级配置

### 环境变量
```bash
# 设置默认 DPI
export PDF_ZIPPER_DEFAULT_DPI=150

# 设置默认目标大小（MB）
export PDF_ZIPPER_DEFAULT_SIZE=5.0
```

### 批处理示例
```bash
# 批量压缩当前目录所有 PDF
for file in *.pdf; do
    pdf-zipper compress "$file" --target-size 5.0
done

# 批量转换为 PPT
for file in *.pdf; do
    pdf-zipper convert "$file"
done
```

## 📋 系统要求

- Python 3.8+
- macOS / Linux / Windows
- 至少 100MB 可用磁盘空间
- 推荐 4GB+ RAM（处理大型 PDF 时）

## 🐛 故障排除

### 常见问题

1. **命令未找到**
   ```bash
   # 确保 pip 安装路径在 PATH 中
   echo $PATH
   which pdf-zipper
   ```

2. **权限错误**
   ```bash
   # 使用用户安装
   pip install --user -e .
   ```

3. **依赖冲突**
   ```bash
   # 使用虚拟环境
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

## 🚀 性能优化

- 对于大型 PDF，建议使用较低的 DPI 值
- 自动压缩模式会进行多次迭代，可能较慢但结果精确
- GUI 模式使用后台线程，不会阻塞界面
- CLI 模式适合批处理和自动化脚本
