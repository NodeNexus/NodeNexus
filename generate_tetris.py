#!/usr/bin/env python3
"""
GitHub Tetris Contribution Graph Generator
Generates an animated SVG that looks like Tetris blocks falling into a GitHub contribution graph
"""

import random
import datetime

def generate_tetris_contribution_graph():
    """Generate an animated Tetris-style GitHub contribution graph"""
    
    # Configuration
    width = 940
    height = 160
    cell_size = 10
    cell_gap = 2
    weeks = 53
    days = 7
    
    # GitHub contribution colors
    colors = {
        0: '#161b22',  # Empty
        1: '#0e4429',  # Low
        2: '#006d32',  # Medium-low
        3: '#26a641',  # Medium-high
        4: '#39d353'   # High
    }
    
    # Tetris piece shapes (represented as list of (x, y) offsets)
    tetris_shapes = {
        'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
        'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
        'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
        'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
        'J': [(1, 0), (1, 1), (1, 2), (0, 2)],
        'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
        'Z': [(0, 0), (1, 0), (1, 1), (2, 1)]
    }
    
    # Initialize grid
    grid = [[0 for _ in range(weeks)] for _ in range(days)]
    
    # Place Tetris pieces randomly on the grid
    num_pieces = random.randint(12, 20)
    for _ in range(num_pieces):
        shape = random.choice(list(tetris_shapes.values()))
        start_week = random.randint(0, weeks - 5)
        start_day = random.randint(0, days - 4)
        intensity = random.randint(2, 4)
        
        for dx, dy in shape:
            week = start_week + dx
            day = start_day + dy
            if 0 <= week < weeks and 0 <= day < days:
                grid[day][week] = intensity
    
    # Add random scattered contributions
    for week in range(weeks):
        for day in range(days):
            if grid[day][week] == 0 and random.random() > 0.65:
                grid[day][week] = random.randint(1, 4)
    
    # Create falling animation for recent weeks
    recent_weeks_start = weeks - 10
    
    # Start SVG
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .cell {{ 
            rx: 2; 
            transition: all 0.3s ease;
        }}
        
        @keyframes fall {{
            from {{ 
                transform: translateY(-120px);
                opacity: 0;
            }}
            to {{ 
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        @keyframes slideIn {{
            from {{ 
                transform: translateX(-50px);
                opacity: 0;
            }}
            to {{ 
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        
        .falling {{ 
            animation: fall 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }}
        
        .active {{
            animation: pulse 2s ease-in-out infinite;
        }}
        
        .cell:hover {{
            transform: scale(1.2);
            filter: brightness(1.3);
        }}
        
        .title {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            font-weight: 600;
            animation: slideIn 1s ease-out;
        }}
        
        .subtitle {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            font-size: 11px;
            animation: slideIn 1.2s ease-out;
        }}
    </style>
    
    <defs>
        <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#39d353;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#26a641;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#006d32;stop-opacity:1" />
        </linearGradient>
        
        <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="{width}" height="{height}" fill="#0d1117" rx="6"/>
    
    <!-- Title -->
    <text x="20" y="28" fill="url(#titleGradient)" font-size="18" class="title" filter="url(#glow)">
        🎮 GitHub Contributions Tetris
    </text>
    
    <!-- Subtitle with date -->
    <text x="20" y="44" fill="#8b949e" class="subtitle">
        Auto-generated pattern • Last updated: {datetime.datetime.now().strftime('%B %d, %Y')}
    </text>
    
'''
    
    # Calculate offsets for centering
    x_offset = 20
    y_offset = 60
    
    # Day labels
    day_labels = ['Mon', 'Wed', 'Fri']
    day_indices = [0, 2, 4]
    
    for label, idx in zip(day_labels, day_indices):
        y = y_offset + (idx * (cell_size + cell_gap)) + 8
        svg += f'    <text x="5" y="{y}" fill="#8b949e" font-size="9" font-family="sans-serif">{label}</text>\n'
    
    # Month labels (simplified)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = datetime.datetime.now().month
    
    for i in range(0, 12):
        month_x = x_offset + (i * 4.3 * (cell_size + cell_gap))
        if month_x < width - 50:
            month_idx = (current_month - 12 + i) % 12
            svg += f'    <text x="{month_x}" y="{y_offset - 5}" fill="#8b949e" font-size="9" font-family="sans-serif">{months[month_idx]}</text>\n'
    
    # Generate cells
    for week in range(weeks):
        for day in range(days):
            x = x_offset + (week * (cell_size + cell_gap))
            y = y_offset + (day * (cell_size + cell_gap))
            
            intensity = grid[day][week]
            color = colors[intensity]
            
            # Calculate animation delay for falling effect
            delay = (week * 0.015) + (day * 0.02)
            
            # Determine if cell should have animation
            if intensity > 0:
                # Recent weeks get falling animation
                if week >= recent_weeks_start:
                    class_name = 'cell falling active'
                else:
                    class_name = 'cell'
                    
                svg += f'    <rect class="{class_name}" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" style="animation-delay: {delay}s"/>\n'
            else:
                # Empty cells
                svg += f'    <rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" stroke="#1b1f23" stroke-width="0.5"/>\n'
    
    # Legend
    legend_y = height - 18
    legend_x = width - 280
    
    svg += f'''    
    <!-- Legend -->
    <g id="legend">
        <text x="{legend_x}" y="{legend_y + 8}" fill="#8b949e" font-size="11" font-family="sans-serif">Less</text>
        <rect x="{legend_x + 35}" y="{legend_y}" width="11" height="11" fill="{colors[0]}" stroke="#1b1f23" stroke-width="1" rx="2"/>
        <rect x="{legend_x + 50}" y="{legend_y}" width="11" height="11" fill="{colors[1]}" rx="2"/>
        <rect x="{legend_x + 65}" y="{legend_y}" width="11" height="11" fill="{colors[2]}" rx="2"/>
        <rect x="{legend_x + 80}" y="{legend_y}" width="11" height="11" fill="{colors[3]}" rx="2"/>
        <rect x="{legend_x + 95}" y="{legend_y}" width="11" height="11" fill="{colors[4]}" rx="2"/>
        <text x="{legend_x + 110}" y="{legend_y + 8}" fill="#8b949e" font-size="11" font-family="sans-serif">More</text>
    </g>
    
    <!-- Stats -->
    <text x="20" y="{height - 8}" fill="#8b949e" font-size="9" font-family="sans-serif">
        💚 {sum(sum(1 for cell in row if cell > 0) for row in grid)} contributions in the last year
    </text>
'''
    
    # Close SVG
    svg += '</svg>'
    
    return svg


if __name__ == '__main__':
    # Generate and save the SVG
    svg_content = generate_tetris_contribution_graph()
    
    with open('tetris.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print('✅ Tetris contribution graph generated successfully!')
    print('📁 Saved to: tetris.svg')
