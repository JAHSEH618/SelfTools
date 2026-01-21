#!/usr/bin/env python3
"""
HTML to PNG Exporter
Exports HTML files to high-resolution PNG images using Playwright.

Usage:
    python html_to_png.py -i <input.html> -o <output.png>
    python html_to_png.py --input <input.html> --output <output.png> --scale 3
    python html_to_png.py <input.html>  # 向后兼容模式

Examples:
    python html_to_png.py -i document.html -o export.png
    python html_to_png.py --input page.html --output page.png --scale 4 --width 1600
    python html_to_png.py document.html                    # 输出: document.png
    python html_to_png.py document.html custom_output.png  # 位置参数兼容

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def html_to_png(
    html_path: str,
    output_path: str = None,
    scale_factor: int = 2,
    viewport_width: int = 1200,
    wait_time: int = 1000
):
    """
    Convert an HTML file to a high-resolution PNG image.
    
    Args:
        html_path: Path to the HTML file
        output_path: Path for the output PNG file (default: same name as HTML with .png extension)
        scale_factor: Scale factor for high resolution (default: 2, use 3 or 4 for even higher quality)
        viewport_width: Viewport width in pixels (default: 1200)
        wait_time: Wait time in ms for content rendering (default: 1000)
    """
    # 规范化输入路径
    html_path = Path(html_path).resolve()
    
    if not html_path.exists():
        print(f"❌ Error: HTML file not found: {html_path}")
        sys.exit(1)
    
    if not html_path.suffix.lower() in ['.html', '.htm']:
        print(f"⚠️  Warning: Input file may not be an HTML file: {html_path.suffix}")
    
    # 处理输出路径
    if output_path is None:
        output_path = html_path.with_suffix('.png')
    else:
        output_path = Path(output_path).resolve()
        # 如果输出是目录，则在该目录下生成同名文件
        if output_path.is_dir():
            output_path = output_path / html_path.with_suffix('.png').name
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 Input:  {html_path}")
    print(f"🖼️  Output: {output_path}")
    print(f"🔍 Scale:  {scale_factor}x | Width: {viewport_width}px")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        
        # Create context with high DPI setting for crisp rendering
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': 800},
            device_scale_factor=scale_factor
        )
        
        page = await context.new_page()
        
        # Load the HTML file
        file_url = html_path.as_uri()
        await page.goto(file_url, wait_until='networkidle')
        
        # Wait for content to be fully rendered
        await page.wait_for_timeout(wait_time)
        
        # Get the full page height
        page_height = await page.evaluate('document.body.scrollHeight')
        
        # Resize viewport to capture full page
        await page.set_viewport_size({'width': viewport_width, 'height': page_height})
        
        # Wait for any reflow
        await page.wait_for_timeout(500)
        
        # Take high-resolution screenshot
        await page.screenshot(
            path=str(output_path),
            full_page=True,
            type='png'
        )
        
        await browser.close()
    
    # 获取文件大小
    file_size = output_path.stat().st_size
    size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / 1024 / 1024:.2f} MB"
    
    print(f"\n✅ Successfully exported!")
    print(f"   📁 File: {output_path}")
    print(f"   📊 Size: {size_str}")
    print(f"   🎨 Resolution: {scale_factor}x ({viewport_width * scale_factor}px effective width)")


def parse_args():
    """Parse command line arguments with support for both flag-based and positional arguments."""
    parser = argparse.ArgumentParser(
        description='HTML to PNG Exporter - Convert HTML files to high-resolution PNG images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -i document.html -o export.png
  %(prog)s --input page.html --output ./exports/page.png --scale 3
  %(prog)s document.html                    # 输出同目录下的 document.png
  %(prog)s document.html custom.png 4       # 位置参数兼容模式
        '''
    )
    
    # 命名参数
    parser.add_argument(
        '-i', '--input',
        type=str,
        dest='input_file',
        help='Input HTML file path'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        dest='output_file',
        help='Output PNG file path (default: same name as input with .png extension)'
    )
    parser.add_argument(
        '-s', '--scale',
        type=int,
        default=2,
        help='Scale factor for resolution (default: 2, use 3-4 for higher quality)'
    )
    parser.add_argument(
        '-w', '--width',
        type=int,
        default=1200,
        help='Viewport width in pixels (default: 1200)'
    )
    parser.add_argument(
        '--wait',
        type=int,
        default=1000,
        help='Wait time in milliseconds for content rendering (default: 1000)'
    )
    
    # 位置参数（向后兼容）
    parser.add_argument(
        'positional_args',
        nargs='*',
        help=argparse.SUPPRESS  # 隐藏帮助信息，保持命令行简洁
    )
    
    args = parser.parse_args()
    
    # 处理参数优先级: 命名参数 > 位置参数
    input_file = args.input_file
    output_file = args.output_file
    scale = args.scale
    
    if args.positional_args:
        if not input_file and len(args.positional_args) >= 1:
            input_file = args.positional_args[0]
        if not output_file and len(args.positional_args) >= 2:
            output_file = args.positional_args[1]
        if len(args.positional_args) >= 3:
            try:
                scale = int(args.positional_args[2])
            except ValueError:
                pass
    
    if not input_file:
        parser.print_help()
        print("\n❌ Error: Input file is required. Use -i/--input or provide as first positional argument.")
        sys.exit(1)
    
    return input_file, output_file, scale, args.width, args.wait


def main():
    input_file, output_file, scale, width, wait = parse_args()
    asyncio.run(html_to_png(input_file, output_file, scale, width, wait))


if __name__ == "__main__":
    main()
