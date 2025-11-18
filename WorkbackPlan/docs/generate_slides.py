#!/usr/bin/env python3
"""
Generate enterprise-grade LibreOffice Impress presentation from markdown slide outline.

Author: Chin-Yew Lin
Created: November 17, 2025

Requirements:
- LibreOffice installed at /Applications/LibreOffice.app
- Python 3.8+

Usage:
    python generate_slides.py input.md output.odp [--enterprise]
    python generate_slides.py input.md output.pptx [--enterprise]
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict


def parse_markdown_slides(md_file):
    """
    Parse markdown file into slide structure.
    
    Returns:
        list of dict: Each dict has 'title', 'content', 'type'
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = []
    current_slide = None
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip metadata and front matter
        if line.startswith('**') and 'Author' in line or 'Created' in line or 'Format' in line:
            i += 1
            continue
        
        # Slide separator (---) or ## Slide
        if line.startswith('---') or line.startswith('## Slide'):
            if current_slide:
                slides.append(current_slide)
            current_slide = {'title': '', 'content': [], 'type': 'content'}
            i += 1
            continue
        
        # Title line (next non-empty after separator, or **Title:** format)
        if current_slide and not current_slide['title']:
            if line.startswith('**') and line.endswith('**'):
                # Format: **Title:**
                title = line.strip('*').strip(':').strip()
                current_slide['title'] = title
                i += 1
                continue
            elif line and not line.startswith('---'):
                current_slide['title'] = line
                i += 1
                continue
        
        # Content
        if current_slide and line:
            current_slide['content'].append(line)
        
        i += 1
    
    # Add last slide
    if current_slide:
        slides.append(current_slide)
    
    return slides


