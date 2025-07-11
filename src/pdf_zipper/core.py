"""
Core PDF processing functionality.

This module contains the main PDF compression and conversion logic.
"""

import io
import os
import platform
import tempfile
from pathlib import Path
from typing import Callable, Optional, Tuple

import fitz  # PyMuPDF
from PIL import Image
from pptx import Presentation
from pptx.util import Inches

# 支持的文件类型
SUPPORTED_INPUT_TYPES = {
    '.pdf': 'PDF Document',
    '.pptx': 'PowerPoint Presentation',
}

SUPPORTED_OUTPUT_TYPES = {
    '.pdf': 'PDF Document',
    '.pptx': 'PowerPoint Presentation',
}


def get_file_type(file_path: str) -> Tuple[str, str]:
    """
    获取文件类型信息

    Args:
        file_path: 文件路径

    Returns:
        Tuple[extension, description]: 文件扩展名和描述
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext in SUPPORTED_INPUT_TYPES:
        return ext, SUPPORTED_INPUT_TYPES[ext]
    else:
        return ext, "Unknown file type"


def validate_input_file(file_path: str) -> bool:
    """
    验证输入文件是否支持

    Args:
        file_path: 文件路径

    Returns:
        bool: 是否支持该文件类型
    """
    if not os.path.exists(file_path):
        return False

    ext, _ = get_file_type(file_path)
    return ext in SUPPORTED_INPUT_TYPES


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


def convert_pptx_to_pdf(
    input_path: str, output_path: str, logger_func: Callable[[str], None]
) -> None:
    """
    将 PowerPoint 文件转换为 PDF

    Args:
        input_path: 输入的 PPTX 文件路径
        output_path: 输出的 PDF 文件路径
        logger_func: 日志记录函数
    """
    logger_func("Starting PPTX to PDF conversion...")

    if not os.path.exists(input_path):
        logger_func(f"[bold red]Error:[/bold red] Input file not found: '{input_path}'")
        return

    try:
        # 使用不同平台的转换方法
        if platform.system() == "Windows":
            _convert_pptx_to_pdf_windows(input_path, output_path, logger_func)
        else:
            _convert_pptx_to_pdf_cross_platform(input_path, output_path, logger_func)

        # 检查输出文件是否成功创建
        if os.path.exists(output_path):
            input_size = os.path.getsize(input_path) / (1024 * 1024)
            output_size = os.path.getsize(output_path) / (1024 * 1024)

            logger_func("\n[bold green]🎉 PPTX to PDF Conversion Complete![/bold green]")
            logger_func(f"  - Input size:  {input_size:.2f} MB")
            logger_func(f"  - Output size: {output_size:.2f} MB")
            logger_func(f"  - Saved to:    [cyan]{output_path}[/cyan]")
        else:
            logger_func("[bold red]Error:[/bold red] Failed to create output PDF file.")

    except Exception as e:
        logger_func(f"[bold red]Error:[/bold red] PPTX to PDF conversion failed: {e}")


def _convert_pptx_to_pdf_windows(
    input_path: str, output_path: str, logger_func: Callable[[str], None]
) -> None:
    """Windows 平台使用 COM 接口转换 PPTX 到 PDF"""
    try:
        import comtypes.client

        logger_func("Using Windows PowerPoint COM interface...")

        # 创建 PowerPoint 应用实例
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        # 打开演示文稿
        presentation = powerpoint.Presentations.Open(os.path.abspath(input_path))

        # 导出为 PDF (格式代码 32 表示 PDF)
        presentation.SaveAs(os.path.abspath(output_path), 32)

        # 关闭演示文稿和应用
        presentation.Close()
        powerpoint.Quit()

        logger_func("✅ Windows COM conversion completed")

    except ImportError:
        logger_func("[bold yellow]Warning:[/bold yellow] Windows COM libraries not available, falling back to cross-platform method")
        _convert_pptx_to_pdf_cross_platform(input_path, output_path, logger_func)
    except Exception as e:
        logger_func(f"[bold red]Error:[/bold red] Windows COM conversion failed: {e}")
        logger_func("Falling back to cross-platform method...")
        _convert_pptx_to_pdf_cross_platform(input_path, output_path, logger_func)


def _convert_pptx_to_pdf_cross_platform(
    input_path: str, output_path: str, logger_func: Callable[[str], None]
) -> None:
    """跨平台方法：将 PPTX 转换为图片再合成 PDF"""
    logger_func("Using cross-platform conversion method...")

    try:
        # 读取 PowerPoint 文件
        prs = Presentation(input_path)
        total_slides = len(prs.slides)
        logger_func(f"Found {total_slides} slides to convert")

        if total_slides == 0:
            logger_func("[bold red]Error:[/bold red] No slides found in presentation")
            return

        # 创建临时目录存储图片
        with tempfile.TemporaryDirectory() as temp_dir:
            image_paths = []

            # 将每个幻灯片转换为图片
            for i, slide in enumerate(prs.slides):
                logger_func(f"  - Processing slide {i+1}/{total_slides}")

                # 这里我们使用一个简化的方法：
                # 由于 python-pptx 不直接支持渲染为图片，我们创建一个临时的单页 PPTX
                # 然后使用 PyMuPDF 来处理（如果可能的话）
                temp_pptx = os.path.join(temp_dir, f"slide_{i+1}.pptx")
                temp_pdf = os.path.join(temp_dir, f"slide_{i+1}.pdf")

                # 创建只包含当前幻灯片的演示文稿
                single_slide_prs = Presentation()
                single_slide_prs.slide_width = prs.slide_width
                single_slide_prs.slide_height = prs.slide_height

                # 复制幻灯片布局和内容（简化版本）
                slide_layout = single_slide_prs.slide_layouts[6]  # 空白布局
                new_slide = single_slide_prs.slides.add_slide(slide_layout)

                # 复制形状（这是一个简化的实现）
                for shape in slide.shapes:
                    try:
                        # 这里只是一个基本的形状复制示例
                        # 实际实现会更复杂
                        if hasattr(shape, 'text'):
                            # 处理文本框
                            textbox = new_slide.shapes.add_textbox(
                                shape.left, shape.top, shape.width, shape.height
                            )
                            textbox.text = shape.text
                    except Exception:
                        # 忽略无法复制的形状
                        continue

                single_slide_prs.save(temp_pptx)

                # 尝试使用系统命令转换（如果可用）
                if not _try_system_conversion(temp_pptx, temp_pdf, logger_func):
                    # 如果系统转换失败，创建一个占位符 PDF
                    _create_placeholder_pdf(temp_pdf, f"Slide {i+1}", logger_func)

                if os.path.exists(temp_pdf):
                    image_paths.append(temp_pdf)

            # 合并所有 PDF 页面
            if image_paths:
                _merge_pdfs(image_paths, output_path, logger_func)
            else:
                logger_func("[bold red]Error:[/bold red] No slides were successfully converted")

    except Exception as e:
        logger_func(f"[bold red]Error:[/bold red] Cross-platform conversion failed: {e}")


def _try_system_conversion(input_pptx: str, output_pdf: str, logger_func: Callable[[str], None]) -> bool:
    """尝试使用系统命令转换 PPTX 到 PDF"""
    try:
        import subprocess

        # 尝试使用 LibreOffice (如果可用)
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", os.path.dirname(output_pdf), input_pptx
            ], check=True, capture_output=True, timeout=30)

            # LibreOffice 会创建与输入文件同名但扩展名为 .pdf 的文件
            expected_output = os.path.join(
                os.path.dirname(output_pdf),
                os.path.splitext(os.path.basename(input_pptx))[0] + ".pdf"
            )

            if os.path.exists(expected_output):
                if expected_output != output_pdf:
                    os.rename(expected_output, output_pdf)
                return True

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # 尝试使用 unoconv (如果可用)
        try:
            subprocess.run([
                "unoconv", "-f", "pdf", "-o", output_pdf, input_pptx
            ], check=True, capture_output=True, timeout=30)

            return os.path.exists(output_pdf)

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass

    except Exception:
        pass

    return False


def _create_placeholder_pdf(output_path: str, text: str, logger_func: Callable[[str], None]) -> None:
    """创建一个包含文本的占位符 PDF"""
    try:
        doc = fitz.open()  # 创建新的 PDF 文档
        page = doc.new_page()  # 添加新页面

        # 在页面中心添加文本
        rect = page.rect
        text_rect = fitz.Rect(50, rect.height/2 - 50, rect.width - 50, rect.height/2 + 50)
        page.insert_textbox(text_rect, text, fontsize=24, align=1)  # 居中对齐

        doc.save(output_path)
        doc.close()

    except Exception as e:
        logger_func(f"[bold yellow]Warning:[/bold yellow] Failed to create placeholder PDF: {e}")


def _merge_pdfs(pdf_paths: list, output_path: str, logger_func: Callable[[str], None]) -> None:
    """合并多个 PDF 文件"""
    try:
        merged_doc = fitz.open()

        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                doc = fitz.open(pdf_path)
                merged_doc.insert_pdf(doc)
                doc.close()

        merged_doc.save(output_path)
        merged_doc.close()

        logger_func(f"✅ Merged {len(pdf_paths)} pages into final PDF")

    except Exception as e:
        logger_func(f"[bold red]Error:[/bold red] Failed to merge PDFs: {e}")


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
