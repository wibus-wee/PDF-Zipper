#!/usr/bin/env python3
"""
PDF Zipper CLI-only 可执行文件入口点
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入并运行主程序
if __name__ == "__main__":
    from pathlib import Path
    from typing import Optional
    
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    
    from pdf_zipper.core import autocompress_pdf, compress_pdf, convert_to_ppt
    
    app = typer.Typer(
        name="pdf-zipper",
        help="🗜️ PDF Zipper - Compress PDFs and convert to PowerPoint with ease!",
        add_completion=False,
    )
    console = Console()
    
    def version_callback(value: bool):
        """Show version information."""
        if value:
            from pdf_zipper import __version__
            console.print(f"PDF Zipper v{__version__}")
            raise typer.Exit()
    
    @app.callback()
    def callback(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            callback=version_callback,
            help="Show version and exit",
        ),
    ):
        """🗜️ PDF Zipper - Compress PDFs and convert to PowerPoint with ease!"""
        pass
    
    @app.command("compress")
    def compress_command(
        input_file: Path = typer.Argument(..., help="Input PDF file"),
        output_file: Path = typer.Argument(..., help="Output PDF file"),
        target_size: Optional[float] = typer.Option(
            None, "--target-size", "-s", help="Target file size in MB (auto mode)"
        ),
        dpi: Optional[int] = typer.Option(
            None, "--dpi", "-d", help="DPI for manual compression"
        ),
    ):
        """🗜️ Compress a PDF file."""
        
        def logger(msg):
            console.print(msg)
        
        if target_size and dpi:
            console.print("❌ Cannot specify both --target-size and --dpi", style="red")
            raise typer.Exit(1)
        
        if target_size:
            # Auto compression
            autocompress_pdf(str(input_file), str(output_file), target_size, logger)
        elif dpi:
            # Manual compression
            compress_pdf(str(input_file), str(output_file), dpi, logger)
        else:
            # Default auto compression to 5MB
            autocompress_pdf(str(input_file), str(output_file), 5.0, logger)
    
    @app.command("convert")
    def convert_command(
        input_file: Path = typer.Argument(..., help="Input PDF file"),
        output_file: Path = typer.Argument(..., help="Output PowerPoint file"),
        dpi: int = typer.Option(150, "--dpi", "-d", help="DPI for conversion"),
    ):
        """📊 Convert a PDF to PowerPoint presentation."""
        
        def logger(msg):
            console.print(msg)
        
        try:
            convert_to_ppt(str(input_file), str(output_file), dpi, logger)
        except Exception as e:
            console.print(f"❌ Error converting PDF: {e}", style="red")
            raise typer.Exit(1)
    
    @app.command("info")
    def info_command(
        input_file: Path = typer.Argument(..., help="Input PDF file"),
    ):
        """📋 Show information about a PDF file."""
        try:
            import fitz
            
            if not input_file.exists():
                console.print(f"❌ File not found: {input_file}", style="red")
                raise typer.Exit(1)
            
            doc = fitz.open(str(input_file))
            file_size = input_file.stat().st_size / (1024 * 1024)
            
            info_panel = Panel.fit(
                f"""[bold]📄 PDF Information[/bold]
                
📁 File: [cyan]{input_file.name}[/cyan]
📏 Size: [yellow]{file_size:.2f} MB[/yellow]
📄 Pages: [green]{len(doc)}[/green]
🔒 Encrypted: [red]{'Yes' if doc.is_encrypted else 'No'}[/red]
📝 Title: [blue]{doc.metadata.get('title', 'N/A')}[/blue]
👤 Author: [blue]{doc.metadata.get('author', 'N/A')}[/blue]""",
                title="PDF Info",
                border_style="blue",
            )
            
            console.print(info_panel)
            doc.close()
            
        except Exception as e:
            console.print(f"❌ Error analyzing PDF: {e}", style="red")
            raise typer.Exit(1)
    
    def main():
        """Main entry point for the CLI."""
        app()
    
    main()
