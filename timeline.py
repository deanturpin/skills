#!/usr/bin/env python3
"""
Modern skills timeline generator using Python and Plotly.
Generates a professional timeline chart from CSV data with logarithmic time scaling.
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


def load_skills_data(csv_file="skills.csv"):
    """Load and prepare skills data from CSV."""
    df = pd.read_csv(csv_file)
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    return df


def log_transform_date(dt, reference_date=None):
    """Transform date to logarithmic scale, emphasising recent years."""
    if reference_date is None:
        reference_date = datetime.now()
    years_ago = (reference_date - dt).days / 365.25
    # Logarithmic scaling: recent years get more space
    # Add 1 to avoid log(0), scale to make recent years prominent
    return -np.log(years_ago + 1)


def create_log_scale_timeline(df):
    """Create a timeline with logarithmic scaling to emphasise recent years."""

    # Reference date for logarithmic scaling (today)
    today = datetime.now()

    # Apply log transformation to dates
    df['start_log'] = df['start'].apply(lambda x: log_transform_date(x, today))
    df['end_log'] = df['end'].apply(lambda x: log_transform_date(x, today))

    # Create figure
    fig = go.Figure()

    # Color palette - modern, professional
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83', '#048A81']

    # Group skills by category (rough categorisation based on naming)
    categories = {
        'Programming': ['C++', 'STL', 'Python', 'JavaScript', 'Haskell', 'Go', 'R', 'Bash'],
        'Tools & Systems': ['Vi', 'Git', 'Linux', 'Unix', 'Make', 'CMake', 'Docker', 'Jenkins'],
        'Protocols & Standards': ['TCP', 'XMPP', 'SIP', 'FIX', 'ONVIF'],
        'Platforms & Cloud': ['Google Cloud', 'AWS', 'Cloudflare', 'Raspberry Pi'],
        'Frameworks & Libraries': ['Qt', 'JUCE', 'ZeroMQ', 'Hugo', 'Jekyll'],
        'Other': []
    }

    # Assign categories
    def categorise_skill(skill_name):
        for category, keywords in categories.items():
            if any(keyword.lower() in skill_name.lower() for keyword in keywords):
                return category
        return 'Other'

    df['category'] = df['name'].apply(categorise_skill)

    # Remove number prefixes from skill names
    df['clean_name'] = df['name'].apply(lambda x: x.split(' ', 1)[-1] if ' ' in x else x)

    # Sort by category and start date for better visual grouping
    df['category_order'] = df['category'].map({
        'Programming': 0,
        'Tools & Systems': 1,
        'Platforms & Cloud': 2,
        'Protocols & Standards': 3,
        'Frameworks & Libraries': 4,
        'Other': 5
    })
    df = df.sort_values(['category_order', 'start'])
    df = df.reset_index(drop=True)

    # Add timeline traces
    for i, (_, row) in enumerate(df.iterrows()):
        category = row['category']
        color_idx = list(categories.keys()).index(category) if category in categories else 0
        color = colors[color_idx % len(colors)]

        # Calculate line thickness based on recency (more recent = thicker)
        years_since_start = (today - row['start']).days / 365.25
        line_width = max(2, 8 - (years_since_start / 5))  # Thicker for more recent

        # Calculate middle point for text placement
        mid_point_log = (row['start_log'] + row['end_log']) / 2

        # Add the timeline segment (using log-transformed dates)
        fig.add_trace(go.Scatter(
            x=[row['start_log'], row['end_log']],
            y=[i, i],  # Use index for y-position
            mode='lines',
            line=dict(
                color=color,
                width=line_width
            ),
            name=category,
            showlegend=False,  # Hide legend
            hovertemplate=f"<b>{row['clean_name']}</b><br>" +
                         f"Start: {row['start'].strftime('%b %Y')}<br>" +
                         f"End: {row['end'].strftime('%b %Y')}<br>" +
                         f"Duration: {((row['end'] - row['start']).days / 365.25):.1f} years<br>" +
                         "<extra></extra>"
        ))

        # Add text label in the middle of the bar
        fig.add_trace(go.Scatter(
            x=[mid_point_log],
            y=[i],  # Use index for y-position
            mode='text',
            text=[row['clean_name']],
            textfont=dict(
                size=7,
                color='white',
                weight='bold'
            ),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Update layout with modern styling
    fig.update_layout(
        title=dict(
            text=f"Skills Timeline • Updated {datetime.now().strftime('%B %Y')}",
            x=0.5,
            font=dict(size=16, color='#2C3E50'),
            pad=dict(b=20)
        ),
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor='#ECF0F1',
            gridwidth=1,
            tickangle=45,
            tickfont=dict(size=10, color='#34495E'),
            range=[df['start_log'].min(), df['end_log'].max()],
            # Custom tick labels to show actual years despite log scale
            tickmode='array',
            tickvals=[log_transform_date(pd.to_datetime(f'{year}-01-01'), today) for year in range(1998, 2026, 3)],
            ticktext=[str(year) for year in range(1998, 2026, 3)]
        ),
        yaxis=dict(
            title="",
            showgrid=False,
            showticklabels=False,  # Hide y-axis labels
            autorange='reversed'  # Most recent skills at top
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=50, r=50, t=80, b=80),
        height=800,
        width=1200,
        showlegend=False
    )

    return fig


def save_timeline(fig, png_path="public/skills.png", html_path="public/timeline.html"):
    """Save the timeline as both PNG and interactive HTML."""
    # High-quality PNG for CV integration
    fig.write_image(
        png_path,
        width=1200,
        height=800,
        scale=3,  # High DPI for crisp CV integration
        format="png"
    )

    # Interactive HTML for GitLab Pages
    fig.write_html(
        html_path,
        config={
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
            'responsive': True
        },
        include_plotlyjs='cdn'
    )


def main():
    """Generate the skills timeline."""
    print("Loading skills data...")
    df = load_skills_data()

    print(f"Found {len(df)} skills spanning {df['start'].min().year} to {df['end'].max().year}")

    print("Creating timeline visualization...")
    fig = create_log_scale_timeline(df)

    print("Saving timeline as PNG and HTML...")
    save_timeline(fig)

    print("✅ Skills timeline generated successfully!")
    print("📁 PNG: public/skills.png")
    print("🌐 Interactive: public/timeline.html")


if __name__ == "__main__":
    main()