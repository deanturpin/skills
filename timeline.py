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

    # Sort by start date for better visual layering
    df = df.sort_values('start')

    # Add timeline traces
    for i, (_, row) in enumerate(df.iterrows()):
        category = row['category']
        color_idx = list(categories.keys()).index(category) if category in categories else 0
        color = colors[color_idx % len(colors)]

        # Calculate line thickness based on recency (more recent = thicker)
        years_since_start = (today - row['start']).days / 365.25
        line_width = max(2, 8 - (years_since_start / 5))  # Thicker for more recent

        # Add the timeline segment (using log-transformed dates)
        fig.add_trace(go.Scatter(
            x=[row['start_log'], row['end_log']],
            y=[row['name'], row['name']],
            mode='lines',
            line=dict(
                color=color,
                width=line_width
            ),
            name=category,
            showlegend=i == 0 or category != df.iloc[i-1]['category'],  # Show legend once per category
            hovertemplate=f"<b>{row['name']}</b><br>" +
                         f"Start: {row['start'].strftime('%b %Y')}<br>" +
                         f"End: {row['end'].strftime('%b %Y')}<br>" +
                         f"Duration: {((row['end'] - row['start']).days / 365.25):.1f} years<br>" +
                         "<extra></extra>"
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
            showgrid=True,
            gridcolor='#F8F9FA',
            gridwidth=1,
            tickfont=dict(size=8, color='#34495E'),
            autorange='reversed'  # Most recent skills at top
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=200, r=50, t=80, b=80),
        height=800,
        width=1200,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )

    return fig


def save_timeline(fig, output_path="public/skills.png"):
    """Save the timeline as a high-quality PNG."""
    fig.write_image(
        output_path,
        width=1200,
        height=800,
        scale=3,  # High DPI for crisp CV integration
        format="png"
    )


def main():
    """Generate the skills timeline."""
    print("Loading skills data...")
    df = load_skills_data()

    print(f"Found {len(df)} skills spanning {df['start'].min().year} to {df['end'].max().year}")

    print("Creating timeline visualization...")
    fig = create_log_scale_timeline(df)

    print("Saving timeline as PNG...")
    save_timeline(fig)

    print("✅ Skills timeline generated successfully!")
    print("📁 Output: public/skills.png")


if __name__ == "__main__":
    main()