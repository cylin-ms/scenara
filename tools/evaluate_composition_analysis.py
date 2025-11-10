#!/usr/bin/env python3
"""
Interactive UX for Evaluating GPT-5 Canonical Tasks Analysis and Execution Plans
Allows reviewing decomposition accuracy and execution plan correctness
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

class EvaluationServer:
    """Web server for evaluation UX"""
    
    def __init__(self):
        self.project_root = project_root
        self.composition_results = self._load_composition_results()
        self.canonical_tasks = self._load_canonical_tasks()
        self.evaluation_results = {}
        self.port = 8080
        
    def _load_composition_results(self) -> Dict:
        """Load GPT-5 composition analysis results"""
        results_file = self.project_root / "docs/gutt_analysis/gpt5_composition_analysis_20251106_232748.json"
        print(f"[LOADING] Composition analysis from {results_file.name}")
        
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[OK] Loaded {len(data['results'])} prompt analyses")
        return data
    
    def _load_canonical_tasks(self) -> List[Dict]:
        """Load all 20 canonical tasks for selection"""
        # Define all 20 canonical tasks
        tasks = [
            {"id": "CAN-01", "name": "Calendar Events Retrieval", "tier": 1},
            {"id": "CAN-02", "name": "Meeting Classification", "tier": 1},
            {"id": "CAN-03", "name": "Calendar Event Creation/Update", "tier": 1},
            {"id": "CAN-04", "name": "Natural Language Understanding (Constraint/Intent Extraction)", "tier": 1},
            {"id": "CAN-05", "name": "Attendee/Contact Resolution", "tier": 1},
            {"id": "CAN-06", "name": "Availability Checking (Free/Busy)", "tier": 2},
            {"id": "CAN-07", "name": "Meeting Metadata Extraction", "tier": 2},
            {"id": "CAN-08", "name": "Document/Content Retrieval", "tier": 2},
            {"id": "CAN-09", "name": "Document Generation/Formatting", "tier": 2},
            {"id": "CAN-10", "name": "Time Aggregation/Statistical Analysis", "tier": 2},
            {"id": "CAN-11", "name": "Priority/Preference Matching", "tier": 2},
            {"id": "CAN-12", "name": "Constraint Satisfaction", "tier": 2},
            {"id": "CAN-13", "name": "RSVP Status Update", "tier": 2},
            {"id": "CAN-14", "name": "Recommendation Engine", "tier": 2},
            {"id": "CAN-15", "name": "Recurrence Rule Generation", "tier": 3},
            {"id": "CAN-16", "name": "Event Monitoring/Change Detection", "tier": 3},
            {"id": "CAN-17", "name": "Automatic Rescheduling", "tier": 3},
            {"id": "CAN-18", "name": "Objection/Risk Anticipation", "tier": 3},
            {"id": "CAN-19", "name": "Resource Booking (Rooms/Equipment)", "tier": 3},
            {"id": "CAN-20", "name": "Data Visualization/Reporting", "tier": 3},
        ]
        return tasks
    
    def generate_html(self) -> str:
        """Generate HTML for evaluation interface"""
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT-5 Canonical Tasks & Execution Plan Evaluation</title>
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
        
        .task-details {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 10px;
            padding-left: 39px;
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
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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
        
        .step-task {
            font-size: 14px;
            color: #666;
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
            min-width: 120px;
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
        
        .step-notes {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        
        .step-notes textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-family: inherit;
            font-size: 13px;
            resize: vertical;
            min-height: 60px;
        }
        
        .step-notes textarea:focus {
            outline: none;
            border-color: #667eea;
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
            <h1>📊 GPT-5 Canonical Tasks & Execution Plan Evaluation</h1>
            <p>Review decomposition accuracy and execution plan correctness for all 9 hero prompts</p>
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
                    <h2>🎉 Evaluation Complete!</h2>
                    <p>All evaluations have been saved. You can review the summary below.</p>
                </div>
                
                <div class="summary-stats" id="summary-stats">
                    <!-- Summary statistics will be shown here -->
                </div>
                
                <div class="action-buttons">
                    <button class="btn btn-primary" onclick="downloadResults()">💾 Download Results JSON</button>
                    <button class="btn btn-secondary" onclick="showPrompts()">← Back to Prompts</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Data will be injected here
        const compositionData = """ + json.dumps(self.composition_results) + """;
        const canonicalTasks = """ + json.dumps(self.canonical_tasks) + """;
        const evaluationResults = {};
        
        // Initialize UI
        function init() {
            generatePromptButtons();
            generateEvaluationPanels();
            updateProgress();
        }
        
        function generatePromptButtons() {
            const container = document.getElementById('prompt-selector');
            compositionData.results.forEach((result, index) => {
                const btn = document.createElement('button');
                btn.className = 'prompt-btn';
                btn.id = `prompt-btn-${result.prompt_id}`;
                btn.innerHTML = `<strong>${result.prompt_id}</strong><br><small>${result.execution_plan?.length || 0} steps</small>`;
                btn.onclick = () => showPrompt(result.prompt_id);
                container.appendChild(btn);
            });
        }
        
        function generateEvaluationPanels() {
            const container = document.getElementById('evaluation-panels');
            
            compositionData.results.forEach(result => {
                const panel = document.createElement('div');
                panel.className = 'evaluation-panel';
                panel.id = `panel-${result.prompt_id}`;
                
                // Initialize evaluation data
                evaluationResults[result.prompt_id] = {
                    prompt_id: result.prompt_id,
                    prompt_text: result.prompt_text,
                    steps: {},
                    missing_tasks: [],
                    execution_plan_rating: null,
                    overall_notes: ''
                };
                
                // Build tasks in plan map for filtering
                const tasksInPlan = {};
                
                // Initialize step evaluations
                if (result.execution_plan) {
                    result.execution_plan.forEach(step => {
                        evaluationResults[result.prompt_id].steps[step.step] = {
                            step_number: step.step,
                            task_id: step.task_id,
                            task_name: step.task_name,
                            tier: step.tier,
                            is_correct: true,
                            notes: ''
                        };
                        
                        // Track which tasks are already in the plan
                        tasksInPlan[step.task_id] = true;
                    });
                }
                
                panel.innerHTML = `
                    <div class="section">
                        <h2>Prompt: ${result.prompt_id}</h2>
                        <div class="prompt-text">${result.prompt_text}</div>
                    </div>
                    
                    <div class="section">
                        <h2>Execution Plan with Canonical Tasks</h2>
                        <p style="color: #666; margin-bottom: 15px;">Review each step: ✓ Check if task, input, processing, and output are correct</p>
                        
                        <div class="execution-plan">
                            ${(result.execution_plan || []).map(step => `
                                <div class="step-item" id="step-${result.prompt_id}-${step.step}">
                                    <div class="step-header">
                                        <div>
                                            <div class="step-number">Step ${step.step}</div>
                                            <div style="display: flex; align-items: center; gap: 10px; margin-top: 8px;">
                                                <input type="checkbox" 
                                                       class="task-checkbox" 
                                                       id="task-${result.prompt_id}-${step.task_id}-step${step.step}"
                                                       checked
                                                       onchange="updateStepCorrectness('${result.prompt_id}', ${step.step}, '${step.task_id}', this.checked)">
                                                <span class="task-id">${step.task_id}</span>
                                                <span class="task-name">${step.task_name}</span>
                                                <span class="tier-badge tier-${step.tier}">Tier ${step.tier}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="step-content">
                                        <div class="step-field">
                                            <span class="step-label">📥 Input:</span>
                                            <span class="step-value">${step.input?.description || 'N/A'}</span>
                                        </div>
                                        <div class="step-field">
                                            <span class="step-label">⚙️ Processing:</span>
                                            <span class="step-value">${step.processing || 'N/A'}</span>
                                        </div>
                                        <div class="step-field">
                                            <span class="step-label">📤 Output:</span>
                                            <span class="step-value">${step.output?.description || 'N/A'}</span>
                                        </div>
                                        <div class="step-field">
                                            <span class="step-label">➡️ Flows to:</span>
                                            <span class="step-value">${step.flows_to?.join(', ') || 'Final Output'}</span>
                                        </div>
                                        ${step.input?.schema ? `
                                        <div class="step-field" style="margin-top: 10px;">
                                            <span class="step-label">Input Schema:</span>
                                            <code class="schema-code">${JSON.stringify(step.input.schema, null, 2)}</code>
                                        </div>
                                        ` : ''}
                                        ${step.output?.schema ? `
                                        <div class="step-field" style="margin-top: 10px;">
                                            <span class="step-label">Output Schema:</span>
                                            <code class="schema-code">${JSON.stringify(step.output.schema, null, 2)}</code>
                                        </div>
                                        ` : ''}
                                    </div>
                                    <div class="step-notes">
                                        <textarea 
                                            id="step-notes-${result.prompt_id}-${step.step}"
                                            placeholder="Notes about this step (optional)..."
                                            onchange="updateStepNotes('${result.prompt_id}', ${step.step}, this.value)"></textarea>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div class="add-task-section" style="margin-top: 20px;">
                            <h3>➕ Add Missing Steps/Tasks</h3>
                            <p style="color: #666; font-size: 14px; margin-bottom: 15px;">If any canonical tasks are missing from the execution plan, add them here:</p>
                            <div class="task-selector">
                                ${canonicalTasks.filter(ct => !tasksInPlan[ct.id]).map(task => `
                                    <label class="task-option">
                                        <input type="checkbox" 
                                               onchange="addMissingTask('${result.prompt_id}', '${task.id}', this.checked)">
                                        <span><strong>${task.id}</strong> - ${task.name} <span class="tier-badge tier-${task.tier}" style="margin-left: 5px;">Tier ${task.tier}</span></span>
                                    </label>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div class="rating-section">
                            <h3>Overall Execution Plan Rating</h3>
                            <p style="color: #666; font-size: 14px; margin-bottom: 15px;">If all steps are correct, the plan is correct. Rate based on the overall computational workflow:</p>
                            <div class="rating-options">
                                <button class="rating-btn correct" 
                                        onclick="rateExecutionPlan('${result.prompt_id}', 'correct')">
                                    ✅ Correct - All tasks, data flow, and logic are accurate
                                </button>
                                <button class="rating-btn partial" 
                                        onclick="rateExecutionPlan('${result.prompt_id}', 'partial')">
                                    ⚠️ Partially Correct - Some steps need adjustment
                                </button>
                                <button class="rating-btn incorrect" 
                                        onclick="rateExecutionPlan('${result.prompt_id}', 'incorrect')">
                                    ❌ Incorrect - Major issues with workflow design
                                </button>
                            </div>
                            
                            <div class="notes-section">
                                <textarea 
                                    id="notes-${result.prompt_id}"
                                    placeholder="Overall notes about the execution plan (summarize issues, suggest improvements)..."
                                    onchange="updateNotes('${result.prompt_id}', this.value)"></textarea>
                            </div>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-secondary" onclick="previousPrompt('${result.prompt_id}')">← Previous</button>
                        <button class="btn btn-primary" onclick="nextPrompt('${result.prompt_id}')">Next →</button>
                        <button class="btn btn-success" onclick="saveAndContinue('${result.prompt_id}')">💾 Save & Continue</button>
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
        
        function updateStepCorrectness(promptId, stepNumber, taskId, isCorrect) {
            evaluationResults[promptId].steps[stepNumber].is_correct = isCorrect;
            
            // Visual feedback
            const stepElement = document.getElementById(`step-${promptId}-${stepNumber}`);
            if (!isCorrect) {
                stepElement.classList.add('incorrect');
            } else {
                stepElement.classList.remove('incorrect');
            }
            
            autoSave();
        }
        
        function updateStepNotes(promptId, stepNumber, notes) {
            evaluationResults[promptId].steps[stepNumber].notes = notes;
            autoSave();
        }
        
        function addMissingTask(promptId, taskId, isAdded) {
            if (isAdded) {
                if (!evaluationResults[promptId].missing_tasks.includes(taskId)) {
                    evaluationResults[promptId].missing_tasks.push(taskId);
                }
            } else {
                evaluationResults[promptId].missing_tasks = 
                    evaluationResults[promptId].missing_tasks.filter(t => t !== taskId);
            }
            autoSave();
        }
        
        function rateExecutionPlan(promptId, rating) {
            evaluationResults[promptId].execution_plan_rating = rating;
            
            // Update button styles
            const panel = document.getElementById(`panel-${promptId}`);
            panel.querySelectorAll('.rating-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            panel.querySelector(`.rating-btn.${rating}`).classList.add('selected');
            
            autoSave();
        }
        
        function updateNotes(promptId, notes) {
            evaluationResults[promptId].overall_notes = notes;
            autoSave();
        }
        
        function nextPrompt(currentId) {
            const prompts = compositionData.results.map(r => r.prompt_id);
            const currentIndex = prompts.indexOf(currentId);
            if (currentIndex < prompts.length - 1) {
                showPrompt(prompts[currentIndex + 1]);
            } else {
                showSummary();
            }
        }
        
        function previousPrompt(currentId) {
            const prompts = compositionData.results.map(r => r.prompt_id);
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
            const total = compositionData.results.length;
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
            let totalSteps = 0;
            let correctSteps = 0;
            let missingTasks = 0;
            let correctPlans = 0;
            let partialPlans = 0;
            let incorrectPlans = 0;
            
            Object.values(evaluationResults).forEach(result => {
                // Count steps
                Object.values(result.steps || {}).forEach(step => {
                    totalSteps++;
                    if (step.is_correct) correctSteps++;
                });
                
                // Count missing tasks
                missingTasks += (result.missing_tasks || []).length;
                
                // Count plan ratings
                if (result.execution_plan_rating === 'correct') correctPlans++;
                else if (result.execution_plan_rating === 'partial') partialPlans++;
                else if (result.execution_plan_rating === 'incorrect') incorrectPlans++;
            });
            
            const stepAccuracy = totalSteps > 0 ? Math.round((correctSteps / totalSteps) * 100) : 0;
            
            const statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${stepAccuracy}%</div>
                    <div class="stat-label">Step Accuracy (${correctSteps}/${totalSteps})</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${missingTasks}</div>
                    <div class="stat-label">Missing Tasks Identified</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${correctPlans}</div>
                    <div class="stat-label">Correct Execution Plans</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${partialPlans}</div>
                    <div class="stat-label">Partially Correct Plans</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${incorrectPlans}</div>
                    <div class="stat-label">Incorrect Plans</div>
                </div>
            `;
            
            document.getElementById('summary-stats').innerHTML = statsHtml;
            document.getElementById('summary-panel').classList.add('active');
            
            // Auto-save final results
            autoSave();
            window.scrollTo(0, 0);
        }
        
        function autoSave() {
            localStorage.setItem('evaluation_results', JSON.stringify(evaluationResults));
        }
        
        function downloadResults() {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            const filename = `evaluation_results_${timestamp}.json`;
            
            const data = {
                metadata: {
                    timestamp: timestamp,
                    total_prompts: compositionData.results.length,
                    evaluator: 'Chin-Yew Lin',
                    source_file: 'gpt5_composition_analysis_20251106_232748.json'
                },
                evaluations: evaluationResults
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
                    alert('✓ Results saved successfully!');
                }
            });
        }
        
        // Load saved results if available
        const saved = localStorage.getItem('evaluation_results');
        if (saved) {
            Object.assign(evaluationResults, JSON.parse(saved));
        }
        
        // Initialize on load
        init();
        
        // Show first prompt by default
        if (compositionData.results.length > 0) {
            showPrompt(compositionData.results[0].prompt_id);
        }
    </script>
</body>
</html>"""
        
        return html
    
    def save_results(self, results_data: Dict):
        """Save evaluation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.project_root / f"docs/gutt_analysis/evaluation_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVED] Evaluation results to {output_file}")
        return output_file
    
    def start_server(self):
        """Start HTTP server for evaluation UI"""
        
        class EvalHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, server_instance=None, **kwargs):
                self.server_instance = server_instance
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/' or self.path == '/evaluate':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = self.server_instance.generate_html()
                    self.wfile.write(html.encode())
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
        
        handler = lambda *args, **kwargs: EvalHandler(*args, server_instance=self, **kwargs)
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            url = f"http://localhost:{self.port}/"
            print(f"\n{'='*80}")
            print(f"EVALUATION SERVER STARTED")
            print(f"{'='*80}")
            print(f"\nURL: {url}")
            print(f"\nOpening browser...")
            print(f"\nPress Ctrl+C to stop the server when done.\n")
            
            # Open browser
            threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n\n{'='*80}")
                print(f"SERVER STOPPED")
                print(f"{'='*80}")
                print(f"\nResults saved to: docs/gutt_analysis/evaluation_results_*.json")
                print(f"You can restart evaluation anytime - progress is saved automatically!\n")


def main():
    """Main execution"""
    server = EvaluationServer()
    server.start_server()


if __name__ == "__main__":
    main()
