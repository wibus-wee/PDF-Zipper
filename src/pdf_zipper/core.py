"""
Core PDF processing functionality.

This module contains the main PDF compression and conversion logic.
"""

import io
import os
from typing import Callable, Optional

import fitz  # PyMuPDF
from PIL import Image
from pptx import Presentation
from pptx.util import Inches


def _generate_pdf_data(
    doc: fitz.Document, dpi: float, logger_func: Callable[[str], None]
) -> Optional[bytes]:
    """Generates PDF data in memory and logs progress."""
    image_list = []
    total_pages = len(doc)
    logger_func(f"Converting {total_pages} pages with DPI {int(dpi)}...")

    for i, page in enumerate(doc):
        try:
            pix = page.get_pixmap(dpi=int(dpi))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_list.append(img)
            if (i + 1) % 10 == 0 or i + 1 == total_pages:
                logger_func(f"  - Converted page {i+1}/{total_pages}")
        except Exception as e:
            logger_func(
                f"[bold red]Warning:[/bold red] Error processing page {i+1}, skipped. Error: {e}"
            )
            continue

    if not image_list:
        logger_func(
            "[bold red]Error:[/bold red] No images were generated from the PDF."
        )
        return None

    logger_func("Saving PDF data to memory buffer...")
    pdf_buffer = io.BytesIO()
    image_list[0].save(
        pdf_buffer,
        "PDF",
        resolution=float(dpi),
        save_all=True,
        append_images=image_list[1:],
    )
    logger_func("[green]In-memory save complete.[/green]")
    return pdf_buffer.getvalue()


def autocompress_pdf(
    input_path: str,
    output_path: str,
    target_size_mb: float,
    logger_func: Callable[[str], None],
    tolerance: float = 0.05,
) -> None:
    """Automatically adjusts DPI to compress a PDF to a target size."""
    if not os.path.exists(input_path):
        logger_func(f"[bold red]Error:[/bold red] Input file not found: '{input_path}'")
        return

    original_size_mb = os.path.getsize(input_path) / (1024 * 1024)
    if original_size_mb <= target_size_mb:
        logger_func(
            "[bold yellow]Info:[/bold yellow] Target size is not smaller than the original. Copying file directly."
        )
        import shutil

        shutil.copy(input_path, output_path)
        return

    logger_func("Starting auto-compression...")
    logger_func(f" - Original Size: {original_size_mb:.2f} MB")
    logger_func(f" - Target Size:   {target_size_mb:.2f} MB")

    try:
        doc = fitz.open(input_path)
    except Exception as e:
        logger_func(f"[bold red]Error:[/bold red] Could not open PDF. Reason: {e}")
        return

    dpi_low, dpi_high = 30, 300
    best_dpi, best_pdf_data = dpi_low, None

    ITERATIONS = 7
    logger_func(f"Starting iterative search for best DPI ({ITERATIONS} iterations)...")

    for i in range(ITERATIONS):
        dpi_guess = (dpi_low + dpi_high) / 2
        if dpi_guess < dpi_low + 1:
            break

        logger_func(
            f"\n[bold]Attempt {i + 1}/{ITERATIONS}:[/bold] Trying DPI = {int(dpi_guess)}"
        )
        pdf_data = _generate_pdf_data(doc, dpi_guess, logger_func)

        if not pdf_data:
            logger_func(
                f"[yellow]Failed to generate PDF at DPI {int(dpi_guess)}.[/yellow]"
            )
            dpi_high = dpi_guess
            continue

        current_size_mb = len(pdf_data) / (1024 * 1024)
        logger_func(f"  - Generated size: {current_size_mb:.2f} MB")

        if abs(current_size_mb - target_size_mb) / target_size_mb <= tolerance:
            logger_func("[green]Result is within tolerance. Search finished.[/green]")
            best_dpi, best_pdf_data = dpi_guess, pdf_data
            break

        if current_size_mb > target_size_mb:
            dpi_high = dpi_guess
        else:
            dpi_low = dpi_guess
            best_dpi, best_pdf_data = dpi_guess, pdf_data

    doc.close()

    if best_pdf_data is None:
        logger_func(
            "[yellow]Search finished without a perfect match. Regenerating with best found DPI...[/yellow]"
        )
        doc = fitz.open(input_path)
        best_pdf_data = _generate_pdf_data(doc, best_dpi, logger_func)
        doc.close()

    if not best_pdf_data:
        logger_func("[bold red]Error:[/bold red] Failed to generate final PDF.")
        return

    logger_func(
        f"\nSearch complete. Best DPI found: [bold cyan]{int(best_dpi)}[/bold cyan]. Saving file..."
    )
    with open(output_path, "wb") as f:
        f.write(best_pdf_data)

    final_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    ratio = (1 - final_size_mb / original_size_mb) * 100 if original_size_mb > 0 else 0

    logger_func("\n[bold green]🎉 Auto-compression Complete![/bold green]")
    logger_func(f"  - Original size: {original_size_mb:.2f} MB")
    logger_func(
        f"  - Final size:    {final_size_mb:.2f} MB (Target: {target_size_mb:.2f} MB)"
    )
    logger_func(f"  - Compression:   {ratio:.2f}%")
    logger_func(f"  - Saved to:      [cyan]{output_path}[/cyan]")


def compress_pdf(
    input_path: str, output_path: str, dpi: int, logger_func: Callable[[str], None]
) -> None:
    """Manually compresses a PDF using a specific DPI."""
    logger_func("Starting manual compression...")
    doc = fitz.open(input_path)
    pdf_data = _generate_pdf_data(doc, dpi, logger_func)
    doc.close()

    if pdf_data:
        with open(output_path, "wb") as f:
            f.write(pdf_data)

        original_size = os.path.getsize(input_path) / (1024 * 1024)
        final_size = os.path.getsize(output_path) / (1024 * 1024)
        ratio = (1 - final_size / original_size) * 100 if original_size > 0 else 0

        logger_func("\n[bold green]🎉 Manual Compression Complete![/bold green]")
        logger_func(f"  - Original size: {original_size:.2f} MB")
        logger_func(f"  - Final size:    {final_size:.2f} MB")
        logger_func(f"  - Compression:   {ratio:.2f}%")
        logger_func(f"  - Saved to:      [cyan]{output_path}[/cyan]")


def convert_to_ppt(
    input_path: str, output_path: str, dpi: int, logger_func: Callable[[str], None]
) -> None:
    """Converts a PDF to a PowerPoint presentation."""
    logger_func("Starting PDF to PPT conversion...")
    doc = fitz.open(input_path)
    prs = Presentation()
    total_pages = len(doc)

    for i, page in enumerate(doc):
        logger_func(f"  - Processing page {i+1}/{total_pages}")
        pix = page.get_pixmap(dpi=int(dpi))
        img_data = pix.tobytes("png")

        prs.slide_width = Inches(page.rect.width / 72)
        prs.slide_height = Inches(page.rect.height / 72)
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(
            io.BytesIO(img_data), 0, 0, width=prs.slide_width, height=prs.slide_height
        )

    doc.close()
    prs.save(output_path)
    logger_func("\n[bold green]🎉 Conversion Complete![/bold green]")
    logger_func(f"  - Saved to: [cyan]{output_path}[/cyan]")
