#!/usr/bin/env python3
"""
专门构建包含 GUI 的 PDF Zipper 可执行文件
使用更强力的方法来处理 Textual 依赖
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path


def get_textual_modules():
    """动态获取所有 textual 模块"""
    try:
        import textual
        import pkgutil
        
        modules = []
        
        # 获取 textual 包的路径
        textual_path = textual.__path__
        
        # 遍历所有子模块
        for importer, modname, _ in pkgutil.walk_packages(
            textual_path,
            textual.__name__ + "."
        ):
            modules.append(modname)
            print(f"发现 textual 模块: {modname}")
        
        return modules
    except Exception as e:
        print(f"获取 textual 模块失败: {e}")
        return []


def create_enhanced_spec():
    """创建增强的 spec 文件"""
    print("🔍 分析 Textual 模块...")
    textual_modules = get_textual_modules()
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 获取项目根目录
project_root = Path(os.getcwd())

# 动态发现的 textual 模块
textual_hiddenimports = {textual_modules}

a = Analysis(
    ['scripts/main_gui_app.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 添加 textual 的 CSS 文件和资源
        ('src/pdf_zipper', 'pdf_zipper'),
    ],
    hiddenimports=[
        # 核心依赖
        'pdf_zipper',
        'pdf_zipper.core',
        'pdf_zipper.gui',
        'pdf_zipper.cli',
        
        # PyMuPDF 相关
        'fitz',
        'pymupdf',
        
        # Rich 相关
        'rich',
        'rich.console',
        'rich.panel',
        'rich.text',
        'rich.progress',
        'rich.table',
        'rich.markdown',
        'rich.syntax',
        'rich.traceback',
        'rich.align',
        'rich.bar',
        'rich.box',
        'rich.columns',
        'rich.layout',
        'rich.live',
        'rich.padding',
        'rich.rule',
        'rich.spinner',
        'rich.status',
        'rich.tree',
        
        # 其他依赖
        'typer',
        'click',
        'PIL',
        'PIL.Image',
        'pptx',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        
        # 系统相关
        'platform',
        'subprocess',
        'threading',
        'queue',
        'asyncio',
        'weakref',
        'functools',
        'itertools',
        'collections',
        'collections.abc',
        'contextlib',
        'dataclasses',
        'enum',
        'inspect',
        'operator',
        'time',
        'datetime',
        'math',
        're',
        'string',
        'unicodedata',
        
        # 添加所有动态发现的 textual 模块
    ] + textual_hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小文件大小
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'jupyter',
        'IPython',
        'notebook',
        'pytest',
        'unittest',
        'test',
        'tests',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf-zipper-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 改为 False，这样 App Bundle 不会显示终端窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# 如果是 macOS，创建 app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='PDF Zipper.app',
        icon=None,
        bundle_identifier='com.pdfzipper.app',
        info_plist={{
            'CFBundleName': 'PDF Zipper',
            'CFBundleDisplayName': 'PDF Zipper',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleIdentifier': 'com.pdfzipper.app',
            'CFBundleExecutable': 'pdf-zipper-gui',
            'CFBundlePackageType': 'APPL',
            'CFBundleSignature': 'PDFZ',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
            'NSRequiresAquaSystemAppearance': False,
            'LSApplicationCategoryType': 'public.app-category.productivity',
            'CFBundleDocumentTypes': [
                {{
                    'CFBundleTypeName': 'PDF Document',
                    'CFBundleTypeExtensions': ['pdf'],
                    'CFBundleTypeRole': 'Editor',
                    'CFBundleTypeIconFile': 'pdf-icon',
                    'LSHandlerRank': 'Alternate'
                }}
            ],
            'UTExportedTypeDeclarations': [
                {{
                    'UTTypeIdentifier': 'com.adobe.pdf',
                    'UTTypeConformsTo': ['public.data'],
                    'UTTypeDescription': 'PDF Document',
                    'UTTypeTagSpecification': {{
                        'public.filename-extension': ['pdf'],
                        'public.mime-type': ['application/pdf']
                    }}
                }}
            ]
        }},
    )
'''
    
    with open('pdf-zipper-gui.spec', 'w') as f:
        f.write(spec_content)
    
    print(f"✅ 创建增强 spec 文件，包含 {len(textual_modules)} 个 textual 模块")


def build_gui_executable():
    """构建 GUI 可执行文件"""
    print("🚀 PDF Zipper GUI 可执行文件构建工具")
    print("=" * 50)
    
    # 检查依赖
    try:
        import textual
        print(f"📦 Textual: {textual.__version__}")
    except ImportError:
        print("❌ 未找到 Textual，请先安装:")
        print("   pip install textual")
        sys.exit(1)
    
    # 清理旧文件
    print("🧹 清理旧的构建文件...")
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 创建增强的 spec 文件
    create_enhanced_spec()
    
    # 构建
    print("🔨 开始构建 GUI 可执行文件...")
    cmd = ["pyinstaller", "--clean", "pdf-zipper-gui.spec"]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ GUI 可执行文件构建成功!")
        
        # 整理输出
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        release_dir = Path("release")
        release_dir.mkdir(exist_ok=True)
        
        if system == "darwin":
            # macOS
            executable = Path("dist/pdf-zipper-gui")
            app_bundle = Path("dist/PDF Zipper.app")

            if executable.exists():
                target = release_dir / f"pdf-zipper-gui-{system}-{machine}"
                if target.exists():
                    target.unlink()
                shutil.move(str(executable), str(target))
                os.chmod(target, 0o755)
                print(f"📦 创建 GUI 可执行文件: {target}")

            if app_bundle.exists():
                target = release_dir / f"PDF-Zipper-{system}-{machine}.app"
                if target.exists():
                    shutil.rmtree(target)
                shutil.move(str(app_bundle), str(target))
                print(f"📦 创建 macOS App Bundle: {target}")
                print(f"💡 双击 App Bundle 将直接启动 GUI 界面")
        
        elif system == "windows":
            # Windows
            executable = Path("dist/pdf-zipper-gui.exe")
            if executable.exists():
                target = release_dir / f"pdf-zipper-gui-{system}-{machine}.exe"
                if target.exists():
                    target.unlink()
                shutil.move(str(executable), str(target))
                print(f"📦 创建 Windows GUI 可执行文件: {target}")
        
        else:
            # Linux
            executable = Path("dist/pdf-zipper-gui")
            if executable.exists():
                target = release_dir / f"pdf-zipper-gui-{system}-{machine}"
                if target.exists():
                    target.unlink()
                shutil.move(str(executable), str(target))
                os.chmod(target, 0o755)
                print(f"📦 创建 Linux GUI 可执行文件: {target}")
        
        print("\\n🎉 GUI 构建完成!")
        print("📁 输出文件位于 'release' 目录")
        
        # 显示文件大小
        if release_dir.exists():
            print("\\n📊 文件信息:")
            for file_path in release_dir.iterdir():
                if file_path.is_file() and 'gui' in file_path.name:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"   {file_path.name}: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI 构建失败:")
        print(f"错误输出: {e.stderr}")
        return False


if __name__ == "__main__":
    success = build_gui_executable()
    sys.exit(0 if success else 1)
