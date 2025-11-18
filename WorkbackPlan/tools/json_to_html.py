#!/usr/bin/env python3
"""
Convert JSON prompts to HTML DevUI test package
Generates HTML file from AI-classified meeting prompts
"""

import json
import sys
from pathlib import Path
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizChat DevUI Test Prompts - {user_name}</title>
    <style>
        :root {{
            --primary-color: #0078d4;
            --secondary-color: #106ebe;
            --success-color: #107c10;
            --warning-color: #ffb900;
            --danger-color: #d13438;
            --bg-color: #f3f2f1;
            --card-bg: #ffffff;
            --text-primary: #323130;
            --text-secondary: #605e5c;
            --border-color: #e1dfdd;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .selection-controls {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border-color);
        }}

        .selection-controls h2 {{
            color: var(--primary-color);
            font-size: 1.3em;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .selection-status {{
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px;
            background: var(--bg-color);
            border-radius: 6px;
        }}

        .selection-counter {{
            font-size: 2em;
            font-weight: 700;
            color: var(--primary-color);
        }}

        .selection-counter.goal-met {{
            color: var(--success-color);
        }}

        .selection-label {{
            font-size: 0.9em;
            color: var(--text-secondary);
        }}

        .selection-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 1em;
        }}

        .btn-primary {{
            background: var(--primary-color);
            color: white;
        }}

        .btn-primary:hover {{
            background: var(--secondary-color);
        }}

        .btn-success {{
            background: var(--success-color);
            color: white;
        }}

        .btn-success:hover {{
            background: #0e6b0e;
        }}

        .btn-secondary {{
            background: var(--text-secondary);
            color: white;
        }}

        .btn-secondary:hover {{
            background: #484644;
        }}

        .filter-toggle {{
            display: flex;
            gap: 10px;
            align-items: center;
            margin-top: 15px;
        }}

        .filter-toggle label {{
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            padding: 8px 12px;
            background: var(--bg-color);
            border-radius: 6px;
            transition: background 0.2s;
        }}

        .filter-toggle label:hover {{
            background: #e8e7e5;
        }}

        .filter-toggle input[type=\"checkbox\"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}

        .auto-save-indicator {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(16, 124, 16, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}

        .auto-save-indicator.show {{
            opacity: 1;
        }}

        .prompt-card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 0;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s, opacity 0.3s;
            overflow: hidden;
        }}

        .prompt-card.hidden {{
            display: none;
        }}

        .prompt-card.selected {{
            border-left: 5px solid var(--success-color);
            box-shadow: 0 2px 12px rgba(16, 124, 16, 0.15);
        }}

        .prompt-card.unselected {{
            opacity: 0.6;
        }}

        .prompt-card.synthetic {{
            border: 2px dashed var(--warning-color);
            background: linear-gradient(135deg, #fffbf0 0%, var(--card-bg) 100%);
        }}

        .prompt-card.completed {{
            border: 2px solid var(--success-color);
            background: linear-gradient(135deg, #f0fff0 0%, var(--card-bg) 100%);
        }}

        .completed-badge {{
            display: inline-block;
            background: var(--success-color);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}

        .synthetic-badge {{
            display: inline-block;
            background: var(--warning-color);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}

        .prompt-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }}

        .prompt-card-header {{
            padding: 20px 25px;
            cursor: pointer;
            user-select: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-color);
            transition: background 0.2s;
        }}

        .prompt-card-header-left {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex: 1;
        }}

        .selection-checkbox {{
            width: 24px;
            height: 24px;
            cursor: pointer;
            flex-shrink: 0;
        }}

        .prompt-card-header:hover {{
            background: #e8e7e5;
        }}

        .prompt-card-title {{
            flex: 1;
        }}

        .prompt-card-title h2 {{
            color: var(--primary-color);
            font-size: 1.6em;
            margin-bottom: 5px;
            font-weight: 700;
        }}

        .prompt-card-title .meeting-info {{
            color: var(--text-secondary);
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .collapse-icon {{
            font-size: 1.5em;
            color: var(--primary-color);
            transition: transform 0.3s;
            margin-left: 15px;
        }}

        .collapse-icon.collapsed {{
            transform: rotate(-90deg);
        }}

        .prompt-content {{
            padding: 0 25px 25px 25px;
            display: none;
        }}

        .prompt-content.expanded {{
            display: block;
        }}

        .prompt-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border-color);
        }}

        .prompt-title {{
            flex: 1;
        }}

        .prompt-title h2 {{
            color: var(--primary-color);
            font-size: 1.5em;
            margin-bottom: 8px;
            font-weight: 600;
        }}

        .prompt-id {{
            background: var(--primary-color);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }}

        .prompt-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .meta-item {{
            background: var(--bg-color);
            padding: 12px 16px;
            border-radius: 6px;
            border-left: 3px solid var(--primary-color);
        }}

        .meta-label {{
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}

        .meta-value {{
            color: var(--text-primary);
            font-size: 1em;
        }}

        .prompt-text {{
            background: #fafafa;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.95em;
            line-height: 1.8;
            white-space: pre-wrap;
            color: var(--text-primary);
        }}

        .input-section {{
            margin-top: 25px;
            padding-top: 20px;
            border-top: 2px solid var(--border-color);
        }}

        .input-group {{
            margin-bottom: 20px;
        }}

        .input-group label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-primary);
            font-size: 0.95em;
        }}

        .input-group input,
        .input-group textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-family: inherit;
            font-size: 0.95em;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .input-group input:focus,
        .input-group textarea:focus {{
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.1);
        }}

        .input-group textarea {{
            min-height: 120px;
            resize: vertical;
            font-family: 'Segoe UI', sans-serif;
        }}

        .tools-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }}

        .tool-tag {{
            background: var(--primary-color);
            color: white;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.85em;
            font-weight: 500;
        }}

        .complexity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .complexity-high {{
            background: var(--danger-color);
            color: white;
        }}

        .complexity-medium {{
            background: var(--warning-color);
            color: white;
        }}

        .complexity-low {{
            background: var(--success-color);
            color: white;
        }}

        .save-button {{
            background: var(--success-color);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            margin-top: 10px;
        }}

        .save-button:hover {{
            background: #0e6b0e;
            transform: translateY(-1px);
        }}

        .save-button:active {{
            transform: translateY(0);
        }}

        .copy-prompt-button {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 0.95em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 15px 0;
        }}

        .copy-prompt-button:hover {{
            background: var(--secondary-color);
            transform: translateY(-1px);
        }}

        .copy-prompt-button:active {{
            transform: translateY(0);
        }}

        .copy-prompt-button.copied {{
            background: var(--success-color);
        }}

        .statistics-section {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border-color);
        }}

        .statistics-section h2 {{
            color: var(--primary-color);
            font-size: 1.5em;
            margin-bottom: 20px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .stat-card {{
            background: var(--bg-color);
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid var(--primary-color);
        }}

        .stat-label {{
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .stat-value {{
            color: var(--text-primary);
            font-size: 1.4em;
            font-weight: 700;
        }}

        .filter-info {{
            background: #f0f9ff;
            border-left: 4px solid var(--primary-color);
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}

        .filter-info h3 {{
            color: var(--primary-color);
            font-size: 1.1em;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .filter-info ul {{
            margin: 0;
            padding-left: 20px;
            line-height: 1.8;
        }}

        .filter-info li {{
            color: var(--text-primary);
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-secondary);
            margin-top: 40px;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.5em;
            }}

            .prompt-meta {{
                grid-template-columns: 1fr;
            }}

            .prompt-header {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 BizChat Workback Planning DevUI Test Prompts</h1>
            <p><strong>User:</strong> {user_name} | <strong>Generated:</strong> {timestamp} | <strong>AI-Classified with Qwen3-Embedding-0.6B</strong></p>
            <p><strong>Author:</strong> TimeBerry T+P</p>
            <div style="margin-top: 15px;">
                <button onclick="expandAll()" style="background: var(--success-color); color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; margin-right: 10px;">📂 Expand All</button>
                <button onclick="collapseAll()" style="background: var(--text-secondary); color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer;">📁 Collapse All</button>
            </div>
        </div>

        <div class="selection-controls">
            <h2>📝 Meeting Selection for Testing</h2>
            <div class="selection-status">
                <div>
                    <div class="selection-counter" id="selection-counter">0</div>
                    <div class="selection-label">Your Meetings Selected / 5 Recommended</div>
                </div>
                <div style="flex: 1; padding-left: 20px;">
                    <p style="margin: 0; color: var(--text-secondary);">🎭 <strong>5 exploration scenarios are pre-selected.</strong> Please select <strong>at least 5 more meetings from your calendar</strong> for testing (you can select more).</p>
                </div>
            </div>
            <div class="selection-buttons">
                <button class="btn btn-primary" onclick="selectAll()">✅ Select All</button>
                <button class="btn btn-secondary" onclick="deselectAll()">❌ Deselect All</button>
                <button class="btn btn-success" onclick="saveAllData()">💾 Save Progress</button>
                <button class="btn btn-success" onclick="exportAnnotations()">📥 Export Annotations</button>
                <button class="btn btn-primary" onclick="exportLocalStorage()">💾 Export localStorage (for regeneration)</button>
            </div>
            <div class="filter-toggle">
                <label>
                    <input type="checkbox" id="filter-unselected" onchange="toggleFilterUnselected()">
                    <span>Hide Unselected Meetings</span>
                </label>
                <label>
                    <input type="checkbox" id="show-all" onchange="toggleShowAll()">
                    <span>Show All Meetings (including hidden)</span>
                </label>
            </div>
        </div>

        <div class="auto-save-indicator" id="auto-save-indicator">💾 Auto-saved</div>

        {prompts_html}

        <div class="footer">
            <p>📊 Total Prompts: {total_prompts} | Generated with AI Classification (Qwen3-Embedding-0.6B)</p>
            <p>TimeBerry T+P © 2025 | BizChat Workback Planning DevUI Testing</p>
        </div>
    </div>

    <script>
        // Initial annotation data from previous testing session
        {initial_annotations_js}
        
        // Collapse/Expand functionality
        function togglePrompt(promptId) {{
            const content = document.getElementById('content-' + promptId);
            const icon = document.getElementById('icon-' + promptId);
            const wasCollapsed = !content.classList.contains('expanded');
            
            content.classList.toggle('expanded');
            icon.classList.toggle('collapsed');
            
            // Load saved data into fields when expanding for the first time
            if (wasCollapsed) {{
                loadFieldData(promptId);
            }}
        }}
        
        // Load field data for a specific prompt
        function loadFieldData(id) {{
            const data = JSON.parse(localStorage.getItem('devui_test_data') || '{{}}');
            if (data[id]) {{
                console.log('Loading data for prompt', id, ':', data[id]);
                const card = document.querySelector(`[data-prompt-id=\"${{id}}\"]`);
                if (!card) return;
                
                const inputMap = {{
                    'devuiLink': '.devui-link-input',
                    'sessionId': '.session-id-input',
                    'dateCaptured': '.date-input',
                    'toolsObserved': '.tools-input',
                    'zeroShotFeedback': '.zero-shot-feedback',
                    'overallFeedback': '.overall-feedback',
                    'notes': '.notes-input'
                }};
                
                Object.keys(inputMap).forEach(field => {{
                    const input = card.querySelector(inputMap[field]);
                    if (input && data[id][field]) {{
                        input.value = data[id][field];
                        console.log('  Set', field, 'to:', data[id][field].substring(0, 30) + '...');
                    }} else if (!input) {{
                        console.log('  Input not found for', field);\n                    }}
                }});
            }}
        }}

        // Expand all prompts
        function expandAll() {{
            document.querySelectorAll('.prompt-content').forEach(content => {{
                content.classList.add('expanded');
            }});
            document.querySelectorAll('.collapse-icon').forEach(icon => {{
                icon.classList.remove('collapsed');
            }});
        }}

        // Collapse all prompts
        function collapseAll() {{
            document.querySelectorAll('.prompt-content').forEach(content => {{
                content.classList.remove('expanded');
            }});
            document.querySelectorAll('.collapse-icon').forEach(icon => {{
                icon.classList.add('collapsed');
            }});
        }}

        // Auto-extract Session ID from DevUI link
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.devui-link-input').forEach(input => {{
                input.addEventListener('input', function(e) {{
                    const url = e.target.value;
                    const content = e.target.closest('.prompt-content');
                    const sessionIdInput = content.querySelector('.session-id-input');
                    
                    // Try different parameter names
                    const params = new URLSearchParams(url.split('?')[1] || '');
                    const sessionId = params.get('sharedSessionId') || 
                                    params.get('sessionId') || 
                                    params.get('sid') || 
                                    params.get('session') || '';
                    
                    if (sessionId && sessionIdInput) {{
                        sessionIdInput.value = sessionId;
                        console.log('Auto-extracted Session ID:', sessionId);
                    }}
                }});
            }});
        }});

        // Save data to localStorage
        function saveData() {{
            const data = {{}};
            const now = new Date().toISOString().split('T')[0]; // Today's date in YYYY-MM-DD format
            
            document.querySelectorAll('.prompt-card').forEach(card => {{
                const id = card.dataset.promptId;
                const dateInput = card.querySelector('.date-input');
                
                // Auto-set date to today if empty and there's data to save
                const hasData = card.querySelector('.devui-link-input')?.value || 
                               card.querySelector('.toolsObserved')?.value ||
                               card.querySelector('.zero-shot-feedback')?.value ||
                               card.querySelector('.overall-feedback')?.value ||
                               card.querySelector('.notes-input')?.value;
                               
                if (hasData && dateInput && !dateInput.value) {{
                    dateInput.value = now;
                }}
                
                data[id] = {{
                    devuiLink: card.querySelector('.devui-link-input')?.value || '',
                    sessionId: card.querySelector('.session-id-input')?.value || '',
                    dateCaptured: card.querySelector('.date-input')?.value || '',
                    toolsObserved: card.querySelector('.tools-input')?.value || '',
                    zeroShotFeedback: card.querySelector('.zero-shot-feedback')?.value || '',
                    overallFeedback: card.querySelector('.overall-feedback')?.value || '',
                    notes: card.querySelector('.notes-input')?.value || ''
                }};
            }});
            
            localStorage.setItem('devui_test_data', JSON.stringify(data));
            alert('✅ Data saved successfully!');
        }}

        // Load data from localStorage
        function loadData() {{
            const data = JSON.parse(localStorage.getItem('devui_test_data') || '{{}}');
            document.querySelectorAll('.prompt-card').forEach(card => {{
                const id = card.dataset.promptId;
                if (data[id]) {{
                    const fields = ['devuiLink', 'sessionId', 'dateCaptured', 'toolsObserved', 
                                  'zeroShotFeedback', 'overallFeedback', 'notes'];
                    fields.forEach(field => {{
                        const inputMap = {{
                            'devuiLink': '.devui-link-input',
                            'sessionId': '.session-id-input',
                            'dateCaptured': '.date-input',
                            'toolsObserved': '.tools-input',
                            'zeroShotFeedback': '.zero-shot-feedback',
                            'overallFeedback': '.overall-feedback',
                            'notes': '.notes-input'
                        }};
                        const input = card.querySelector(inputMap[field]);
                        if (input && data[id][field]) {{
                            input.value = data[id][field];
                        }}
                    }});
                }}
            }});
        }}

        // Load on page load
        window.addEventListener('load', loadData);

        // ===== SELECTION MANAGEMENT =====
        let autoSaveTimer = null;

        function updateSelectionCounter() {{
            // Count only non-synthetic (real meeting) selections
            const selectedCards = document.querySelectorAll('.prompt-card[data-selected="true"]');
            let realMeetingCount = 0;
            selectedCards.forEach(card => {{
                if (!card.classList.contains('synthetic')) {{
                    realMeetingCount++;
                }}
            }});
            
            const counter = document.getElementById('selection-counter');
            counter.textContent = realMeetingCount;
            
            // Visual feedback for goal (5 real meetings)
            if (realMeetingCount >= 5) {{
                counter.classList.add('goal-met');
            }} else {{
                counter.classList.remove('goal-met');
            }}
        }}

        function handleSelection(promptId, isSelected) {{
            const card = document.querySelector(`.prompt-card[data-prompt-id="${{promptId}}"]`);
            card.dataset.selected = isSelected;
            
            if (isSelected) {{
                card.classList.add('selected');
                card.classList.remove('unselected');
            }} else {{
                card.classList.remove('selected');
                card.classList.add('unselected');
            }}
            
            updateSelectionCounter();
            applyFilters();
            triggerAutoSave();
        }}

        function selectAll() {{
            document.querySelectorAll('.selection-checkbox').forEach(cb => {{
                cb.checked = true;
                const promptId = cb.closest('.prompt-card').dataset.promptId;
                handleSelection(promptId, true);
            }});
        }}

        function deselectAll() {{
            document.querySelectorAll('.selection-checkbox').forEach(cb => {{
                cb.checked = false;
                const promptId = cb.closest('.prompt-card').dataset.promptId;
                handleSelection(promptId, false);
            }});
        }}

        function toggleFilterUnselected() {{
            applyFilters();
        }}

        function toggleShowAll() {{
            applyFilters();
        }}

        function applyFilters() {{
            const filterUnselected = document.getElementById('filter-unselected').checked;
            const showAll = document.getElementById('show-all').checked;
            
            document.querySelectorAll('.prompt-card').forEach(card => {{
                const isSelected = card.dataset.selected === 'true';
                
                if (showAll) {{
                    // Show all cards
                    card.classList.remove('hidden');
                }} else if (filterUnselected && !isSelected) {{
                    // Hide unselected cards if filter is on
                    card.classList.add('hidden');
                }} else {{
                    card.classList.remove('hidden');
                }}
            }});
        }}

        // ===== AUTO-SAVE FUNCTIONALITY =====
        function triggerAutoSave() {{
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {{
                saveAllData(true); // true = silent auto-save
            }}, 30000); // 30 seconds
        }}

        function showAutoSaveIndicator() {{
            const indicator = document.getElementById('auto-save-indicator');
            indicator.classList.add('show');
            setTimeout(() => {{
                indicator.classList.remove('show');
            }}, 2000);
        }}

        function saveAllData(isAutoSave = false) {{
            const data = {{}};
            document.querySelectorAll('.prompt-card').forEach(card => {{
                const id = card.dataset.promptId;
                const isSelected = card.dataset.selected === 'true';
                const isSynthetic = card.classList.contains('synthetic');
                
                data[id] = {{
                    selected: isSelected,
                    devuiLink: card.querySelector('.devui-link-input')?.value || '',
                    sessionId: card.querySelector('.session-id-input')?.value || '',
                    dateCaptured: card.querySelector('.date-input')?.value || '',
                    toolsObserved: card.querySelector('.tools-input')?.value || '',
                    zeroShotFeedback: card.querySelector('.zero-shot-feedback')?.value || '',
                    overallFeedback: card.querySelector('.overall-feedback')?.value || '',
                    notes: card.querySelector('.notes-input')?.value || ''
                }};
                
                // Update completed styling dynamically
                const hasAnnotation = data[id].devuiLink || data[id].sessionId || 
                                     data[id].toolsObserved || data[id].zeroShotFeedback || 
                                     data[id].overallFeedback || data[id].notes;
                
                if (hasAnnotation && !isSynthetic) {{
                    card.classList.add('completed');
                    // Add completed badge if not already present
                    const title = card.querySelector('.prompt-card-title h2');
                    if (title && !title.querySelector('.completed-badge')) {{
                        const badge = document.createElement('span');
                        badge.className = 'completed-badge';
                        badge.textContent = '\u2705 Annotated';
                        title.appendChild(badge);
                    }}
                }} else {{
                    card.classList.remove('completed');
                    // Remove badge if present
                    const badge = card.querySelector('.completed-badge');
                    if (badge) {{
                        badge.remove();
                    }}
                }}
            }});
            
            localStorage.setItem('devui_test_data', JSON.stringify(data));
            
            if (isAutoSave) {{
                showAutoSaveIndicator();
            }} else {{
                alert('✅ Data saved successfully!');
            }}
        }}

        function loadAllData() {{
            // Check if localStorage is empty (first load)
            let data = JSON.parse(localStorage.getItem('devui_test_data') || '{{}}');
            
            // If empty and we have initial data, use it
            if (Object.keys(data).length === 0 && typeof INITIAL_ANNOTATIONS !== 'undefined') {{
                console.log('📥 Loading initial annotation data...');
                data = INITIAL_ANNOTATIONS;
                localStorage.setItem('devui_test_data', JSON.stringify(data));
                console.log('✅ Loaded ' + Object.keys(data).filter(k => data[k].devuiLink).length + ' existing annotations');
            }}
            
            document.querySelectorAll('.prompt-card').forEach(card => {{
                const id = card.dataset.promptId;
                const checkbox = card.querySelector('.selection-checkbox');
                const isSynthetic = card.classList.contains('synthetic');
                
                // Check if meeting has any annotation data
                const hasAnnotation = data[id] && (
                    data[id].devuiLink || 
                    data[id].sessionId || 
                    data[id].toolsObserved || 
                    data[id].zeroShotFeedback || 
                    data[id].overallFeedback || 
                    data[id].notes
                );
                
                // Add 'completed' class and badge for annotated meetings
                if (hasAnnotation && !isSynthetic) {{
                    card.classList.add('completed');
                    // Add completed badge if not already present
                    const title = card.querySelector('.prompt-card-title h2');
                    if (title && !title.querySelector('.completed-badge')) {{
                        const badge = document.createElement('span');
                        badge.className = 'completed-badge';
                        badge.textContent = '✅ Annotated';
                        title.appendChild(badge);
                    }}
                }}
                
                // Pre-select synthetic prompts OR meetings with annotations
                if (isSynthetic || hasAnnotation) {{
                    if (checkbox) {{
                        checkbox.checked = true;
                        handleSelection(id, true);
                    }}
                }} else if (data[id]) {{
                    // Load saved selection state for non-synthetic, non-annotated meetings
                    if (checkbox) {{
                        checkbox.checked = data[id].selected || false;
                        handleSelection(id, checkbox.checked);
                    }}
                }}
                
                // Load form fields from localStorage
                if (data[id]) {{
                    console.log('Loading data for prompt', id, ':', data[id]);
                }}
            }});
            updateSelectionCounter();
        }}

        // ===== EXPORT FUNCTIONALITY =====
        function exportLocalStorage() {{
            // Export raw localStorage for prompt regeneration
            const data = localStorage.getItem('devui_test_data');
            if (!data) {{
                alert('⚠️ No saved data found in localStorage');
                return;
            }}
            
            const blob = new Blob([data], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'annotated_data.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert('✅ Exported localStorage data!\\n\\nUse this file with check_annotated_meetings.py to preserve your annotated meetings when regenerating prompts.');
        }}

        function exportAnnotations() {{
            const exportData = {{
                metadata: {{
                    user: '{user_name}',
                    exportDate: new Date().toISOString(),
                    totalPrompts: document.querySelectorAll('.prompt-card').length,
                    selectedPrompts: document.querySelectorAll('.prompt-card[data-selected="true"]').length
                }},
                annotations: []
            }};
            
            document.querySelectorAll('.prompt-card[data-selected="true"]').forEach(card => {{
                const id = card.dataset.promptId;
                const title = card.querySelector('.prompt-card-title h2').textContent;
                const category = card.querySelector('.meta-value').textContent;
                
                exportData.annotations.push({{
                    id: id,
                    title: title,
                    category: category,
                    selected: true,
                    devuiLink: card.querySelector('.devui-link-input')?.value || '',
                    sessionId: card.querySelector('.session-id-input')?.value || '',
                    dateCaptured: card.querySelector('.date-input')?.value || '',
                    toolsObserved: card.querySelector('.tools-input')?.value || '',
                    zeroShotFeedback: card.querySelector('.zero-shot-feedback')?.value || '',
                    overallFeedback: card.querySelector('.overall-feedback')?.value || '',
                    notes: card.querySelector('.notes-input')?.value || ''
                }});
            }});
            
            // Create and download JSON file
            const blob = new Blob([JSON.stringify(exportData, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `bizchat_annotations_${{new Date().toISOString().split('T')[0]}}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert(`✅ Exported ${{exportData.annotations.length}} selected annotations!`);
        }}

        // ===== COPY PROMPT FUNCTIONALITY =====
        function copyPromptText(promptId) {{
            const promptText = document.getElementById(`prompt-text-${{promptId}}`);
            const copyButton = event.target.closest('.copy-prompt-button');
            const copyIcon = document.getElementById(`copy-icon-${{promptId}}`);
            
            // Get the text content (strip HTML)
            let text = promptText.innerText || promptText.textContent;
            
            // Remove synthetic scenario header if present
            text = text.replace(/\*\*\[EXPLORATION SCENARIO - Not from your calendar\]\*\*\s*/gi, '');
            text = text.trim();
            
            // Copy to clipboard
            navigator.clipboard.writeText(text).then(() => {{
                // Visual feedback
                copyButton.classList.add('copied');
                copyIcon.textContent = '✅';
                
                // Reset after 2 seconds
                setTimeout(() => {{
                    copyButton.classList.remove('copied');
                    copyIcon.textContent = '📋';
                }}, 2000);
            }}).catch(err => {{
                console.error('Failed to copy:', err);
                alert('Failed to copy prompt text');
            }});
        }}

        // Monitor input changes for auto-save
        document.addEventListener('input', (e) => {{
            if (e.target.matches('input, textarea')) {{
                triggerAutoSave();
            }}
        }});

        // Initialize on load
        window.addEventListener('load', () => {{
            loadAllData();
            updateSelectionCounter();
        }});
    </script>
</body>
</html>
"""

PROMPT_CARD_TEMPLATE = """
        <div class="prompt-card {selected_class}" data-prompt-id="{id}" data-selected="{selected}">
            <div class="prompt-card-header">
                <div class="prompt-card-header-left">
                    <input type="checkbox" class="selection-checkbox" 
                           onchange="handleSelection({id}, this.checked)" 
                           onclick="event.stopPropagation()"
                           {checked}>
                    <div class="prompt-card-title" onclick="togglePrompt({id})">
                        <h2>{role_icon} Prompt #{id}: {title}</h2>
                        <div class="meeting-info">📅 {real_meeting} | {user_role_display}</div>
                    </div>
                </div>
                <div class="collapse-icon collapsed" id="icon-{id}" onclick="togglePrompt({id})">▼</div>
            </div>

            <div class="prompt-content" id="content-{id}">
                <div class="prompt-meta">
                    <div class="meta-item">
                        <div class="meta-label">Category</div>
                        <div class="meta-value">{category}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Complexity</div>
                        <div class="meta-value">
                            <span class="complexity-badge complexity-{complexity}">{complexity}</span>
                        </div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Lead Time</div>
                        <div class="meta-value">{lead_time} days</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Your Role</div>
                        <div class="meta-value">{role_icon} {user_role_display}</div>
                    </div>
                    {meeting_meta_html}
                </div>

                <div class="prompt-text" id="prompt-text-{id}">{prompt}</div>

                <button class="copy-prompt-button" onclick="copyPromptText({id})">
                    <span id="copy-icon-{id}">📋</span> Copy Sample Prompt
                </button>

                <div class="meta-item" style="margin-bottom: 15px;">
                    <div class="meta-label">Expected Tools</div>
                    <div class="tools-grid">
                        {tools_html}
                    </div>
                </div>

                <div class="input-section">
                    <div class="input-group">
                        <label>📎 DevUI Link</label>
                        <input type="url" class="devui-link-input" placeholder="Paste DevUI session link here...">
                    </div>

                    <div class="input-group">
                        <label>🆔 Session ID (auto-extracted)</label>
                        <input type="text" class="session-id-input" placeholder="Session ID will auto-populate...">
                    </div>

                    <div class="input-group">
                        <label>📅 Date Captured</label>
                        <input type="date" class="date-input">
                    </div>

                    <div class="input-group">
                        <label>🛠️ Tools Observed</label>
                        <input type="text" class="tools-input" placeholder="e.g., graph_calendar_get_events, bizchat_search">
                    </div>

                    <div class="input-group">
                        <label>💭 Zero-Shot Feedback</label>
                        <textarea class="zero-shot-feedback" placeholder="How well did BizChat handle this prompt without additional context?"></textarea>
                    </div>

                    <div class="input-group">
                        <label>📝 Overall Feedback</label>
                        <textarea class="overall-feedback" placeholder="General observations, issues, or suggestions..."></textarea>
                    </div>

                    <div class="input-group">
                        <label>📌 Notes</label>
                        <textarea class="notes-input" placeholder="Additional notes or observations..."></textarea>
                    </div>

                    <button class="save-button" onclick="saveData()">💾 Save Progress</button>
                </div>
            </div>
        </div>
"""


def generate_html(json_path: str, output_path: str, user_name: str = "Unknown User"):
    """Generate HTML from JSON prompts"""
    
    # Load JSON
    with open(json_path, 'r') as f:
        prompts = json.load(f)
    
    # Load preserved meetings to mark as completed
    preserved_titles = set()
    preserve_file = Path(json_path).parent.parent / 'tools' / 'preserve_meetings.json'
    if preserve_file.exists():
        try:
            with open(preserve_file, 'r') as f:
                preserve_data = json.load(f)
                for meeting in preserve_data.get('meetings_to_preserve', []):
                    # Extract title without attendee count
                    title = meeting['realMeeting']
                    if ' (' in title:
                        title = title.rsplit(' (', 1)[0]
                    preserved_titles.add(title.lower().strip())
        except:
            pass
    
    # Collect statistics
    categories = {}
    complexities = {}
    roles = {'organizer': 0, 'participant': 0}
    total_attendees = 0
    
    for prompt in prompts:
        # Count by category
        cat = prompt.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
        
        # Count by complexity
        comp = prompt.get('complexity', 'unknown')
        complexities[comp] = complexities.get(comp, 0) + 1
        
        # Count by role
        role = prompt.get('userRole', 'participant')
        roles[role] = roles.get(role, 0) + 1
    
    # Generate statistics section
    category_items = '\n'.join([
        f'            <div class="stat-card">\n'
        f'                <div class="stat-label">{cat}</div>\n'
        f'                <div class="stat-value">{count}</div>\n'
        f'            </div>'
        for cat, count in categories.items()
    ])
    
    complexity_badges = {
        'high': '🔴',
        'medium': '🟡', 
        'low': '🟢'
    }
    
    complexity_items = '\n'.join([
        f'            <div class="stat-card">\n'
        f'                <div class="stat-label">{complexity_badges.get(comp.lower(), "⚪")} {comp.title()}</div>\n'
        f'                <div class="stat-value">{count}</div>\n'
        f'            </div>'
        for comp, count in complexities.items()
    ])
    
    statistics_html = f"""
        <div class="statistics-section">
            <h2>📊 Meeting Selection Summary</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Prompts</div>
                    <div class="stat-value">{len(prompts)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">👤 As Organizer</div>
                    <div class="stat-value">{roles.get('organizer', 0)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">👥 As Participant</div>
                    <div class="stat-value">{roles.get('participant', 0)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Meeting Categories</div>
                    <div class="stat-value">{len(categories)}</div>
                </div>
            </div>

            <h3 style="color: #323130; font-size: 1.1em; margin: 20px 0 10px 0;">📋 By Category</h3>
            <div class="stats-grid">
{category_items}
            </div>

            <h3 style="color: #323130; font-size: 1.1em; margin: 20px 0 10px 0;">⚡ By Complexity</h3>
            <div class="stats-grid">
{complexity_items}
            </div>

            <div class="filter-info">
                <h3>🎯 Selection Criteria</h3>
                <ul>
                    <li><strong>AI Classification:</strong> Qwen3-Embedding-0.6B (100% coverage)</li>
                    <li><strong>Role Detection:</strong> Prioritized organizer meetings (minimum {roles.get('organizer', 0)})</li>
                    <li><strong>Diversity:</strong> Maximum 3 meetings per category</li>
                    <li><strong>Quality:</strong> Sorted by confidence score and attendee count</li>
                    <li><strong>Source:</strong> Real calendar data from {user_name}</li>
                </ul>
            </div>
        </div>
"""
    
    # Sort prompts: synthetic first, then real meetings
    synthetic_prompts = [p for p in prompts if p.get('isSynthetic', False)]
    real_prompts = [p for p in prompts if not p.get('isSynthetic', False)]
    sorted_prompts = synthetic_prompts + real_prompts
    
    # Generate prompt cards
    prompts_html = []
    for prompt in sorted_prompts:
        user_role = prompt.get('userRole', 'participant')
        role_icon = "👤" if user_role == "organizer" else "👥"
        user_role_display = "Meeting Organizer" if user_role == "organizer" else "Meeting Participant"
        
        # Handle synthetic scenarios - pre-select them
        is_synthetic = prompt.get('isSynthetic', False)
        
        # Check if this meeting was previously annotated (preserved)
        meeting_title = prompt.get('realMeeting', '')
        if ' (' in meeting_title:
            meeting_title = meeting_title.rsplit(' (', 1)[0]
        is_preserved = meeting_title.lower().strip() in preserved_titles
        
        # Pre-select synthetic prompts and preserved meetings, respect saved state for others
        if is_synthetic:
            selected = True  # Always pre-select synthetic
            selected_class = 'selected synthetic'
            synthetic_badge = '<span class="synthetic-badge">🎭 EXPLORATION SCENARIO</span>'
        elif is_preserved:
            selected = True  # Pre-select preserved meetings
            selected_class = 'selected completed'
            synthetic_badge = '<span class="completed-badge">✅ Annotated</span>'
        else:
            selected = prompt.get('selected', False)
            selected_class = 'selected' if selected else 'unselected'
            synthetic_badge = ''
        
        checked = 'checked' if selected else ''
        
        tools_html = '\n                    '.join([
            f'<span class="tool-tag">{tool}</span>' 
            for tool in prompt.get('expectedTools', [])
        ])
        
        # Build meeting metadata HTML (only for real meetings)
        meeting_meta_html = ""
        if not is_synthetic and prompt.get('meetingDate'):
            meta_items = []
            
            # Meeting Date & Time
            if prompt.get('meetingDate'):
                date_display = prompt['meetingDate']
                if prompt.get('meetingTime'):
                    date_display += f" at {prompt['meetingTime']}"
                if prompt.get('meetingDuration'):
                    date_display += f" ({prompt['meetingDuration']})"
                meta_items.append(f'''
                    <div class="meta-item">
                        <div class="meta-label">📅 Meeting Date</div>
                        <div class="meta-value">{date_display}</div>
                    </div>''')
            
            # Location
            if prompt.get('meetingLocation'):
                location_icon = "🌐" if prompt.get('isOnline') else "📍"
                meta_items.append(f'''
                    <div class="meta-item">
                        <div class="meta-label">{location_icon} Location</div>
                        <div class="meta-value">{prompt['meetingLocation']}</div>
                    </div>''')
            
            # Organizer
            if prompt.get('organizerName'):
                organizer_display = prompt['organizerName']
                if prompt.get('organizerEmail'):
                    organizer_display += f" ({prompt['organizerEmail']})"
                meta_items.append(f'''
                    <div class="meta-item">
                        <div class="meta-label">👤 Organizer</div>
                        <div class="meta-value">{organizer_display}</div>
                    </div>''')
            
            # Attendee Count
            if prompt.get('attendeeCount'):
                meta_items.append(f'''
                    <div class="meta-item">
                        <div class="meta-label">👥 Attendees</div>
                        <div class="meta-value">{prompt['attendeeCount']} people</div>
                    </div>''')
            
            meeting_meta_html = '\n'.join(meta_items)
        
        card_html = PROMPT_CARD_TEMPLATE.format(
            id=prompt['id'],
            title=prompt['title'] + synthetic_badge,
            real_meeting=prompt['realMeeting'],
            user_role=user_role,
            user_role_display=user_role_display,
            role_icon=role_icon,
            selected='true' if selected else 'false',
            selected_class=selected_class,
            checked=checked,
            category=prompt['category'],
            complexity=prompt['complexity'],
            lead_time=prompt['leadTime'],
            prompt=prompt['prompt'],
            tools_html=tools_html,
            meeting_meta_html=meeting_meta_html
        )
        prompts_html.append(card_html)
    
    # Load initial annotation data if available
    initial_annotations_js = "// No initial annotations"
    initial_localstorage_path = Path(__file__).parent / 'initial_localstorage.json'
    if initial_localstorage_path.exists():
        try:
            with open(initial_localstorage_path, 'r') as f:
                initial_data = json.load(f)
            initial_annotations_js = f"const INITIAL_ANNOTATIONS = {json.dumps(initial_data, indent=2)};"
            print(f"📥 Loaded initial annotation data for {sum(1 for v in initial_data.values() if v.get('devuiLink'))} meetings")
        except Exception as e:
            print(f"⚠️  Could not load initial annotations: {e}")
    
    # Generate final HTML
    html = HTML_TEMPLATE.format(
        user_name=user_name,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_prompts=len(prompts),
        prompts_html=statistics_html + '\n' + '\n'.join(prompts_html),
        initial_annotations_js=initial_annotations_js
    )
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Generated HTML: {output_path}")
    print(f"📊 Total prompts: {len(prompts)}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python json_to_html.py <json_file> <output_html> <user_name>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    user_name = sys.argv[3]
    
    generate_html(json_path, output_path, user_name)
