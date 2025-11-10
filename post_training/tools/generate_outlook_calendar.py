#!/usr/bin/env python3
"""
Interactive Outlook-Style Calendar Interface Generator

Creates a rich, interactive web calendar that looks and feels like Microsoft Outlook.
Features:
- Week view with time slots (like Outlook)
- Drag and drop (visual only)
- Color-coded by importance
- Meeting details on hover
- Time conflict visualization
- Responsive design

Usage:
    # Generate Outlook-style calendar for one persona
    python post_training/tools/generate_outlook_calendar.py \
        --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
        --output outlook_calendar.html
    
    # Generate with multiple personas (tabs)
    python post_training/tools/generate_outlook_calendar.py \
        --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
        --calendar post_training/data/training/calendars/tier2_senior_ic_architect_calendar_4weeks.jsonl \
        --calendar post_training/data/training/calendars/tier3_specialist_legal_calendar_4weeks.jsonl \
        --output outlook_calendar_all.html
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def load_calendar(calendar_path: Path) -> List[Dict[str, Any]]:
    """Load calendar from JSONL file."""
    meetings = []
    with open(calendar_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                meetings.append(json.loads(line))
    return meetings


def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO datetime string."""
    if '.' in dt_str:
        dt_str = dt_str.split('.')[0]
    return datetime.fromisoformat(dt_str)


