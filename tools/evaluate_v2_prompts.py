#!/usr/bin/env python3
"""
Interactive UX for Evaluating GPT-5 V2 Hero Prompts Analysis
Reviews decomposition accuracy using 24 Canonical Tasks framework
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import webbrowser
import http.server
import socketserver
import threading

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class V2EvaluationServer:
    """Web server for v2 evaluation UX"""
    
    def __init__(self):
        self.project_root = project_root
        self.v2_results = self._load_v2_results()
        self.canonical_tasks = self._load_canonical_tasks_24()
        self.evaluation_results = {}
        self.port = 8080
        
    def _load_v2_results(self) -> Dict:
        """Load GPT-5 v2 analysis results"""
        results_file = self.project_root / "docs/gutt_analysis/gpt5_v2_analysis_20251107_125720.json"
        print(f"[LOADING] V2 analysis from {results_file.name}")
        
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[OK] Loaded {len(data['prompts'])} v2 prompt analyses")
        return data
    
    def _load_canonical_tasks_24(self) -> List[Dict]:
        """Load all 24 canonical tasks (v2.0) for selection"""
        tasks = [
            # Tier 1: Universal (5 tasks)
            {"id": "CAN-01", "name": "Calendar Events Retrieval", "tier": 1},
            {"id": "CAN-02A", "name": "Meeting Type Classification", "tier": 1},
            {"id": "CAN-02B", "name": "Meeting Priority Classification", "tier": 1},
            {"id": "CAN-03", "name": "Calendar Event Creation/Update", "tier": 1},
            {"id": "CAN-04", "name": "Natural Language Understanding (Constraint/Intent Extraction)", "tier": 1},
            {"id": "CAN-05", "name": "Attendee/Contact Resolution", "tier": 1},
            
            # Tier 2: Common (9 tasks)
            {"id": "CAN-06", "name": "Availability Checking (Free/Busy)", "tier": 2},
            {"id": "CAN-07", "name": "Meeting Metadata Extraction", "tier": 2},
            {"id": "CAN-08", "name": "Document/Content Retrieval", "tier": 2},
            {"id": "CAN-09", "name": "Document Generation/Formatting", "tier": 2},
            {"id": "CAN-10", "name": "Time Aggregation/Statistical Analysis", "tier": 2},
            {"id": "CAN-11", "name": "Priority/Preference Matching", "tier": 2},
            {"id": "CAN-12", "name": "Constraint Satisfaction", "tier": 2},
            {"id": "CAN-13", "name": "RSVP Status Update", "tier": 2},
            {"id": "CAN-14", "name": "Recommendation Engine", "tier": 2},
            
            # Tier 3: Specialized (10 tasks)
            {"id": "CAN-15", "name": "Recurrence Rule Generation", "tier": 3},
            {"id": "CAN-16", "name": "Event Monitoring/Change Detection", "tier": 3},
            {"id": "CAN-17", "name": "Automatic Rescheduling", "tier": 3},
            {"id": "CAN-18", "name": "Objection/Risk Anticipation", "tier": 3},
            {"id": "CAN-19", "name": "Resource Booking (Rooms/Equipment)", "tier": 3},
            {"id": "CAN-20", "name": "Data Visualization/Reporting", "tier": 3},
            {"id": "CAN-21", "name": "Focus Time/Preparation Time Analysis", "tier": 3},
            {"id": "CAN-22", "name": "Research/Intelligence Gathering", "tier": 3},
            {"id": "CAN-23", "name": "Agenda Generation/Structuring", "tier": 3},
            {"id": "CAN-24", "name": "Multi-party Coordination/Negotiation", "tier": 3},
        ]
        return tasks
    
    def generate_html(self) -> str:
        """Generate HTML for v2 evaluation interface"""
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT-5 V2 Hero Prompts Evaluation (24 Canonical Tasks)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .framework-badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 10px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .progress-bar {
            background: white;
            padding: 20px 30px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .progress-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .progress-track {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
            width: 0%;
        }
        
        .content {
            padding: 30px;
        }
        
        .prompt-selector {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .prompt-btn {
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            font-weight: 500;
        }
        
        .prompt-btn:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .prompt-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .prompt-btn.evaluated {
            background: #4caf50;
            color: white;
            border-color: #4caf50;
        }
        
        .evaluation-panel {
            display: none;
        }
        
        .evaluation-panel.active {
            display: block;
        }
        
        .section {
            background: #f9f9f9;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
        }
        
        .section h2 {
            color: #333;
            font-size: 20px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .prompt-text {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-size: 16px;
            line-height: 1.6;
            color: #555;
            margin-bottom: 20px;
        }
        
        .task-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        
        .task-item:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .task-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .task-checkbox {
            width: 24px;
            height: 24px;
            margin-right: 15px;
            cursor: pointer;
            accent-color: #667eea;
        }
        
        .task-id {
            font-weight: bold;
            color: #667eea;
            font-size: 14px;
            margin-right: 10px;
        }
        
        .task-name {
            font-size: 16px;
            color: #333;
            flex: 1;
        }
        
        .tier-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .tier-1 { background: #e3f2fd; color: #1976d2; }
        .tier-2 { background: #fff3e0; color: #f57c00; }
        .tier-3 { background: #fce4ec; color: #c2185b; }
        
        .execution-plan {
            margin-top: 20px;
        }
        
        .step-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .step-item:hover {
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .step-item.incorrect {
            border-left-color: #f44336;
            background: #ffebee;
        }
        
        .step-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .step-number {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }
        
        .step-content {
            display: grid;
            gap: 12px;
            font-size: 14px;
        }
        
        .step-field {
            display: flex;
            gap: 10px;
            align-items: flex-start;
        }
        
        .step-label {
            font-weight: 600;
            color: #555;
            min-width: 140px;
            flex-shrink: 0;
        }
        
        .step-value {
            color: #666;
            flex: 1;
            line-height: 1.6;
        }
        
        .schema-code {
            display: block;
            background: #f5f5f5;
            padding: 12px;
            border-radius: 6px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: #333;
            white-space: pre-wrap;
            overflow-x: auto;
            flex: 1;
            border: 1px solid #e0e0e0;
        }
        
        .add-task-section {
            margin-top: 20px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 8px;
        }
        
        .add-task-section h3 {
            color: #1976d2;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .task-selector {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 10px;
        }
        
        .task-option {
            display: flex;
            align-items: center;
            padding: 10px;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .task-option:hover {
            background: #bbdefb;
        }
        
        .task-option input {
            margin-right: 10px;
            cursor: pointer;
        }
        
        .rating-section {
            background: #fff3e0;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .rating-section h3 {
            color: #f57c00;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .rating-options {
            display: flex;
            gap: 15px;
        }
        
        .rating-btn {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .rating-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .rating-btn.correct {
            border-color: #4caf50;
        }
        
        .rating-btn.correct.selected {
            background: #4caf50;
            color: white;
        }
        
        .rating-btn.incorrect {
            border-color: #f44336;
        }
        
        .rating-btn.incorrect.selected {
            background: #f44336;
            color: white;
        }
        
        .rating-btn.partial {
            border-color: #ff9800;
        }
        
        .rating-btn.partial.selected {
            background: #ff9800;
            color: white;
        }
        
        .notes-section {
            margin-top: 15px;
        }
        
        .notes-section textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            min-height: 80px;
        }
        
        .notes-section textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        
        .btn {
            flex: 1;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        
        .btn-success {
            background: #4caf50;
            color: white;
        }
        
        .btn-success:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        .summary-panel {
            display: none;
            padding: 30px;
        }
        
        .summary-panel.active {
            display: block;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .completion-message {
            background: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .completion-message h2 {
            color: #2e7d32;
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .completion-message p {
            color: #558b2f;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 GPT-5 V2 Hero Prompts Evaluation</h1>
            <p>Human evaluation for gold standard reference creation</p>
            <div class="framework-badge">24 Canonical Tasks v2.0 Framework</div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-info">
                <span id="progress-text">Progress: 0 of 9 prompts evaluated</span>
                <span id="progress-percent">0%</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
        </div>
        
        <div class="content">
            <div class="prompt-selector" id="prompt-selector">
                <!-- Prompt buttons will be generated here -->
            </div>
            
            <div id="evaluation-panels">
                <!-- Evaluation panels will be generated here -->
            </div>
            
            <div class="summary-panel" id="summary-panel">
                <div class="completion-message">
                    <h2>🎉 V2 Evaluation Complete!</h2>
                    <p>All evaluations have been saved. You can review the summary below and download the gold standard reference.</p>
                </div>
                
                <div class="summary-stats" id="summary-stats">
                    <!-- Summary statistics will be shown here -->
                </div>
                
                <div class="action-buttons">
                    <button class="btn btn-primary" onclick="downloadResults()">💾 Download V2 Gold Standard JSON</button>
                    <button class="btn btn-secondary" onclick="showPrompts()">← Back to Prompts</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Data will be injected here
        const v2Data = """ + json.dumps(self.v2_results) + """;
        const canonicalTasks = """ + json.dumps(self.canonical_tasks) + """;
        const evaluationResults = {};
        
        // Initialize UI
        function init() {
            generatePromptButtons();
            generateEvaluationPanels();
            loadSavedResults();
            updateProgress();
        }
        
        function generatePromptButtons() {
            const container = document.getElementById('prompt-selector');
            v2Data.prompts.forEach((prompt, index) => {
                const btn = document.createElement('button');
                btn.className = 'prompt-btn';
                btn.id = `prompt-btn-${prompt.prompt_id}`;
                const taskCount = prompt.analysis?.tasks_covered?.length || 0;
                btn.innerHTML = `<strong>${prompt.prompt_id}</strong><br><small>${taskCount} tasks</small>`;
                btn.onclick = () => showPrompt(prompt.prompt_id);
                container.appendChild(btn);
            });
        }
        
        function generateEvaluationPanels() {
            const container = document.getElementById('evaluation-panels');
            
            v2Data.prompts.forEach(prompt => {
                const panel = document.createElement('div');
                panel.className = 'evaluation-panel';
                panel.id = `panel-${prompt.prompt_id}`;
                
                // Initialize evaluation data
                evaluationResults[prompt.prompt_id] = {
                    prompt_id: prompt.prompt_id,
                    prompt_text: prompt.prompt_text,
                    tasks_covered: [],
                    missing_tasks: [],
                    overall_rating: null,
                    notes: ''
                };
                
                // Build tasks in plan map
                const tasksInPlan = {};
                const tasksCovered = prompt.analysis?.tasks_covered || [];
                tasksCovered.forEach(taskId => {
                    tasksInPlan[taskId] = true;
                });
                
                const executionPlan = prompt.analysis?.execution_plan || [];
                
                panel.innerHTML = `
                    <div class="section">
                        <h2>Prompt: ${prompt.prompt_id}</h2>
                        <div class="prompt-text">${prompt.prompt_text}</div>
                    </div>
                    
                    <div class="section">
                        <h2>Execution Plan with Canonical Tasks Decomposition</h2>
                        <p style="color: #666; margin-bottom: 15px;">Review each step and verify the canonical task assignment is correct</p>
                        
                        <div class="execution-plan">
                            ${executionPlan.map(step => {
                                const task = canonicalTasks.find(t => t.id === step.task_id);
                                return `
                                    <div class="step-item" id="step-${prompt.prompt_id}-${step.step}">
                                        <div class="step-header">
                                            <div>
                                                <div class="step-number">Step ${step.step}</div>
                                                <div style="display: flex; align-items: center; gap: 10px; margin-top: 8px;">
                                                    <input type="checkbox" 
                                                           class="task-checkbox" 
                                                           id="task-${prompt.prompt_id}-${step.task_id}-step${step.step}"
                                                           checked
                                                           onchange="updateTaskCorrectness('${prompt.prompt_id}', '${step.task_id}', this.checked)">
                                                    <span class="task-id">${step.task_id}</span>
                                                    <span class="task-name">${step.task_name}</span>
                                                    ${task ? `<span class="tier-badge tier-${task.tier}">Tier ${task.tier}</span>` : ''}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="step-content">
                                            <div class="step-field">
                                                <span class="step-label">📋 Description:</span>
                                                <span class="step-value">${step.description || 'N/A'}</span>
                                            </div>
                                            ${step.input_schema ? `
                                            <div class="step-field" style="margin-top: 10px;">
                                                <span class="step-label">📥 Input Schema:</span>
                                                <code class="schema-code">${JSON.stringify(step.input_schema, null, 2)}</code>
                                            </div>
                                            ` : ''}
                                            ${step.output_schema ? `
                                            <div class="step-field" style="margin-top: 10px;">
                                                <span class="step-label">📤 Output Schema:</span>
                                                <code class="schema-code">${JSON.stringify(step.output_schema, null, 2)}</code>
                                            </div>
                                            ` : ''}
                                            ${step.note ? `
                                            <div class="step-field" style="margin-top: 10px;">
                                                <span class="step-label">💡 Note:</span>
                                                <span class="step-value" style="font-style: italic; color: #888;">${step.note}</span>
                                            </div>
                                            ` : ''}
                                            ${step.parallel_execution !== undefined ? `
                                            <div class="step-field" style="margin-top: 10px;">
                                                <span class="step-label">⚡ Parallel:</span>
                                                <span class="step-value">${step.parallel_execution ? 'Yes' : 'No'}</span>
                                            </div>
                                            ` : ''}
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                        
                        <div class="add-task-section">
                            <h3>➕ Add Missing Canonical Tasks</h3>
                            <p style="color: #666; font-size: 14px; margin-bottom: 15px;">If any canonical tasks are missing from GPT-5's analysis, add them here:</p>
                            <div class="task-selector">
                                ${canonicalTasks.filter(ct => !tasksInPlan[ct.id]).map(task => `
                                    <label class="task-option">
                                        <input type="checkbox" 
                                               onchange="addMissingTask('${prompt.prompt_id}', '${task.id}', this.checked)">
                                        <span><strong>${task.id}</strong> - ${task.name} <span class="tier-badge tier-${task.tier}">Tier ${task.tier}</span></span>
                                    </label>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div class="rating-section">
                            <h3>Overall Task Decomposition Rating</h3>
                            <p style="color: #666; font-size: 14px; margin-bottom: 15px;">Rate the overall quality of canonical tasks decomposition:</p>
                            <div class="rating-options">
                                <button class="rating-btn correct" 
                                        onclick="rateDecomposition('${prompt.prompt_id}', 'correct')">
                                    ✅ Correct - All necessary tasks identified accurately
                                </button>
                                <button class="rating-btn partial" 
                                        onclick="rateDecomposition('${prompt.prompt_id}', 'partial')">
                                    ⚠️ Partially Correct - Missing some tasks or includes unnecessary ones
                                </button>
                                <button class="rating-btn incorrect" 
                                        onclick="rateDecomposition('${prompt.prompt_id}', 'incorrect')">
                                    ❌ Incorrect - Major issues with task identification
                                </button>
                            </div>
                            
                            <div class="notes-section">
                                <textarea 
                                    id="notes-${prompt.prompt_id}"
                                    placeholder="Overall notes about task decomposition (explain issues, rationale for missing tasks)..."
                                    onchange="updateNotes('${prompt.prompt_id}', this.value)"></textarea>
                            </div>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-secondary" onclick="previousPrompt('${prompt.prompt_id}')">← Previous</button>
                        <button class="btn btn-primary" onclick="nextPrompt('${prompt.prompt_id}')">Next →</button>
                        <button class="btn btn-success" onclick="saveAndContinue('${prompt.prompt_id}')">💾 Save & Continue</button>
                    </div>
                `;
                
                container.appendChild(panel);
            });
        }
        
        function showPrompt(promptId) {
            // Hide all panels
            document.querySelectorAll('.evaluation-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.prompt-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('summary-panel').classList.remove('active');
            
            // Show selected panel
            document.getElementById(`panel-${promptId}`).classList.add('active');
            document.getElementById(`prompt-btn-${promptId}`).classList.add('active');
            
            // Scroll to top
            window.scrollTo(0, 0);
        }
        
        function showPrompts() {
            document.querySelectorAll('.evaluation-panel').forEach(p => p.classList.remove('active'));
            document.getElementById('summary-panel').classList.remove('active');
            window.scrollTo(0, 0);
        }
        
        function updateTaskCorrectness(promptId, taskId, isCorrect) {
            if (isCorrect) {
                if (!evaluationResults[promptId].tasks_covered.includes(taskId)) {
                    evaluationResults[promptId].tasks_covered.push(taskId);
                }
            } else {
                evaluationResults[promptId].tasks_covered = 
                    evaluationResults[promptId].tasks_covered.filter(t => t !== taskId);
            }
            autoSave();
        }
        
        function addMissingTask(promptId, taskId, isAdded) {
            if (isAdded) {
                if (!evaluationResults[promptId].missing_tasks.includes(taskId)) {
                    evaluationResults[promptId].missing_tasks.push(taskId);
                }
                if (!evaluationResults[promptId].tasks_covered.includes(taskId)) {
                    evaluationResults[promptId].tasks_covered.push(taskId);
                }
            } else {
                evaluationResults[promptId].missing_tasks = 
                    evaluationResults[promptId].missing_tasks.filter(t => t !== taskId);
                evaluationResults[promptId].tasks_covered = 
                    evaluationResults[promptId].tasks_covered.filter(t => t !== taskId);
            }
            autoSave();
        }
        
        function rateDecomposition(promptId, rating) {
            evaluationResults[promptId].overall_rating = rating;
            
            // Update button styles
            const panel = document.getElementById(`panel-${promptId}`);
            panel.querySelectorAll('.rating-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            panel.querySelector(`.rating-btn.${rating}`).classList.add('selected');
            
            autoSave();
        }
        
        function updateNotes(promptId, notes) {
            evaluationResults[promptId].notes = notes;
            autoSave();
        }
        
        function nextPrompt(currentId) {
            const prompts = v2Data.prompts.map(r => r.prompt_id);
            const currentIndex = prompts.indexOf(currentId);
            if (currentIndex < prompts.length - 1) {
                showPrompt(prompts[currentIndex + 1]);
            } else {
                showSummary();
            }
        }
        
        function previousPrompt(currentId) {
            const prompts = v2Data.prompts.map(r => r.prompt_id);
            const currentIndex = prompts.indexOf(currentId);
            if (currentIndex > 0) {
                showPrompt(prompts[currentIndex - 1]);
            }
        }
        
        function saveAndContinue(promptId) {
            // Mark as evaluated
            const btn = document.getElementById(`prompt-btn-${promptId}`);
            btn.classList.add('evaluated');
            
            // Update progress
            updateProgress();
            
            // Move to next
            nextPrompt(promptId);
        }
        
        function updateProgress() {
            const total = v2Data.prompts.length;
            const evaluated = document.querySelectorAll('.prompt-btn.evaluated').length;
            const percent = Math.round((evaluated / total) * 100);
            
            document.getElementById('progress-text').textContent = `Progress: ${evaluated} of ${total} prompts evaluated`;
            document.getElementById('progress-percent').textContent = `${percent}%`;
            document.getElementById('progress-fill').style.width = `${percent}%`;
        }
        
        function showSummary() {
            // Hide all panels
            document.querySelectorAll('.evaluation-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.prompt-btn').forEach(b => b.classList.remove('active'));
            
            // Generate summary stats
            let totalTasks = 0;
            let correctTasks = 0;
            let missingTasks = 0;
            let correctRatings = 0;
            let partialRatings = 0;
            let incorrectRatings = 0;
            
            Object.values(evaluationResults).forEach(result => {
                const original = v2Data.prompts.find(p => p.prompt_id === result.prompt_id);
                const originalTasks = original?.analysis?.tasks_covered || [];
                
                totalTasks += originalTasks.length;
                correctTasks += result.tasks_covered.length;
                missingTasks += result.missing_tasks.length;
                
                if (result.overall_rating === 'correct') correctRatings++;
                else if (result.overall_rating === 'partial') partialRatings++;
                else if (result.overall_rating === 'incorrect') incorrectRatings++;
            });
            
            const statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${correctTasks}</div>
                    <div class="stat-label">Total Validated Tasks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${missingTasks}</div>
                    <div class="stat-label">Tasks Added by Human</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${correctRatings}</div>
                    <div class="stat-label">Correct Decompositions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${partialRatings}</div>
                    <div class="stat-label">Partially Correct</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${incorrectRatings}</div>
                    <div class="stat-label">Incorrect</div>
                </div>
            `;
            
            document.getElementById('summary-stats').innerHTML = statsHtml;
            document.getElementById('summary-panel').classList.add('active');
            
            // Auto-save final results
            autoSave();
            window.scrollTo(0, 0);
        }
        
        function autoSave() {
            localStorage.setItem('v2_evaluation_results', JSON.stringify(evaluationResults));
        }
        
        function loadSavedResults() {
            const saved = localStorage.getItem('v2_evaluation_results');
            if (saved) {
                const savedData = JSON.parse(saved);
                Object.assign(evaluationResults, savedData);
                
                // Restore UI state
                Object.keys(savedData).forEach(promptId => {
                    const result = savedData[promptId];
                    
                    // Restore checkboxes
                    result.tasks_covered.forEach(taskId => {
                        const checkbox = document.getElementById(`task-${promptId}-${taskId}`);
                        if (checkbox) checkbox.checked = true;
                    });
                    
                    // Restore rating
                    if (result.overall_rating) {
                        const panel = document.getElementById(`panel-${promptId}`);
                        if (panel) {
                            const btn = panel.querySelector(`.rating-btn.${result.overall_rating}`);
                            if (btn) btn.classList.add('selected');
                        }
                    }
                    
                    // Restore notes
                    const notesField = document.getElementById(`notes-${promptId}`);
                    if (notesField && result.notes) {
                        notesField.value = result.notes;
                    }
                });
            } else {
                // Initialize with GPT-5's results
                v2Data.prompts.forEach(prompt => {
                    evaluationResults[prompt.prompt_id].tasks_covered = 
                        [...(prompt.analysis?.tasks_covered || [])];
                });
            }
        }
        
        function downloadResults() {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            const filename = `v2_gold_standard_${timestamp}.json`;
            
            const data = {
                metadata: {
                    timestamp: timestamp,
                    framework_version: '24 Canonical Tasks v2.0',
                    total_prompts: v2Data.prompts.length,
                    evaluator: 'Chin-Yew Lin',
                    source_file: 'gpt5_v2_analysis_20251107_125720.json',
                    description: 'Human-validated gold standard for v2 hero prompts'
                },
                prompts: evaluationResults
            };
            
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
            
            // Also send to server
            fetch('/save_results', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    alert('✓ V2 Gold Standard saved successfully!');
                }
            });
        }
        
        // Initialize on load
        init();
        
        // Show first prompt by default
        if (v2Data.prompts.length > 0) {
            showPrompt(v2Data.prompts[0].prompt_id);
        }
    </script>
</body>
</html>"""
        
        return html
    
    def save_results(self, results_data: Dict):
        """Save v2 evaluation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.project_root / f"docs/gutt_analysis/v2_gold_standard_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVED] V2 gold standard to {output_file}")
        return output_file
    
    def start_server(self):
        """Start HTTP server for v2 evaluation UI"""
        
        class V2EvalHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, server_instance=None, **kwargs):
                self.server_instance = server_instance
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/' or self.path == '/evaluate':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    html = self.server_instance.generate_html()
                    self.wfile.write(html.encode('utf-8'))
                else:
                    super().do_GET()
            
            def do_POST(self):
                if self.path == '/save_results':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    results = json.loads(post_data.decode('utf-8'))
                    
                    output_file = self.server_instance.save_results(results)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'status': 'success', 'file': str(output_file)}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # Suppress logging
                pass
        
        handler = lambda *args, **kwargs: V2EvalHandler(*args, server_instance=self, **kwargs)
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            url = f"http://localhost:{self.port}/"
            print(f"\n{'='*80}")
            print(f"V2 HERO PROMPTS EVALUATION SERVER STARTED")
            print(f"{'='*80}")
            print(f"\n📊 Framework: 24 Canonical Tasks v2.0")
            print(f"📁 Source: gpt5_v2_analysis_20251107_125720.json")
            print(f"🎯 Prompts: 9 v2 hero prompts")
            print(f"\nURL: {url}")
            print(f"\nOpening browser...")
            print(f"\nPress Ctrl+C to stop the server when done.\n")
            
            # Open browser
            threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n\n{'='*80}")
                print(f"V2 EVALUATION SERVER STOPPED")
                print(f"{'='*80}")
                print(f"\n✅ V2 Gold Standard saved to: docs/gutt_analysis/v2_gold_standard_*.json")
                print(f"📝 Progress auto-saved to browser localStorage")
                print(f"🔄 You can restart evaluation anytime - all progress is preserved!\n")


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("GPT-5 V2 HERO PROMPTS HUMAN EVALUATION TOOL")
    print("24 Canonical Tasks Framework v2.0")
    print("="*80 + "\n")
    
    server = V2EvaluationServer()
    server.start_server()


if __name__ == "__main__":
    main()
