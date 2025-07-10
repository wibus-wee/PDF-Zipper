"""
Command-line interface for PDF Zipper.

This module provides the CLI commands for PDF compression and conversion.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core import autocompress_pdf, compress_pdf, convert_to_ppt
from .gui import launch_gui

app = typer.Typer(
    name="pdf-zipper",
    help="🗜️ A powerful PDF compression tool with GUI and CLI interfaces",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Show version information."""
    if value:
        from . import __version__

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


@app.command("gui")
def gui_command():
    """🖥️ Launch the graphical user interface."""
    console.print("🚀 Launching PDF Zipper GUI...")
    try:
        launch_gui()
    except KeyboardInterrupt:
        console.print("\n👋 GUI closed by user")
    except Exception as e:
        console.print(f"❌ Error launching GUI: {e}", style="red")
        raise typer.Exit(1)


@app.command("compress")
def compress_command(
    input_file: Path = typer.Argument(..., help="Input PDF file path"),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    dpi: int = typer.Option(
        150, "--dpi", "-d", help="DPI for compression (default: 150)"
    ),
    target_size: Optional[float] = typer.Option(
        None, "--target-size", "-s", help="Target size in MB (auto mode)"
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
):
    """🗜️ Compress a PDF file."""

    # Validate input file
    if not input_file.exists():
        console.print(f"❌ Input file not found: {input_file}", style="red")
        raise typer.Exit(1)

    if not input_file.suffix.lower() == ".pdf":
        console.print(f"❌ Input file must be a PDF: {input_file}", style="red")
        raise typer.Exit(1)

    # Generate output filename if not provided
    if output_file is None:
        if target_size:
            output_file = input_file.with_stem(f"{input_file.stem}_auto_compressed")
        else:
            output_file = input_file.with_stem(f"{input_file.stem}_compressed")

    # Create logger function
    def logger(message: str):
        if not quiet:
            # Remove rich markup for CLI output
            clean_message = message.replace("[bold red]", "").replace("[/bold red]", "")
            clean_message = clean_message.replace("[bold green]", "").replace(
                "[/bold green]", ""
            )
            clean_message = clean_message.replace("[bold yellow]", "").replace(
                "[/bold yellow]", ""
            )
            clean_message = clean_message.replace("[green]", "").replace("[/green]", "")
            clean_message = clean_message.replace("[yellow]", "").replace(
                "[/yellow]", ""
            )
            clean_message = clean_message.replace("[cyan]", "").replace("[/cyan]", "")
            clean_message = clean_message.replace("[bold cyan]", "").replace(
                "[/bold cyan]", ""
            )
            clean_message = clean_message.replace("[bold]", "").replace("[/bold]", "")
            console.print(clean_message)

    try:
        if target_size:
            console.print(f"🎯 Auto-compressing to {target_size} MB...")
            autocompress_pdf(str(input_file), str(output_file), target_size, logger)
        else:
            console.print(f"🗜️ Compressing with {dpi} DPI...")
            compress_pdf(str(input_file), str(output_file), dpi, logger)

        if not quiet:
            console.print(f"✅ Compression complete: {output_file}", style="green")

    except Exception as e:
        console.print(f"❌ Compression failed: {e}", style="red")
        raise typer.Exit(1)


@app.command("convert")
def convert_command(
    input_file: Path = typer.Argument(..., help="Input PDF file path"),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output PowerPoint file path"
    ),
    dpi: int = typer.Option(150, "--dpi", "-d", help="DPI for images (default: 150)"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
):
    """📊 Convert a PDF to PowerPoint presentation."""

    # Validate input file
    if not input_file.exists():
        console.print(f"❌ Input file not found: {input_file}", style="red")
        raise typer.Exit(1)

    if not input_file.suffix.lower() == ".pdf":
        console.print(f"❌ Input file must be a PDF: {input_file}", style="red")
        raise typer.Exit(1)

    # Generate output filename if not provided
    if output_file is None:
        output_file = input_file.with_suffix(".pptx")

    # Create logger function
    def logger(message: str):
        if not quiet:
            # Remove rich markup for CLI output
            clean_message = message.replace("[bold red]", "").replace("[/bold red]", "")
            clean_message = clean_message.replace("[bold green]", "").replace(
                "[/bold green]", ""
            )
            clean_message = clean_message.replace("[cyan]", "").replace("[/cyan]", "")
            clean_message = clean_message.replace("[bold]", "").replace("[/bold]", "")
            console.print(clean_message)

    try:
        console.print(f"📊 Converting to PowerPoint with {dpi} DPI...")
        convert_to_ppt(str(input_file), str(output_file), dpi, logger)

        if not quiet:
            console.print(f"✅ Conversion complete: {output_file}", style="green")

    except Exception as e:
        console.print(f"❌ Conversion failed: {e}", style="red")
        raise typer.Exit(1)


@app.command("info")
def info_command(
    input_file: Path = typer.Argument(..., help="PDF file to analyze"),
):
    """📋 Show information about a PDF file."""

    if not input_file.exists():
        console.print(f"❌ File not found: {input_file}", style="red")
        raise typer.Exit(1)

    if not input_file.suffix.lower() == ".pdf":
        console.print(f"❌ File must be a PDF: {input_file}", style="red")
        raise typer.Exit(1)

    try:
        import fitz

        doc = fitz.open(str(input_file))

        file_size = input_file.stat().st_size / (1024 * 1024)  # MB
        page_count = len(doc)

        # Get first page dimensions
        first_page = doc[0]
        width_pt = first_page.rect.width
        height_pt = first_page.rect.height
        width_in = width_pt / 72
        height_in = height_pt / 72

        doc.close()

        info_text = Text()
        info_text.append("📄 PDF Information\n\n", style="bold blue")
        info_text.append(f"File: {input_file.name}\n", style="bold")
        info_text.append(f"Size: {file_size:.2f} MB\n")
        info_text.append(f"Pages: {page_count}\n")
        info_text.append(
            f'Dimensions: {width_pt:.1f} × {height_pt:.1f} pt ({width_in:.1f}" × {height_in:.1f}")\n'
        )

        panel = Panel(info_text, title="PDF Analysis", border_style="blue")
        console.print(panel)

    except Exception as e:
        console.print(f"❌ Error analyzing PDF: {e}", style="red")
        raise typer.Exit(1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