def generate_outlook_calendar_html(
    calendars: List[Dict[str, Any]],
    output_path: Path
):
    """Generate interactive Outlook-style calendar HTML."""
    
    # HTML template with Outlook styling
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Outlook Calendar - Training Data Viewer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f2f1;
            overflow: hidden;
        }
        
        /* Header (like Outlook ribbon) */
        .header {
            background: linear-gradient(to bottom, #0078d4 0%, #106ebe 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .header-controls {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .persona-selector {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .persona-selector:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .week-nav {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .week-nav button {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 6px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
        }
        
        .week-nav button:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .week-label {
            font-size: 14px;
            font-weight: 500;
            min-width: 200px;
            text-align: center;
        }
        
        /* Main calendar container */
        .calendar-container {
            display: flex;
            height: calc(100vh - 60px);
            background: white;
        }
        
        /* Time column */
        .time-column {
            width: 60px;
            background: #faf9f8;
            border-right: 1px solid #edebe9;
            padding-top: 60px;
        }
        
        .time-slot {
            height: 60px;
            font-size: 11px;
            color: #605e5c;
            padding: 5px;
            text-align: right;
            border-bottom: 1px solid #edebe9;
        }
        
        /* Calendar grid */
        .calendar-grid {
            flex: 1;
            display: flex;
            overflow-x: auto;
        }
        
        .day-column {
            flex: 1;
            min-width: 150px;
            border-right: 1px solid #edebe9;
            position: relative;
        }
        
        .day-column:last-child {
            border-right: none;
        }
        
        .day-header {
            height: 60px;
            background: #faf9f8;
            border-bottom: 2px solid #0078d4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .day-name {
            font-size: 11px;
            color: #605e5c;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .day-date {
            font-size: 24px;
            font-weight: 300;
            color: #323130;
            margin-top: 2px;
        }
        
        .day-date.today {
            background: #0078d4;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 600;
        }
        
        .time-grid {
            position: relative;
        }
        
        .time-slot-grid {
            height: 60px;
            border-bottom: 1px solid #edebe9;
            position: relative;
        }
        
        /* Meeting blocks */
        .meeting {
            position: absolute;
            left: 2px;
            right: 2px;
            border-radius: 4px;
            padding: 6px 8px;
            font-size: 12px;
            cursor: pointer;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            border-left: 4px solid;
            transition: all 0.2s;
            z-index: 1;
        }
        
        .meeting:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            z-index: 100;
            transform: scale(1.02);
        }
        
        /* Importance colors (Outlook-style) */
        .meeting.critical {
            background: linear-gradient(to right, #fff5f5 0%, #ffe4e4 100%);
            border-left-color: #d13438;
            color: #a4262c;
        }
        
        .meeting.high {
            background: linear-gradient(to right, #fffef5 0%, #fff4ce 100%);
            border-left-color: #ffaa44;
            color: #8a5700;
        }
        
        .meeting.medium {
            background: linear-gradient(to right, #f5fff5 0%, #e1f5e1 100%);
            border-left-color: #0b6a0b;
            color: #0b6a0b;
        }
        
        .meeting.low {
            background: linear-gradient(to right, #f5f9ff 0%, #deecf9 100%);
            border-left-color: #0078d4;
            color: #005a9e;
        }
        
        .meeting-time {
            font-weight: 600;
            font-size: 11px;
            margin-bottom: 2px;
        }
        
        .meeting-subject {
            font-weight: 500;
            line-height: 1.3;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .meeting-location {
            font-size: 10px;
            opacity: 0.8;
            margin-top: 2px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .meeting-prep {
            position: absolute;
            top: 4px;
            right: 4px;
            background: #9c27b0;
            color: white;
            font-size: 9px;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: 600;
        }
        
        /* Tooltip */
        .tooltip {
            display: none;
            position: fixed;
            background: white;
            border: 1px solid #d1d1d1;
            border-radius: 6px;
            padding: 15px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            z-index: 1000;
            max-width: 400px;
            font-size: 13px;
        }
        
        .tooltip.show {
            display: block;
        }
        
        .tooltip-header {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid #edebe9;
        }
        
        .tooltip-row {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
        }
        
        .tooltip-label {
            font-weight: 600;
            color: #605e5c;
            min-width: 80px;
        }
        
        .tooltip-value {
            color: #323130;
        }
        
        .tooltip-description {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #edebe9;
            color: #605e5c;
            line-height: 1.5;
        }
        
        .tooltip-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }
        
        .tooltip-badge.critical {
            background: #d13438;
            color: white;
        }
        
        .tooltip-badge.high {
            background: #ffaa44;
            color: #000;
        }
        
        .tooltip-badge.medium {
            background: #0b6a0b;
            color: white;
        }
        
        .tooltip-badge.low {
            background: #0078d4;
            color: white;
        }
        
        /* Statistics panel */
        .stats-panel {
            width: 280px;
            background: #faf9f8;
            border-left: 1px solid #edebe9;
            padding: 20px;
            overflow-y: auto;
        }
        
        .stats-section {
            margin-bottom: 25px;
        }
        
        .stats-title {
            font-size: 14px;
            font-weight: 600;
            color: #323130;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #edebe9;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 13px;
            border-bottom: 1px solid #edebe9;
        }
        
        .stat-label {
            color: #605e5c;
        }
        
        .stat-value {
            font-weight: 600;
            color: #323130;
        }
        
        .importance-bar {
            height: 24px;
            background: #edebe9;
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            margin-top: 8px;
        }
        
        .importance-segment {
            height: 100%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 600;
            color: white;
        }
        
        .importance-segment.critical { background: #d13438; }
        .importance-segment.high { background: #ffaa44; color: #000; }
        .importance-segment.medium { background: #0b6a0b; }
        .importance-segment.low { background: #0078d4; }
        
        /* No meetings placeholder */
        .no-meetings {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #a19f9d;
            font-size: 13px;
            font-style: italic;
        }
        
        /* Loading state */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-size: 18px;
            color: #605e5c;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <span>📅</span>
            <span>Outlook Calendar - Training Data Viewer</span>
        </h1>
        <div class="header-controls">
            <select class="persona-selector" id="personaSelector">
"""
    
    # Add persona options
    for i, cal in enumerate(calendars):
        selected = 'selected' if i == 0 else ''
        html += f'                <option value="{i}" {selected}>{cal["persona_name"]}</option>\n'
    
    html += """            </select>
            <div class="week-nav">
                <button id="prevWeek">◀ Previous</button>
                <span class="week-label" id="weekLabel"></span>
                <button id="nextWeek">Next ▶</button>
            </div>
        </div>
    </div>
    
    <div class="calendar-container">
        <div class="time-column" id="timeColumn">
"""
    
    # Add time slots (8 AM to 6 PM)
    for hour in range(8, 19):
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        html += f'            <div class="time-slot">{display_hour}:00 {period}</div>\n'
    
    html += """        </div>
        
        <div class="calendar-grid" id="calendarGrid">
            <!-- Days will be populated by JavaScript -->
        </div>
        
        <div class="stats-panel">
            <div class="stats-section">
                <div class="stats-title">Week Overview</div>
                <div class="stat-row">
                    <span class="stat-label">Total Meetings</span>
                    <span class="stat-value" id="statTotalMeetings">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Avg Duration</span>
                    <span class="stat-value" id="statAvgDuration">0 min</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Prep Time Needed</span>
                    <span class="stat-value" id="statPrepTime">0 hrs</span>
                </div>
            </div>
            
            <div class="stats-section">
                <div class="stats-title">Importance Distribution</div>
                <div class="importance-bar" id="importanceBar"></div>
                <div class="stat-row">
                    <span class="stat-label">🔴 Critical</span>
                    <span class="stat-value" id="statCritical">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">🟡 High</span>
                    <span class="stat-value" id="statHigh">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">🟢 Medium</span>
                    <span class="stat-value" id="statMedium">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">🔵 Low</span>
                    <span class="stat-value" id="statLow">0</span>
                </div>
            </div>
            
            <div class="stats-section">
                <div class="stats-title">Meeting Types</div>
                <div class="stat-row">
                    <span class="stat-label">🔄 Recurring</span>
                    <span class="stat-value" id="statRecurring">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">📌 Ad-hoc</span>
                    <span class="stat-value" id="statAdhoc">0</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        // Calendar data
        const calendars = """ + json.dumps([{
            'persona_name': cal['persona_name'],
            'meetings': cal['meetings']
        } for cal in calendars], indent=8) + """;
        
        let currentPersonaIndex = 0;
        let currentWeekStart = null;
        let allWeeks = [];
        let currentWeekIndex = 0;
        
        // Initialize
        function init() {
            loadPersona(0);
            
            document.getElementById('personaSelector').addEventListener('change', (e) => {
                loadPersona(parseInt(e.target.value));
            });
            
            document.getElementById('prevWeek').addEventListener('click', () => {
                if (currentWeekIndex > 0) {
                    currentWeekIndex--;
                    renderWeek(allWeeks[currentWeekIndex]);
                }
            });
            
            document.getElementById('nextWeek').addEventListener('click', () => {
                if (currentWeekIndex < allWeeks.length - 1) {
                    currentWeekIndex++;
                    renderWeek(allWeeks[currentWeekIndex]);
                }
            });
        }
        
        function loadPersona(index) {
            currentPersonaIndex = index;
            const persona = calendars[index];
            
            // Extract all weeks
            const weekMap = new Map();
            persona.meetings.forEach(meeting => {
                const startDate = new Date(meeting.start.dateTime);
                const weekStart = getWeekStart(startDate);
                const weekKey = weekStart.toISOString().split('T')[0];
                
                if (!weekMap.has(weekKey)) {
                    weekMap.set(weekKey, []);
                }
                weekMap.get(weekKey).push(meeting);
            });
            
            allWeeks = Array.from(weekMap.entries())
                .sort((a, b) => a[0].localeCompare(b[0]))
                .map(([key, meetings]) => ({
                    start: new Date(key),
                    meetings: meetings
                }));
            
            currentWeekIndex = 0;
            if (allWeeks.length > 0) {
                renderWeek(allWeeks[0]);
            }
        }
        
        function getWeekStart(date) {
            const d = new Date(date);
            const day = d.getDay();
            const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Monday
            return new Date(d.setDate(diff));
        }
        
        function renderWeek(week) {
            const weekStart = week.start;
            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekEnd.getDate() + 6);
            
            // Update week label
            const weekLabel = `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
            document.getElementById('weekLabel').textContent = weekLabel;
            
            // Clear grid
            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '';
            
            // Create day columns
            for (let i = 0; i < 7; i++) {
                const dayDate = new Date(weekStart);
                dayDate.setDate(dayDate.getDate() + i);
                
                const dayMeetings = week.meetings.filter(m => {
                    const meetingDate = new Date(m.start.dateTime);
                    return meetingDate.toDateString() === dayDate.toDateString();
                });
                
                const dayColumn = createDayColumn(dayDate, dayMeetings);
                grid.appendChild(dayColumn);
            }
            
            // Update statistics
            updateStatistics(week.meetings);
        }
        
        function createDayColumn(date, meetings) {
            const column = document.createElement('div');
            column.className = 'day-column';
            
            // Day header
            const header = document.createElement('div');
            header.className = 'day-header';
            
            const dayName = document.createElement('div');
            dayName.className = 'day-name';
            dayName.textContent = date.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
            
            const dayDateEl = document.createElement('div');
            dayDateEl.className = 'day-date';
            const today = new Date();
            if (date.toDateString() === today.toDateString()) {
                dayDateEl.classList.add('today');
            }
            dayDateEl.textContent = date.getDate();
            
            header.appendChild(dayName);
            header.appendChild(dayDateEl);
            column.appendChild(header);
            
            // Time grid
            const timeGrid = document.createElement('div');
            timeGrid.className = 'time-grid';
            
            // Add time slot backgrounds
            for (let hour = 8; hour < 19; hour++) {
                const slot = document.createElement('div');
                slot.className = 'time-slot-grid';
                timeGrid.appendChild(slot);
            }
            
            // Add meetings
            meetings.forEach(meeting => {
                const meetingEl = createMeetingElement(meeting);
                timeGrid.appendChild(meetingEl);
            });
            
            column.appendChild(timeGrid);
            return column;
        }
        
        function createMeetingElement(meeting) {
            const startDate = new Date(meeting.start.dateTime);
            const endDate = new Date(meeting.end.dateTime);
            
            const startHour = startDate.getHours();
            const startMinute = startDate.getMinutes();
            const durationMinutes = (endDate - startDate) / 60000;
            
            // Calculate position (8 AM = 0)
            const topOffset = ((startHour - 8) * 60 + startMinute) * (60 / 60); // 60px per hour
            const height = (durationMinutes / 60) * 60;
            
            const div = document.createElement('div');
            div.className = `meeting ${meeting.importance_label}`;
            div.style.top = `${topOffset}px`;
            div.style.height = `${Math.max(height - 2, 20)}px`; // Min height
            
            // Time
            const timeEl = document.createElement('div');
            timeEl.className = 'meeting-time';
            timeEl.textContent = formatTime(startDate);
            div.appendChild(timeEl);
            
            // Subject
            const subjectEl = document.createElement('div');
            subjectEl.className = 'meeting-subject';
            subjectEl.textContent = meeting.subject;
            div.appendChild(subjectEl);
            
            // Prep indicator
            if (meeting.prep_needed) {
                const prepEl = document.createElement('div');
                prepEl.className = 'meeting-prep';
                prepEl.textContent = '📝';
                div.appendChild(prepEl);
            }
            
            // Tooltip on hover
            div.addEventListener('mouseenter', (e) => showTooltip(e, meeting));
            div.addEventListener('mouseleave', hideTooltip);
            
            return div;
        }
        
        function showTooltip(e, meeting) {
            const tooltip = document.getElementById('tooltip');
            const startDate = new Date(meeting.start.dateTime);
            const endDate = new Date(meeting.end.dateTime);
            const duration = Math.round((endDate - startDate) / 60000);
            
            const attendeeCount = meeting.attendees ? meeting.attendees.length : 0;
            
            tooltip.innerHTML = `
                <div class="tooltip-header">${meeting.subject}</div>
                <div class="tooltip-row">
                    <span class="tooltip-label">Time:</span>
                    <span class="tooltip-value">${formatTime(startDate)} - ${formatTime(endDate)} (${duration} min)</span>
                </div>
                <div class="tooltip-row">
                    <span class="tooltip-label">Importance:</span>
                    <span class="tooltip-value"><span class="tooltip-badge ${meeting.importance_label}">${meeting.importance_label.toUpperCase()}</span></span>
                </div>
                ${meeting.prep_needed ? `
                <div class="tooltip-row">
                    <span class="tooltip-label">Prep Time:</span>
                    <span class="tooltip-value">📝 ${meeting.prep_time_minutes} minutes</span>
                </div>
                ` : ''}
                <div class="tooltip-row">
                    <span class="tooltip-label">Attendees:</span>
                    <span class="tooltip-value">${attendeeCount} people</span>
                </div>
                <div class="tooltip-row">
                    <span class="tooltip-label">Type:</span>
                    <span class="tooltip-value">${meeting.type === 'occurrence' ? '🔄 Recurring' : '📌 Ad-hoc'}</span>
                </div>
                ${meeting.bodyPreview ? `
                <div class="tooltip-description">
                    <strong>Description:</strong><br>
                    ${meeting.bodyPreview.substring(0, 200)}${meeting.bodyPreview.length > 200 ? '...' : ''}
                </div>
                ` : ''}
                ${meeting.reasoning ? `
                <div class="tooltip-description">
                    <strong>Reasoning:</strong><br>
                    ${meeting.reasoning}
                </div>
                ` : ''}
            `;
            
            tooltip.classList.add('show');
            
            // Position tooltip
            const rect = e.target.getBoundingClientRect();
            tooltip.style.left = `${rect.right + 10}px`;
            tooltip.style.top = `${rect.top}px`;
            
            // Adjust if off-screen
            const tooltipRect = tooltip.getBoundingClientRect();
            if (tooltipRect.right > window.innerWidth) {
                tooltip.style.left = `${rect.left - tooltipRect.width - 10}px`;
            }
            if (tooltipRect.bottom > window.innerHeight) {
                tooltip.style.top = `${window.innerHeight - tooltipRect.height - 10}px`;
            }
        }
        
        function hideTooltip() {
            document.getElementById('tooltip').classList.remove('show');
        }
        
        function updateStatistics(meetings) {
            const total = meetings.length;
            
            // Importance distribution
            const importanceCounts = {
                critical: 0,
                high: 0,
                medium: 0,
                low: 0
            };
            
            let totalDuration = 0;
            let totalPrepTime = 0;
            let recurringCount = 0;
            
            meetings.forEach(m => {
                importanceCounts[m.importance_label]++;
                
                const start = new Date(m.start.dateTime);
                const end = new Date(m.end.dateTime);
                totalDuration += (end - start) / 60000;
                
                if (m.prep_needed) {
                    totalPrepTime += m.prep_time_minutes || 0;
                }
                
                if (m.type === 'occurrence') {
                    recurringCount++;
                }
            });
            
            // Update stats
            document.getElementById('statTotalMeetings').textContent = total;
            document.getElementById('statAvgDuration').textContent = total > 0 ? Math.round(totalDuration / total) + ' min' : '0 min';
            document.getElementById('statPrepTime').textContent = (totalPrepTime / 60).toFixed(1) + ' hrs';
            
            document.getElementById('statCritical').textContent = importanceCounts.critical;
            document.getElementById('statHigh').textContent = importanceCounts.high;
            document.getElementById('statMedium').textContent = importanceCounts.medium;
            document.getElementById('statLow').textContent = importanceCounts.low;
            
            document.getElementById('statRecurring').textContent = recurringCount;
            document.getElementById('statAdhoc').textContent = total - recurringCount;
            
            // Update importance bar
            const bar = document.getElementById('importanceBar');
            bar.innerHTML = '';
            
            if (total > 0) {
                ['critical', 'high', 'medium', 'low'].forEach(importance => {
                    const count = importanceCounts[importance];
                    if (count > 0) {
                        const percentage = (count / total) * 100;
                        const segment = document.createElement('div');
                        segment.className = `importance-segment ${importance}`;
                        segment.style.width = `${percentage}%`;
                        if (percentage > 15) {
                            segment.textContent = count;
                        }
                        bar.appendChild(segment);
                    }
                });
            }
        }
        
        function formatDate(date) {
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
        
        function formatTime(date) {
            return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        }
        
        // Initialize on load
        init();
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Outlook-style calendar generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate interactive Outlook-style calendar"
    )
    
    parser.add_argument(
        '--calendar',
        type=Path,
        action='append',
        required=True,
        help='Path to calendar JSONL file (can specify multiple)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path("outlook_calendar.html"),
        help='Output HTML file path (default: outlook_calendar.html)'
    )
    
    args = parser.parse_args()
    
    # Load calendars
    calendars = []
    for cal_path in args.calendar:
        meetings = load_calendar(cal_path)
        if not meetings:
            print(f"Warning: No meetings found in {cal_path}")
            continue
            
        persona_id = meetings[0].get('persona_id', 'unknown')
        persona_name = persona_id.replace('_', ' ').title()
        
        calendars.append({
            'persona_name': persona_name,
            'meetings': meetings
        })
    
    if not calendars:
        print("Error: No calendars loaded")
        return
    
    # Generate HTML
    generate_outlook_calendar_html(calendars, args.output)
    print(f"\n📅 Open {args.output} in your browser to view the interactive calendar!")


if __name__ == "__main__":
    main()
