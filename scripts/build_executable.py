#!/usr/bin/env python3
"""
构建 PDF Zipper 可执行文件的脚本
支持 Windows、macOS 和 Linux 平台
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path


def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        return "macos", machine
    elif system == "windows":
        return "windows", machine
    elif system == "linux":
        return "linux", machine
    else:
        return system, machine


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)


def run_pyinstaller():
    """运行 PyInstaller"""
    print("🔨 开始构建可执行文件...")

    # 构建 CLI-only 版本（更稳定）
    print("📦 构建 CLI 版本...")
    cmd_cli = ["pyinstaller", "--onefile", "--name", "pdf-zipper-cli", "scripts/main_cli_only.py"]

    try:
        subprocess.run(cmd_cli, check=True, capture_output=True, text=True)
        print("✅ CLI 版本构建成功!")
    except subprocess.CalledProcessError as e:
        print(f"❌ CLI 版本构建失败:")
        print(f"错误输出: {e.stderr}")
        return False

    # 尝试构建完整版本（包含 GUI）
    print("📦 尝试构建完整版本（包含 GUI）...")
    cmd_full = ["python", "scripts/build_gui_executable.py"]

    try:
        subprocess.run(cmd_full, check=True, capture_output=True, text=True)
        print("✅ 完整版本构建成功!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  完整版本构建失败:")
        print(f"错误输出: {e.stderr}")
        print("📝 将只提供 CLI 版本")

    return True


def organize_output():
    """整理输出文件"""
    system, machine = get_platform_info()

    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)

    # 处理 CLI 版本
    cli_executable = None
    if system == "windows":
        cli_executable = Path("dist/pdf-zipper-cli.exe")
        extension = ".exe"
    else:
        cli_executable = Path("dist/pdf-zipper-cli")
        extension = ""

    if cli_executable and cli_executable.exists():
        target = release_dir / f"pdf-zipper-cli-{system}-{machine}{extension}"
        if target.exists():
            target.unlink()
        shutil.move(str(cli_executable), str(target))
        if system != "windows":
            os.chmod(target, 0o755)
        print(f"📦 创建 CLI 可执行文件: {target}")

    # 处理 GUI 版本（如果存在）
    gui_executable = None
    if system == "windows":
        gui_executable = Path("dist/pdf-zipper-gui.exe")
    else:
        gui_executable = Path("dist/pdf-zipper-gui")

    if gui_executable and gui_executable.exists():
        target = release_dir / f"pdf-zipper-gui-{system}-{machine}{extension}"
        if target.exists():
            target.unlink()
        shutil.move(str(gui_executable), str(target))
        if system != "windows":
            os.chmod(target, 0o755)
        print(f"📦 创建 GUI 可执行文件: {target}")

    # 检查 release 目录中是否已有 GUI 文件（由 build_gui_executable.py 创建）
    existing_gui = None
    if system == "darwin":
        existing_gui = release_dir / f"pdf-zipper-gui-darwin-{machine}"
    elif system == "windows":
        existing_gui = release_dir / f"pdf-zipper-gui-windows-{machine}.exe"
    else:
        existing_gui = release_dir / f"pdf-zipper-gui-linux-{machine}"

    if existing_gui and existing_gui.exists():
        print(f"📦 发现已存在的 GUI 可执行文件: {existing_gui}")

    # 处理 macOS App Bundle（如果存在）
    if system == "macos":
        app_bundle = Path("dist/PDF Zipper.app")
        if app_bundle.exists():
            target = release_dir / f"PDF-Zipper-{system}-{machine}.app"
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(app_bundle), str(target))
            print(f"📦 创建 macOS App Bundle: {target}")


def create_readme():
    """创建发布说明文件"""
    system, machine = get_platform_info()
    
    readme_content = f"""# PDF Zipper 可执行文件

## 平台信息
- 操作系统: {platform.system()}
- 架构: {platform.machine()}
- Python 版本: {platform.python_version()}

## 使用方法

### 命令行模式
```bash
./pdf-zipper-{system}-{machine} --help
./pdf-zipper-{system}-{machine} compress input.pdf output.pdf --target-size 5
```

### GUI 模式
```bash
./pdf-zipper-{system}-{machine} gui
```

## 功能
- 🗜️ PDF 压缩 (自动/手动)
- 📊 PDF 转 PowerPoint
- 🖥️ 图形界面
- ⌨️ 命令行界面

## 注意事项
- 这是一个独立的可执行文件，无需安装 Python 环境
- 首次运行可能需要几秒钟启动时间
- 如果遇到权限问题，请确保文件有执行权限

## 支持
- GitHub: https://github.com/your-username/pdf-zipper
- PyPI: https://pypi.org/project/pdf-zipper/
"""
    
    readme_path = Path("release") / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"📝 创建说明文件: {readme_path}")


def main():
    """主函数"""
    print("🚀 PDF Zipper 可执行文件构建工具")
    print("=" * 50)
    
    system, machine = get_platform_info()
    print(f"🖥️  平台: {system}-{machine}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # 检查是否安装了 PyInstaller
    try:
        import PyInstaller
        print(f"📦 PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ 未找到 PyInstaller，请先安装:")
        print("   pip install pyinstaller")
        sys.exit(1)
    
    # 构建步骤
    print("\n🔧 开始构建过程...")
    
    # 1. 清理
    clean_build_dirs()
    
    # 2. 构建
    if not run_pyinstaller():
        sys.exit(1)
    
    # 3. 整理输出
    organize_output()
    
    # 4. 创建说明文件
    create_readme()
    
    print("\n🎉 构建完成!")
    print("📁 输出文件位于 'release' 目录")
    
    # 显示文件大小
    release_dir = Path("release")
    if release_dir.exists():
        print("\n📊 文件信息:")
        for file_path in release_dir.iterdir():
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"   {file_path.name}: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
