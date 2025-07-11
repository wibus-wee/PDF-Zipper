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

from .core import (
    autocompress,
    autocompress_pdf,
    compress_pdf,
    convert_to_ppt,
    convert_pptx_to_pdf,
    get_file_type,
    validate_input_file,
    SUPPORTED_INPUT_TYPES
)
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
    input_file: Path = typer.Argument(..., help="Input file path (PDF or PPTX)"),
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
    """🗜️ Compress a file (supports PDF and PPTX)."""

    # Validate input file
    if not input_file.exists():
        console.print(f"❌ Input file not found: {input_file}", style="red")
        raise typer.Exit(1)

    # Check file type
    if not validate_input_file(str(input_file)):
        ext, desc = get_file_type(str(input_file))
        supported_types = ", ".join(SUPPORTED_INPUT_TYPES.keys())
        console.print(f"❌ Unsupported file type: {ext}", style="red")
        console.print(f"💡 Supported types: {supported_types}", style="yellow")
        raise typer.Exit(1)

    # Get file type info
    input_ext, input_desc = get_file_type(str(input_file))

    # Generate output filename if not provided
    if output_file is None:
        if input_ext == ".pptx":
            if target_size:
                # For PPTX auto-compression, keep PPTX format
                output_file = input_file.with_stem(f"{input_file.stem}_auto_compressed")
            else:
                # For PPTX manual compression (conversion), default output is PDF
                output_file = input_file.with_suffix(".pdf")
        else:
            # For PDF input, add appropriate suffix
            if target_size:
                # Default to same format for auto-compression
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
            # Auto-compression mode (supports both PDF and PPTX)
            console.print(f"🎯 Auto-compressing to {target_size} MB...")
            autocompress(str(input_file), str(output_file), target_size, logger)
        elif input_ext == ".pptx":
            # PPTX to PDF conversion (manual mode)
            console.print(f"📊 Converting PPTX to PDF...")
            convert_pptx_to_pdf(str(input_file), str(output_file), logger)
        else:
            # PDF manual compression
            console.print(f"🗜️ Compressing with {dpi} DPI...")
            compress_pdf(str(input_file), str(output_file), dpi, logger)

        if not quiet:
            console.print(f"✅ Processing complete: {output_file}", style="green")

    except Exception as e:
        console.print(f"❌ Processing failed: {e}", style="red")
        raise typer.Exit(1)


@app.command("convert")
def convert_command(
    input_file: Path = typer.Argument(..., help="Input file path (PDF or PPTX)"),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    dpi: int = typer.Option(150, "--dpi", "-d", help="DPI for images (default: 150)"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
):
    """📊 Convert between PDF and PowerPoint formats."""

    # Validate input file
    if not input_file.exists():
        console.print(f"❌ Input file not found: {input_file}", style="red")
        raise typer.Exit(1)

    # Check file type
    if not validate_input_file(str(input_file)):
        ext, desc = get_file_type(str(input_file))
        supported_types = ", ".join(SUPPORTED_INPUT_TYPES.keys())
        console.print(f"❌ Unsupported file type: {ext}", style="red")
        console.print(f"💡 Supported types: {supported_types}", style="yellow")
        raise typer.Exit(1)

    # Get file type info
    input_ext, input_desc = get_file_type(str(input_file))

    # Generate output filename if not provided
    if output_file is None:
        if input_ext == ".pdf":
            # PDF to PPTX
            output_file = input_file.with_suffix(".pptx")
        elif input_ext == ".pptx":
            # PPTX to PDF
            output_file = input_file.with_suffix(".pdf")

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
        if input_ext == ".pdf":
            # PDF to PowerPoint
            console.print(f"📊 Converting PDF to PowerPoint with {dpi} DPI...")
            convert_to_ppt(str(input_file), str(output_file), dpi, logger)
        elif input_ext == ".pptx":
            # PowerPoint to PDF
            console.print(f"📄 Converting PowerPoint to PDF...")
            convert_pptx_to_pdf(str(input_file), str(output_file), logger)

        if not quiet:
            console.print(f"✅ Conversion complete: {output_file}", style="green")

    except Exception as e:
        console.print(f"❌ Conversion failed: {e}", style="red")
        raise typer.Exit(1)


@app.command("info")
def info_command(
    input_file: Path = typer.Argument(..., help="File to analyze (PDF or PPTX)"),
):
    """📋 Show information about a file."""

    if not input_file.exists():
        console.print(f"❌ File not found: {input_file}", style="red")
        raise typer.Exit(1)

    # Check file type
    if not validate_input_file(str(input_file)):
        ext, desc = get_file_type(str(input_file))
        supported_types = ", ".join(SUPPORTED_INPUT_TYPES.keys())
        console.print(f"❌ Unsupported file type: {ext}", style="red")
        console.print(f"💡 Supported types: {supported_types}", style="yellow")
        raise typer.Exit(1)

    # Get file type info
    input_ext, input_desc = get_file_type(str(input_file))
    file_size = input_file.stat().st_size / (1024 * 1024)  # MB

    try:
        if input_ext == ".pdf":
            # Analyze PDF file
            import fitz
            doc = fitz.open(str(input_file))
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

        elif input_ext == ".pptx":
            # Analyze PPTX file
            from pptx import Presentation
            prs = Presentation(str(input_file))
            slide_count = len(prs.slides)

            # Get slide dimensions
            width_in = prs.slide_width.inches
            height_in = prs.slide_height.inches
            width_pt = prs.slide_width.pt
            height_pt = prs.slide_height.pt

            info_text = Text()
            info_text.append("📊 PowerPoint Information\n\n", style="bold green")
            info_text.append(f"File: {input_file.name}\n", style="bold")
            info_text.append(f"Size: {file_size:.2f} MB\n")
            info_text.append(f"Slides: {slide_count}\n")
            info_text.append(
                f'Dimensions: {width_pt:.1f} × {height_pt:.1f} pt ({width_in:.1f}" × {height_in:.1f}")\n'
            )

            panel = Panel(info_text, title="PowerPoint Analysis", border_style="green")
            console.print(panel)

    except Exception as e:
        console.print(f"❌ Error analyzing file: {e}", style="red")
        raise typer.Exit(1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
