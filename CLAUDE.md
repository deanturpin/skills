# Skills Timeline Project - Claude Code Session

## Project Overview
A skills timeline visualisation tool that generates professional timeline charts from CSV data for CV integration.

## 2025 Modernisation Session

### What We Did
- **Migrated from R to Python/Plotly** - Modern tech stack with better tooling
- **Added logarithmic time scaling** - Recent years get more visual emphasis
- **Implemented skill categorisation** - Colour-coded by type (programming, tools, platforms)
- **Enhanced visual design** - Professional styling with smart line thickness
- **Updated build pipeline** - Python-based CI/CD with backup R version
- **High-DPI output** - 300 DPI PNG for crisp CV integration

### Technical Improvements
- **Data handling**: pandas for CSV processing vs R's data.frame
- **Visualisation**: Plotly for modern charts vs ggplot2
- **Time scaling**: Logarithmic transformation emphasises recent skills
- **Categorisation**: Automatic skill grouping with colour coding
- **Line weights**: Recent skills appear bolder/thicker
- **Build system**: `make install && make all` workflow

### Files Modified
- `timeline.py` - New Python implementation with log scaling
- `requirements.txt` - Python dependencies
- `makefile` - Updated for Python workflow (with R backup)
- `.gitlab-ci.yml` - Python CI/CD pipeline
- `skills.csv` - Updated end dates to 2025-12-31

### Key Features
- **Logarithmic time axis** - More space for recent years, compressed historical view
- **Smart visual weighting** - Recent skills more prominent
- **Professional colour palette** - Modern, CV-ready styling
- **High-quality output** - 1200x800px at 300 DPI
- **Skill categorisation** - Grouped by programming, tools, platforms, etc.

### Usage
```bash
make install    # Install Python dependencies
make all       # Generate timeline and view
make r-version # Use legacy R version
make deploy    # Auto-commit and push
```

---
*Generated during Claude Code session - September 2025*