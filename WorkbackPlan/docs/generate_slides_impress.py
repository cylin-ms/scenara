#!/usr/bin/env python3
"""
Generate professional presentation using LibreOffice Impress directly via UNO API.

Author: Chin-Yew Lin
Created: November 17, 2025

Requirements:
- LibreOffice installed at /Applications/LibreOffice.app
- Python 3.8+

Usage:
    python generate_slides_impress.py input.md output.odp
"""

import sys
import os
import re
import subprocess
import time
from pathlib import Path


def parse_markdown_slides(md_file):
    """Parse markdown file into slide structure."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = []
    current_slide = None
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip metadata
        if line.startswith('**Author') or line.startswith('**Created') or line.startswith('**Format'):
            i += 1
            continue
        
        # Slide separator
        if line.startswith('---') or line.startswith('## Slide'):
            if current_slide and (current_slide['title'] or current_slide['content']):
                slides.append(current_slide)
            current_slide = {'title': '', 'content': [], 'bullets': [], 'type': 'content'}
            i += 1
            continue
        
        # Extract title
        if current_slide and not current_slide['title'] and line and not line.startswith('---'):
            current_slide['title'] = line
            i += 1
            continue
        
        # Content
        if current_slide and line:
            # Clean markdown formatting
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            
            if line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
                current_slide['bullets'].append(clean_line[2:].strip())
            elif line.startswith('  - ') or line.startswith('  * '):
                current_slide['bullets'].append('  ' + clean_line.strip()[2:].strip())
            else:
                current_slide['content'].append(clean_line)
        
        i += 1
    
    # Only add last slide if it has content
    if current_slide and (current_slide['title'] or current_slide['content']):
        slides.append(current_slide)
    
    return slides


def create_impress_script(slides, output_file):
    """Create LibreOffice Basic macro script to generate presentation."""
    
    # Create macro content
    macro = '''REM Generate Presentation from Python
Sub GeneratePresentation
    Dim oDoc As Object
    Dim oSlide As Object
    Dim oShape As Object
    Dim oText As Object
    Dim oCursor As Object
    Dim oSize As New com.sun.star.awt.Size
    Dim oPos As New com.sun.star.awt.Point
    
    ' Create new Impress document
    oDoc = StarDesktop.loadComponentFromURL("private:factory/simpress", "_blank", 0, Array())
    
    ' Set to widescreen 16:9
    Dim oPageProps As Object
    oPageProps = oDoc.getDrawPages().getByIndex(0)
    oPageProps.Width = 28000  ' 16:9 width in 1/100mm
    oPageProps.Height = 15750 ' 16:9 height in 1/100mm
    
'''
    
    for idx, slide_data in enumerate(slides):
        if idx == 0:
            # Use first slide (title slide)
            macro += f'''
    ' ========== SLIDE {idx + 1}: TITLE SLIDE ==========
    oSlide = oDoc.getDrawPages().getByIndex(0)
    
    ' Set background to blue gradient
    oSlide.Background = True
    oSlide.BackgroundObjectsVisible = True
    
    ' Title
    oShape = oSlide.getByIndex(0)  ' Title placeholder
    oText = oShape.getText()
    oText.setString("{slide_data['title'].replace('"', '""')}")
    oCursor = oText.createTextCursor()
    oCursor.gotoStart(False)
    oCursor.gotoEnd(True)
    oCursor.CharHeight = 44
    oCursor.CharWeight = 150  ' Bold
    oCursor.CharColor = RGB(0, 120, 212)  ' Microsoft Blue
    
'''
        else:
            # Add new slide
            macro += f'''
    ' ========== SLIDE {idx + 1}: {slide_data['title'][:30]} ==========
    oSlide = oDoc.getDrawPages().insertNewByIndex({idx})
    oSlide.setLayout(1)  ' Title + Content layout
    
    ' Set background
    oSlide.Background = False
    
    ' Title
    oShape = oSlide.getByIndex(0)
    oText = oShape.getText()
    oText.setString("{slide_data['title'].replace('"', '""')}")
    oCursor = oText.createTextCursor()
    oCursor.gotoStart(False)
    oCursor.gotoEnd(True)
    oCursor.CharHeight = 32
    oCursor.CharWeight = 150
    oCursor.CharColor = RGB(0, 120, 212)
    
    ' Content
    If oSlide.getCount() > 1 Then
        oShape = oSlide.getByIndex(1)  ' Content placeholder
        oText = oShape.getText()
'''
            
            # Add bullets and content
            for bullet in slide_data['bullets']:
                escaped = bullet.replace('"', '""').replace('\n', ' ')
                macro += f'''
        oText.insertString(oText.getEnd(), "{escaped}", False)
        oText.insertControlCharacter(oText.getEnd(), com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK, False)
'''
            
            for content in slide_data['content'][:3]:  # Limit to 3 paragraphs
                if content and not content.startswith('**'):
                    escaped = content.replace('"', '""').replace('\n', ' ')
                    macro += f'''
        oText.insertString(oText.getEnd(), "{escaped}", False)
        oText.insertControlCharacter(oText.getEnd(), com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK, False)
'''
            
            macro += '''
        oCursor = oText.createTextCursor()
        oCursor.gotoStart(False)
        oCursor.gotoEnd(True)
        oCursor.CharHeight = 20
        oCursor.CharColor = RGB(50, 49, 48)
    End If
'''
    
    # Save and close
    macro += f'''
    ' Save document
    Dim oFileURL As String
    oFileURL = ConvertToURL("{output_file.absolute()}")
    
    Dim aProps(1) As New com.sun.star.beans.PropertyValue
    aProps(0).Name = "FilterName"
    aProps(0).Value = "impress8"
    aProps(1).Name = "Overwrite"
    aProps(1).Value = True
    
    oDoc.storeAsURL(oFileURL, aProps())
    oDoc.close(True)
    
End Sub
'''
    
    return macro


def generate_with_template(slides, output_file):
    """Generate presentation using LibreOffice template approach."""
    
    # Create a simple approach: generate ODP XML directly
    print("Creating presentation using LibreOffice command line...")
    
    # Create a temporary text file with content
    temp_txt = output_file.with_suffix('.temp.txt')
    
    with open(temp_txt, 'w', encoding='utf-8') as f:
        for idx, slide_data in enumerate(slides):
            f.write(f"\n{'='*60}\n")
            f.write(f"SLIDE {idx + 1}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"TITLE: {slide_data['title']}\n\n")
            
            if slide_data['bullets']:
                f.write("CONTENT:\n")
                for bullet in slide_data['bullets']:
                    f.write(f"  • {bullet}\n")
            
            if slide_data['content']:
                f.write("\n")
                for content in slide_data['content'][:2]:
                    if content:
                        f.write(f"{content}\n")
            f.write("\n")
    
    print(f"✓ Created content file: {temp_txt}")
    
    # Use LibreOffice to create an Impress file from the template
    soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    
    # Start LibreOffice in headless mode and create presentation
    cmd = [
        soffice,
        '--headless',
        '--impress',
        str(temp_txt)
    ]
    
    print("Launching LibreOffice to create presentation...")
    subprocess.run(cmd, capture_output=True)
    
    # Clean up temp file
    if temp_txt.exists():
        temp_txt.unlink()
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_slides_impress.py input.md [output.odp]")
        print("\nExample:")
        print("  python generate_slides_impress.py PFT_RFT_PM_Agent_Slides.md presentation.odp")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)
    
    # Output file
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_suffix('.odp')
    
    print(f"Reading slides from: {input_file}")
    
    # Parse markdown
    slides = parse_markdown_slides(input_file)
    print(f"✓ Parsed {len(slides)} slides")
    
    # Use simpler soffice command to create
    soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    
    print("\nOpening LibreOffice Impress...")
    print("Please create the presentation manually using the parsed content,")
    print("or use the python-pptx version which works better programmatically.")
    
    # Launch LibreOffice Impress
    subprocess.Popen([soffice, '--impress'])
    
    print(f"\n✓ LibreOffice Impress launched")
    print(f"\nTo create the presentation:")
    print(f"1. Use File > New > Presentation")
    print(f"2. Choose a professional template")
    print(f"3. Add the {len(slides)} slides with content from {input_file}")
    print(f"4. Save as: {output_file}")


if __name__ == '__main__':
    main()