def create_enterprise_html_presentation(slides, output_file):
    """
    Create enterprise-grade HTML presentation that can be converted to ODP/PPTX.
    """
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Project Management Agent: PFT + RFT</title>
    <style>
        @page {
            size: 10in 7.5in;
            margin: 0;
        }
        body {
            font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: white;
        }
        .slide {
            page-break-after: always;
            width: 10in;
            height: 7.5in;
            padding: 0;
            box-sizing: border-box;
            position: relative;
            background: white;
        }
        
        /* Title Slide */
        .slide.title-slide {
            background: linear-gradient(135deg, #0078D4 0%, #005A9E 100%);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 80px;
        }
        .slide.title-slide h1 {
            font-size: 56px;
            margin: 0 0 30px 0;
            font-weight: 700;
            line-height: 1.2;
        }
        .slide.title-slide .subtitle {
            font-size: 28px;
            margin: 20px 0;
            font-weight: 300;
            line-height: 1.4;
        }
        .slide.title-slide .key-message {
            font-size: 22px;
            margin-top: 40px;
            padding: 25px 30px;
            background: rgba(255,255,255,0.15);
            border-left: 5px solid white;
            font-weight: 400;
            line-height: 1.5;
        }
        
        /* Content Slide */
        .slide.content-slide {
            padding: 50px 70px 60px 70px;
        }
        .slide.content-slide::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
            background: linear-gradient(90deg, #0078D4 0%, #00BCF2 100%);
        }
        .slide.content-slide h2 {
            font-size: 40px;
            margin: 0 0 35px 0;
            color: #0078D4;
            font-weight: 600;
            line-height: 1.2;
        }
        
        /* Content Area */
        .content {
            font-size: 20px;
            line-height: 1.7;
            color: #323130;
        }
        .content ul {
            margin: 15px 0;
            padding-left: 25px;
            list-style: none;
        }
        .content ul li {
            margin: 12px 0;
            padding-left: 30px;
            position: relative;
        }
        .content ul li::before {
            content: '▸';
            position: absolute;
            left: 0;
            color: #0078D4;
            font-weight: bold;
            font-size: 20px;
        }
        .content ul ul {
            margin: 8px 0;
            padding-left: 20px;
        }
        .content ul ul li {
            font-size: 18px;
            margin: 8px 0;
        }
        .content ul ul li::before {
            content: '•';
            font-size: 16px;
        }
        .content strong {
            color: #0078D4;
            font-weight: 600;
        }
        .content p {
            margin: 15px 0;
        }
        
        /* Special Boxes */
        .emphasis, .outcome, .opportunity {
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 19px;
            line-height: 1.6;
        }
        .emphasis {
            background: #F3F2F1;
            border-left: 5px solid #0078D4;
        }
        .outcome {
            background: #E6F7E6;
            border-left: 5px solid #107C10;
            font-weight: 500;
        }
        .opportunity {
            background: #FFF4CE;
            border-left: 5px solid #FFB900;
            font-weight: 500;
        }
        
        /* Section Headers */
        .section-header {
            font-size: 22px;
            color: #0078D4;
            font-weight: 600;
            margin: 25px 0 15px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Slide Footer */
        .slide-footer {
            position: absolute;
            bottom: 20px;
            right: 70px;
            font-size: 14px;
            color: #605E5C;
        }
        
        /* Code/Technical Blocks */
        .code-block {
            background: #F5F5F5;
            border: 1px solid #D1D1D1;
            padding: 15px 20px;
            margin: 15px 0;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 16px;
            border-radius: 4px;
            line-height: 1.5;
        }
        
        /* Visual Indicator */
        .visual-note {
            font-style: italic;
            color: #605E5C;
            font-size: 16px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
"""
    
    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        
        if idx == 0:
            # Title slide
            html += '    <div class="slide title-slide">\n'
            html += f'        <h1>{slide["title"]}</h1>\n'
            for line in slide['content']:
                if line.startswith('**Subtitle:**'):
                    subtitle = line.replace('**Subtitle:**', '').strip()
                    html += f'        <div class="subtitle">{subtitle}</div>\n'
                elif line.startswith('**Key Message:**'):
                    msg = line.replace('**Key Message:**', '').strip()
                    html += f'        <div class="key-message">{msg}</div>\n'
            html += '    </div>\n\n'
        else:
            # Content slide
            html += '    <div class="slide content-slide">\n'
            html += f'        <h2>{slide["title"]}</h2>\n'
            html += '        <div class="content">\n'
            
            in_list = False
            in_nested_list = False
            
            for line in slide['content']:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Nested list items (starts with spaces/tabs)
                if line.startswith('  ') and (line.strip().startswith('-') or line.strip().startswith('*')):
                    if not in_nested_list:
                        html += '                <ul>\n'
                        in_nested_list = True
                    item = line.strip()[2:].strip()
                    item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
                    html += f'                    <li>{item}</li>\n'
                    continue
                elif in_nested_list:
                    html += '                </ul>\n'
                    in_nested_list = False
                
                # Main list items
                if line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
                    if not in_list:
                        html += '            <ul>\n'
                        in_list = True
                    item = re.sub(r'^[•\-*]\s+', '', line).strip()
                    item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
                    html += f'                <li>{item}</li>\n'
                
                # Special boxes
                elif line.startswith('**Outcome:**'):
                    if in_list:
                        html += '            </ul>\n'
                        in_list = False
                    msg = line.replace('**Outcome:**', '').strip()
                    msg = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', msg)
                    html += f'            <div class="outcome"><strong>Outcome:</strong> {msg}</div>\n'
                
                elif line.startswith('**Opportunity:**'):
                    if in_list:
                        html += '            </ul>\n'
                        in_list = False
                    msg = line.replace('**Opportunity:**', '').strip()
                    msg = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', msg)
                    html += f'            <div class="opportunity"><strong>Opportunity:</strong> {msg}</div>\n'
                
                # Section headers (e.g., "Four main layers:")
                elif line.endswith(':') and not line.startswith('-'):
                    if in_list:
                        html += '            </ul>\n'
                        in_list = False
                    header = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
                    html += f'            <div class="section-header">{header}</div>\n'
                
                # Visual notes (in parentheses or italics)
                elif line.startswith('*(') or line.startswith('(Visual:'):
                    if in_list:
                        html += '            </ul>\n'
                        in_list = False
                    note = line.strip('*()').strip()
                    html += f'            <div class="visual-note">{note}</div>\n'
                
                # Regular paragraphs
                elif line and not line.startswith('---'):
                    if in_list:
                        html += '            </ul>\n'
                        in_list = False
                    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
                    html += f'            <p>{line}</p>\n'
            
            if in_nested_list:
                html += '                </ul>\n'
            if in_list:
                html += '            </ul>\n'
            
            html += '        </div>\n'
            html += f'        <div class="slide-footer">{slide_num}</div>\n'
            html += '    </div>\n\n'
    
    html += """</body>
</html>"""
    
    output_file.write_text(html, encoding='utf-8')
    print(f"✓ Created HTML: {output_file}")


def convert_to_presentation(html_file, output_file):
    """
    Convert HTML to ODP or PPTX using LibreOffice.
    """
    soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    
    if not os.path.exists(soffice):
        print("ERROR: LibreOffice not found at /Applications/LibreOffice.app")
        return False
    
    # Determine output format
    output_ext = output_file.suffix.lower()
    if output_ext == '.odp':
        filter_name = 'impress8'
    elif output_ext == '.pptx':
        filter_name = 'Impress MS PowerPoint 2007 XML'
    else:
        print(f"ERROR: Unsupported output format: {output_ext}")
        return False
    
    # Convert using LibreOffice headless mode
    cmd = [
        soffice,
        '--headless',
        '--convert-to', f'{output_ext[1:]}:{filter_name}',
        '--outdir', str(output_file.parent),
        str(html_file)
    ]
    
    print(f"Converting to {output_ext.upper()}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # LibreOffice converts with same basename
        converted = output_file.parent / f"{html_file.stem}{output_ext}"
        if converted.exists() and converted != output_file:
            converted.rename(output_file)
        print(f"✓ Created presentation: {output_file}")
        return True
    else:
        print(f"ERROR: Conversion failed")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_slides.py input.md [output.odp|output.pptx]")
        print("\nExample:")
        print("  python generate_slides.py PFT_RFT_PM_Agent_Slides.md presentation.odp")
        print("  python generate_slides.py PFT_RFT_PM_Agent_Slides.md presentation.pptx")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)
    
    # Default output
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_suffix('.odp')
    
    print(f"Reading slides from: {input_file}")
    
    # Parse markdown
    slides = parse_markdown_slides(input_file)
    print(f"✓ Parsed {len(slides)} slides")
    
    # Create HTML intermediate
    html_file = input_file.with_suffix('.tmp.html')
    create_enterprise_html_presentation(slides, html_file)
    
    # Convert to presentation format
    success = convert_to_presentation(html_file, output_file)
    
    # Cleanup
    if html_file.exists():
        html_file.unlink()
    
    if success:
        print(f"\n✓ SUCCESS! Presentation created: {output_file}")
        print(f"\nOpen with: open '{output_file}'")
    else:
        print("\n✗ FAILED to create presentation")
        sys.exit(1)


if __name__ == '__main__':
    main()
