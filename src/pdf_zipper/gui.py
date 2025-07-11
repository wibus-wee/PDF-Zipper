"""
Graphical user interface for PDF Zipper using Textual.

This module provides the TUI (Terminal User Interface) for PDF compression.
"""

import os
from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.events import Paste
from textual.validation import Number
from textual.widgets import (
    Button,
    DirectoryTree,
    Footer,
    Header,
    Input,
    Label,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from .core import (
    autocompress_pdf,
    compress_pdf,
    convert_to_ppt,
    convert_pptx_to_pdf,
    get_file_type,
    validate_input_file,
    SUPPORTED_INPUT_TYPES
)


class PDFZipperApp(App):
    """Main application class for PDF Zipper GUI."""

    CSS_PATH = None  # We'll define CSS inline
    BINDINGS = [("q", "quit", "Quit")]

    # Inline CSS
    CSS = """
    #tree-view {
        width: 30%;
        dock: left;
    }
    
    #main-view {
        width: 70%;
        dock: right;
    }
    
    #selected-file {
        height: 3;
        margin: 1;
        padding: 1;
        border: solid $primary;
    }
    
    #tabs {
        height: auto;
        margin: 1;
    }
    
    #custom-operations {
        height: 3;
        margin: 1;
    }
    
    #log {
        height: 1fr;
        margin: 1;
        border: solid $secondary;
    }
    
    Button {
        margin: 0 1;
    }
    
    Input {
        margin: 1 0;
    }
    
    Label {
        margin: 1 0 0 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the UI layout."""
        yield Header(name="🗜️ PDF Zipper")
        with Container():
            yield DirectoryTree(".", id="tree-view")
            with Vertical(id="main-view"):
                yield Static(
                    "Select a file (PDF/PPTX) from the tree or enter custom path.",
                    id="selected-file",
                )
                with TabbedContent(id="tabs"):
                    with TabPane("Custom Path", id="tab-custom"):
                        yield Label("File Path (PDF/PPTX):")
                        yield Input(
                            placeholder="输入完整文件路径，如: /Users/name/file.pdf 或 file.pptx",
                            id="custom-path",
                        )
                        with Horizontal(id="custom-operations"):
                            yield Button(
                                "Auto (5MB)", variant="primary", id="btn-custom-auto"
                            )
                            yield Button(
                                "Manual (150DPI)",
                                variant="primary",
                                id="btn-custom-manual",
                            )
                            yield Button(
                                "To PPT (150DPI)",
                                variant="primary",
                                id="btn-custom-ppt",
                            )
                    with TabPane("Auto Compress", id="tab-auto"):
                        yield Label("Target Size (MB):")
                        yield Input(
                            placeholder="e.g., 5.5",
                            id="auto-size",
                            validators=[Number(minimum=0)],
                        )
                        yield Button(
                            "Start Auto Compress", variant="primary", id="btn-auto"
                        )
                    with TabPane("Manual Compress", id="tab-manual"):
                        yield Label("Resolution (DPI):")
                        yield Input(
                            value="150",
                            id="manual-dpi",
                            validators=[Number(minimum=10)],
                        )
                        yield Button(
                            "Start Manual Compress", variant="primary", id="btn-manual"
                        )
                    with TabPane("Convert to PPT", id="tab-ppt"):
                        yield Label("Image Resolution (DPI):")
                        yield Input(
                            value="150", id="ppt-dpi", validators=[Number(minimum=10)]
                        )
                        yield Button(
                            "Start Conversion", variant="primary", id="btn-ppt"
                        )
                    with TabPane("PPTX to PDF", id="tab-pptx-pdf"):
                        yield Label("Convert PowerPoint to PDF:")
                        yield Static("Select a .pptx file and click convert")
                        yield Button(
                            "Convert to PDF", variant="primary", id="btn-pptx-pdf"
                        )
                yield RichLog(id="log", wrap=True, highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        self.query_one(DirectoryTree).focus()
        log = self.query_one(RichLog)
        log.write("Welcome to PDF Zipper!")
        log.write("💡 提示：")
        log.write("  - 从左侧文件树选择文件 (PDF/PPTX)")
        log.write("  - 或使用「Custom Path」选项卡输入/拖拽文件路径")
        log.write("  - 然后点击对应的操作按钮开始处理")
        log.write("  - 支持的文件类型: PDF (.pdf), PowerPoint (.pptx)")

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle file selection from directory tree."""
        file_path = str(event.path)
        if validate_input_file(file_path):
            ext, desc = get_file_type(file_path)
            self.query_one("#selected-file").update(
                f"Selected: [bold cyan]{event.path}[/bold cyan] ({desc})"
            )
            self.selected_path = event.path
            # 同时更新自定义路径输入框
            self.query_one("#custom-path").value = str(event.path)
        else:
            ext, desc = get_file_type(file_path)
            supported_types = ", ".join(SUPPORTED_INPUT_TYPES.keys())
            self.query_one("#selected-file").update(
                f"[bold red]Unsupported file type: {ext}. Supported: {supported_types}[/bold red]"
            )
            self.selected_path = None

    def on_paste(self, event: Paste) -> None:
        """Handle paste events for drag and drop functionality."""
        # 检查粘贴的内容是否是文件路径
        pasted_text = event.text.strip()

        # 预处理粘贴的文本，去除可能的引号
        if pasted_text:
            if (pasted_text.startswith("'") and pasted_text.endswith("'")) or (
                pasted_text.startswith('"') and pasted_text.endswith('"')
            ):
                pasted_text = pasted_text[1:-1].strip()

        if pasted_text and (
            validate_input_file(pasted_text) or os.path.exists(pasted_text)
        ):
            # 如果当前焦点在自定义路径输入框
            try:
                custom_input = self.query_one("#custom-path")
                if custom_input.has_focus:
                    custom_input.value = pasted_text
                    self._update_selected_path_from_custom()
            except Exception:
                pass

    def _update_selected_path_from_custom(self):
        """Update selected path from custom input."""
        custom_path = self.query_one("#custom-path").value.strip()

        # 处理从 Finder 拖拽时的引号包裹问题
        if custom_path:
            # 去除前后的单引号或双引号
            if (custom_path.startswith("'") and custom_path.endswith("'")) or (
                custom_path.startswith('"') and custom_path.endswith('"')
            ):
                custom_path = custom_path[1:-1]

            # 再次去除可能的空格
            custom_path = custom_path.strip()

        if custom_path and os.path.exists(custom_path) and validate_input_file(custom_path):
            ext, desc = get_file_type(custom_path)
            self.selected_path = Path(custom_path)
            self.query_one("#selected-file").update(
                f"Custom: [bold cyan]{custom_path}[/bold cyan] ({desc})"
            )
        elif custom_path:
            if os.path.exists(custom_path):
                ext, desc = get_file_type(custom_path)
                supported_types = ", ".join(SUPPORTED_INPUT_TYPES.keys())
                self.query_one("#selected-file").update(
                    f"[bold red]Unsupported file type: {ext}. Supported: {supported_types}[/bold red]"
                )
            else:
                self.query_one("#selected-file").update(
                    f"[bold red]File not found: {custom_path}[/bold red]"
                )
            self.selected_path = None
        else:
            self.query_one("#selected-file").update(
                "Select a file (PDF/PPTX) from the tree or enter custom path."
            )
            self.selected_path = None

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "custom-path":
            self._update_selected_path_from_custom()

    @work(thread=True)
    def worker_autocompress(
        self, input_path: str, output_path: str, target_size: float, logger_func
    ) -> None:
        """Worker for auto compression."""
        autocompress_pdf(input_path, output_path, target_size, logger_func)

    @work(thread=True)
    def worker_manual_compress(
        self, input_path: str, output_path: str, dpi: int, logger_func
    ) -> None:
        """Worker for manual compression."""
        compress_pdf(input_path, output_path, dpi, logger_func)

    @work(thread=True)
    def worker_convert_ppt(
        self, input_path: str, output_path: str, dpi: int, logger_func
    ) -> None:
        """Worker for PPT conversion."""
        convert_to_ppt(input_path, output_path, dpi, logger_func)

    @work(thread=True)
    def worker_convert_pptx_to_pdf(
        self, input_path: str, output_path: str, logger_func
    ) -> None:
        """Worker for PPTX to PDF conversion."""
        convert_pptx_to_pdf(input_path, output_path, logger_func)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses and dispatch jobs."""
        log = self.query_one(RichLog)
        log.clear()

        if not hasattr(self, "selected_path") or self.selected_path is None:
            log.write("[bold red]Error: No file selected.[/bold red]")
            log.write("请先选择文件：")
            log.write("  1. 从左侧文件树选择文件 (PDF/PPTX)")
            log.write("  2. 或在「Custom Path」选项卡中输入文件路径")
            return

        input_path = str(self.selected_path)
        base, ext = os.path.splitext(os.path.basename(input_path))
        input_ext, input_desc = get_file_type(input_path)

        # Common logger function
        def logger(message):
            self.call_from_thread(log.write, message)

        # Handle custom path operations (quick with defaults)
        if event.button.id == "btn-custom-auto":
            target_size = 5.0  # 默认5MB
            log.write(f"使用默认目标大小: {target_size} MB")
            output_path = f"{base}_auto_compressed.pdf"
            self.worker_autocompress(input_path, output_path, target_size, logger)

        elif event.button.id == "btn-custom-manual":
            dpi = 150  # 默认DPI
            log.write(f"使用默认DPI: {dpi}")
            output_path = f"{base}_manual_compressed.pdf"
            self.worker_manual_compress(input_path, output_path, dpi, logger)

        elif event.button.id == "btn-custom-ppt":
            dpi = 150  # 默认DPI
            log.write(f"使用默认DPI: {dpi}")
            output_path = f"{base}_converted.pptx"
            self.worker_convert_ppt(input_path, output_path, dpi, logger)

        elif event.button.id == "btn-auto":
            target_size_input = self.query_one("#auto-size", Input)
            if not target_size_input.is_valid or not target_size_input.value:
                log.write("[bold red]Error: Invalid target size.[/bold red]")
                return
            target_size = float(target_size_input.value)
            output_path = f"{base}_auto_compressed.pdf"
            self.worker_autocompress(input_path, output_path, target_size, logger)

        elif event.button.id == "btn-manual":
            dpi_input = self.query_one("#manual-dpi", Input)
            if not dpi_input.is_valid or not dpi_input.value:
                log.write("[bold red]Error: Invalid DPI value.[/bold red]")
                return
            dpi = int(dpi_input.value)
            output_path = f"{base}_manual_compressed.pdf"
            self.worker_manual_compress(input_path, output_path, dpi, logger)

        elif event.button.id == "btn-ppt":
            # PDF to PowerPoint conversion
            if input_ext != ".pdf":
                log.write("[bold red]Error: PDF to PPT conversion requires a PDF file.[/bold red]")
                return
            dpi_input = self.query_one("#ppt-dpi", Input)
            if not dpi_input.is_valid or not dpi_input.value:
                log.write("[bold red]Error: Invalid DPI value.[/bold red]")
                return
            dpi = int(dpi_input.value)
            output_path = f"{base}_converted.pptx"
            self.worker_convert_ppt(input_path, output_path, dpi, logger)

        elif event.button.id == "btn-pptx-pdf":
            # PowerPoint to PDF conversion
            if input_ext != ".pptx":
                log.write("[bold red]Error: PPTX to PDF conversion requires a PowerPoint file.[/bold red]")
                return
            output_path = f"{base}_converted.pdf"
            self.worker_convert_pptx_to_pdf(input_path, output_path, logger)


def launch_gui():
    """Launch the PDF Zipper GUI application."""
    app = PDFZipperApp()
    app.run()
