# 📦 发布 PDF Zipper 到 PyPI 指南

## 🎯 发布前准备

### 1. 确保项目信息完整
检查 `pyproject.toml` 中的以下信息：
- [ ] 项目名称（确保在 PyPI 上唯一）
- [ ] 版本号
- [ ] 作者信息
- [ ] 项目描述
- [ ] GitHub 仓库链接
- [ ] 许可证信息

### 2. 更新项目元数据
```bash
# 编辑 pyproject.toml
vim pyproject.toml
```

需要更新的字段：
```toml
[project]
name = "pdf-zipper"  # 可能需要改名，如 "pdf-zipper-tool"
authors = [
    { name = "Your Name", email = "your.email@example.com" },
]

[project.urls]
Homepage = "https://github.com/your-username/pdf-zipper"
Repository = "https://github.com/your-username/pdf-zipper"
Issues = "https://github.com/your-username/pdf-zipper/issues"
```

## 🔧 发布步骤

### 1. 注册 PyPI 账户
- 访问 https://pypi.org/account/register/
- 注册账户并验证邮箱
- 启用两步验证（推荐）

### 2. 创建 API Token
- 登录 PyPI
- 访问 https://pypi.org/manage/account/token/
- 创建新的 API token
- 保存 token（只显示一次）

### 3. 配置本地认证
```bash
# 创建 ~/.pypirc 文件
cat > ~/.pypirc << EOF
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-api-token-here
EOF

# 设置文件权限
chmod 600 ~/.pypirc
```

### 4. 检查包名可用性
```bash
# 搜索是否已存在同名包
pip search pdf-zipper
# 或访问 https://pypi.org/project/pdf-zipper/
```

如果名称已被占用，需要修改 `pyproject.toml` 中的包名，例如：
- `pdf-zipper-tool`
- `pdf-compression-tool`
- `pdfzipper-cli`

### 5. 构建和测试包
```bash
# 清理之前的构建
make clean

# 构建包
make build

# 检查构建的包
twine check dist/*

# 本地测试安装
pip install dist/pdf_zipper-1.0.0-py3-none-any.whl
pdf-zipper --help
```

### 6. 上传到 Test PyPI（推荐先测试）
```bash
# 上传到测试环境
python -m twine upload --repository testpypi dist/*

# 从测试环境安装验证
pip install --index-url https://test.pypi.org/simple/ pdf-zipper
```

### 7. 正式发布到 PyPI
```bash
# 确认一切正常后，上传到正式 PyPI
python -m twine upload dist/*
```

## 📋 发布检查清单

### 发布前检查
- [ ] 所有测试通过
- [ ] 文档完整且准确
- [ ] 版本号正确
- [ ] 依赖项列表完整
- [ ] 许可证文件存在
- [ ] README.md 内容准确
- [ ] 包名在 PyPI 上可用

### 发布后验证
- [ ] 在 PyPI 上能找到包
- [ ] `pip install pdf-zipper` 能正常安装
- [ ] 安装后命令能正常工作
- [ ] 文档链接正确

## 🔄 版本管理

### 语义化版本控制
- `1.0.0` - 主要版本（重大变更）
- `1.1.0` - 次要版本（新功能）
- `1.0.1` - 补丁版本（bug 修复）

### 发布新版本
```bash
# 1. 更新版本号
vim src/pdf_zipper/__init__.py
vim pyproject.toml

# 2. 提交更改
git add .
git commit -m "Bump version to 1.0.1"
git tag v1.0.1

# 3. 构建和发布
make clean
make build
twine upload dist/*

# 4. 推送到 Git
git push origin main --tags
```

## 🚨 常见问题

### 1. 包名已存在
```bash
# 修改包名
sed -i 's/name = "pdf-zipper"/name = "pdf-zipper-tool"/' pyproject.toml
```

### 2. 上传失败
```bash
# 检查网络连接
ping pypi.org

# 检查认证信息
cat ~/.pypirc

# 重新生成 API token
```

### 3. 依赖问题
```bash
# 检查依赖是否都在 PyPI 上可用
pip install --dry-run -r requirements.txt
```

## 📝 发布后更新 README

发布成功后，更新 README.md：

```markdown
## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install pdf-zipper  # 或你的实际包名
```

### From Source
```bash
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper
pip install -e .
```
```

## 🎉 完成

发布成功后，用户就可以通过简单的 `pip install pdf-zipper` 来安装你的工具了！

记得在项目的 GitHub 页面添加 PyPI 徽章：
```markdown
[![PyPI version](https://badge.fury.io/py/pdf-zipper.svg)](https://badge.fury.io/py/pdf-zipper)
```
