# Enterprise Presentation Generator

**Created**: November 17, 2025  
**Author**: Chin-Yew Lin

## Overview

Automated tool to generate enterprise-grade presentations from markdown slide outlines using LibreOffice.

## Files Generated

### Source Document
- `PFT_RFT_PM_Agent_Slides.md` - Markdown slide outline (13 slides)

### Presentations
- **`PFT_RFT_PM_Agent_Enterprise.pptx`** - Enterprise PowerPoint (recommended)
- **`PFT_RFT_PM_Agent_Enterprise.odp`** - Enterprise LibreOffice Impress

## Enterprise Design Features

### Visual Design
- **Microsoft Blue color scheme** (#0078D4 primary, #00BCF2 accent)
- **Professional gradient** backgrounds for title slides
- **Clean white backgrounds** for content slides
- **Top accent bar** on all content slides (8px gradient)
- **Calibri font family** (Microsoft standard)

### Typography
- **Title slide**: 56px heading, 28px subtitle
- **Content slides**: 40px headings, 20px body text
- **Hierarchical bullets**: Custom styled with blue arrows (▸)
- **Proper line spacing**: 1.7 for readability

### Layout & Structure
- **Consistent margins**: 50-80px padding
- **Slide numbers**: Bottom right footer
- **Visual indicators**: Color-coded boxes for outcomes/opportunities
- **Section headers**: Uppercase, blue, 22px

### Content Formatting
- **Special boxes**:
  - 🟢 Green box for outcomes (#E6F7E6)
  - 🟡 Yellow box for opportunities (#FFF4CE)
  - 🔵 Blue box for emphasis (#F3F2F1)
- **Code blocks**: Gray background with monospace font
- **Strong text**: Blue color (#0078D4) for emphasis
- **Nested lists**: Proper indentation and styling

## Usage

### Generate Presentation
```bash
# PowerPoint format (recommended)
python generate_slides.py PFT_RFT_PM_Agent_Slides.md PFT_RFT_PM_Agent_Enterprise.pptx

# LibreOffice format
python generate_slides.py PFT_RFT_PM_Agent_Slides.md PFT_RFT_PM_Agent_Enterprise.odp
```

### Open Presentation
```bash
# macOS
open PFT_RFT_PM_Agent_Enterprise.pptx

# Or with LibreOffice
/Applications/LibreOffice.app/Contents/MacOS/soffice PFT_RFT_PM_Agent_Enterprise.pptx
```

## Technical Details

### Requirements
- LibreOffice 25.8+ installed at `/Applications/LibreOffice.app`
- Python 3.8+
- macOS (or adjust paths for Linux/Windows)

### Process Flow
1. **Parse markdown** → Extract slide titles and content
2. **Generate HTML** → Create styled HTML with CSS
3. **Convert to presentation** → LibreOffice headless mode
4. **Output format** → PPTX or ODP

### HTML Intermediate
The script creates a temporary HTML file with:
- Page-break CSS for slide separation
- Print-optimized styles (10in × 7.5in)
- Professional color palette
- Responsive typography

### LibreOffice Conversion
Uses LibreOffice CLI in headless mode:
```bash
soffice --headless --convert-to pptx:Impress\ MS\ PowerPoint\ 2007\ XML input.html
```

## Slide Content

### 13 Core Slides
1. **Title & Vision** - Project overview
2. **Problem & Opportunity** - Business case
3. **Design Goals** - Requirements
4. **High-Level Architecture** - 4-layer system
5. **Foundation & Alignment (PFT)** - Training approach
6. **Reinforcement Fine-Tuning (RFT)** - Tool workflows
7. **Core Components** - Technical modules
8. **Data & Knowledge Flow** - Information pipeline
9. **Example Use Case: Sprint Planning** - Practical demo
10. **Example Use Case: Risk Review** - Risk management
11. **Evaluation & Metrics** - Quality measures
12. **Security, Governance, & Audit** - Enterprise controls
13. **Roadmap** - Phased deployment plan

## Customization

### Change Colors
Edit `generate_slides.py`, line ~50:
```python
background: linear-gradient(135deg, #0078D4 0%, #005A9E 100%);  # Title slide
color: #0078D4;  # Primary blue
```

### Adjust Typography
Edit font sizes in CSS (lines 60-120):
```css
h1 { font-size: 56px; }  /* Title */
h2 { font-size: 40px; }  /* Slide heading */
.content { font-size: 20px; }  /* Body text */
```

### Add Branding
Insert logo or footer text:
```python
html += '<div class="slide-footer">Company Name | {slide_num}</div>\n'
```

## Quality Standards

### Enterprise Readiness
- ✅ Professional color palette (Microsoft standard)
- ✅ Consistent typography and spacing
- ✅ Clear visual hierarchy
- ✅ Accessible contrast ratios (WCAG AA)
- ✅ Print-optimized layout
- ✅ Numbered slides for reference

### Best Practices
- **One idea per slide** - Avoid clutter
- **6×6 rule** - Max 6 bullets, 6 words per bullet (where possible)
- **Visual balance** - White space for readability
- **Action-oriented** - Clear takeaways highlighted

## Troubleshooting

### LibreOffice Not Found
```bash
# Check installation
ls /Applications/LibreOffice.app

# If not found, install from:
# https://www.libreoffice.org/download/download/
```

### Conversion Fails
```bash
# Test LibreOffice CLI manually
/Applications/LibreOffice.app/Contents/MacOS/soffice --version

# Check temp HTML file
cat PFT_RFT_PM_Agent_Slides.tmp.html
```

### Styling Issues
- Edit CSS in `generate_slides.py`
- Test with: `open PFT_RFT_PM_Agent_Slides.tmp.html`
- Adjust colors, fonts, spacing as needed

## Future Enhancements

### Potential Additions
- [ ] Chart/diagram generation from data
- [ ] Image/icon insertion from library
- [ ] Template selection (themes)
- [ ] Speaker notes generation
- [ ] Table formatting support
- [ ] Animation/transition markers
- [ ] Multi-column layouts
- [ ] Master slide customization

### Advanced Features
- [ ] Python-UNO direct API integration (no HTML intermediate)
- [ ] PDF export with speaker notes
- [ ] Batch conversion for multiple decks
- [ ] Version control integration (diff slides)
- [ ] Auto-generation from Jira/Notion/Confluence

## License

Internal Microsoft tool for Scenara project.

---

**Questions?** Contact: Chin-Yew Lin
