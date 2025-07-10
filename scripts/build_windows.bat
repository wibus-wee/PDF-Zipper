@echo off
REM Windows 构建脚本 for PDF Zipper

echo 🚀 PDF Zipper Windows 构建工具
echo ================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" >nul 2>&1
if errorlevel 1 (
    echo 📝 建议在虚拟环境中运行构建
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -e .[build]
    echo.
)

echo 📦 安装构建依赖...
pip install -e .[build]
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo 🧹 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release

echo 🔨 构建 CLI 版本...
pyinstaller --onefile --name pdf-zipper-cli main_cli_only.py
if errorlevel 1 (
    echo ❌ CLI 版本构建失败
    pause
    exit /b 1
)

echo 📦 整理输出文件...
if not exist release mkdir release

REM 移动 CLI 可执行文件
if exist dist\pdf-zipper-cli.exe (
    move dist\pdf-zipper-cli.exe release\pdf-zipper-cli-windows-x64.exe
    echo ✅ 创建 Windows CLI 可执行文件: release\pdf-zipper-cli-windows-x64.exe
)

REM 创建说明文件
echo # PDF Zipper Windows 可执行文件 > release\README.txt
echo. >> release\README.txt
echo ## 使用方法 >> release\README.txt
echo. >> release\README.txt
echo ### 命令行模式 >> release\README.txt
echo pdf-zipper-cli-windows-x64.exe --help >> release\README.txt
echo pdf-zipper-cli-windows-x64.exe compress input.pdf output.pdf --target-size 5 >> release\README.txt
echo. >> release\README.txt
echo ## 功能 >> release\README.txt
echo - 🗜️ PDF 压缩 (自动/手动) >> release\README.txt
echo - 📊 PDF 转 PowerPoint >> release\README.txt
echo - ⌨️ 命令行界面 >> release\README.txt
echo. >> release\README.txt
echo ## 注意事项 >> release\README.txt
echo - 这是一个独立的可执行文件，无需安装 Python 环境 >> release\README.txt
echo - 首次运行可能需要几秒钟启动时间 >> release\README.txt

echo.
echo 🎉 构建完成!
echo 📁 输出文件位于 'release' 目录

REM 显示文件信息
echo.
echo 📊 文件信息:
for %%f in (release\*) do (
    echo    %%~nxf: %%~zf bytes
)

echo.
echo 💡 测试可执行文件:
echo    release\pdf-zipper-cli-windows-x64.exe --version
echo.

pause
