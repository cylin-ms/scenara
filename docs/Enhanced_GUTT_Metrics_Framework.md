# Enhanced GUTT Metrics Framework: Precision-Based Evaluation System

**Advanced Metrics for Meeting Intelligence System Evaluation**

*Framework Version: 2.0*  
*Contact: Chin-Yew Lin*  
*Date: September 29, 2025*  
*Enhancement: Dual-Track Trigger and Quality Metrics*

---

## Overview: Dual-Track GUTT Metrics System

This enhanced framework introduces **two independent measurement tracks** for comprehensive system evaluation:

### **Track 1: GUTT Trigger Metrics**
- **GUTT_Trigger_Precision**: Accuracy of task activation decisions
- **GUTT_Trigger_Recall**: Coverage of required task activation  
- **GUTT_Trigger_F1**: Balanced measure of trigger performance

### **Track 2: GUTT Quality Metrics**
- **Individual GUTT Rubric Scores**: 1-4 point quality assessment per triggered task
- **GUTT_Rubric_Aggregate**: Mean quality score across all triggered GUTTs
- **Weighted Quality Metrics**: Priority-adjusted quality measurements

---

## Track 1: GUTT Trigger Metrics

### **GUTT_Trigger_Precision Formula**
```
GUTT_Trigger_Precision = Correctly_Triggered_Tasks / Total_Triggered_Tasks

Where:
- Correctly_Triggered_Tasks = Tasks that should have been triggered AND were triggered
- Total_Triggered_Tasks = All tasks the system actually triggered
```

**Interpretation**: 
- **1.0 (100%)**: Perfect - No false positive task triggers
- **0.8-0.99**: Excellent - Minimal inappropriate task activation
- **0.6-0.79**: Good - Some unnecessary task triggers
- **0.4-0.59**: Poor - Many inappropriate task activations
- **<0.4**: Critical - More wrong triggers than correct ones

### **GUTT_Trigger_Recall Formula**
```
GUTT_Trigger_Recall = Correctly_Triggered_Tasks / Expected_Tasks

Where:
- Correctly_Triggered_Tasks = Tasks that should have been triggered AND were triggered  
- Expected_Tasks = All tasks that should have been triggered based on user query
```

**Interpretation**:
- **1.0 (100%)**: Perfect - All required tasks triggered
- **0.8-0.99**: Excellent - Minimal missing task triggers
- **0.6-0.79**: Good - Some required tasks missed
- **0.4-0.59**: Poor - Many required tasks not triggered
- **<0.4**: Critical - Most required functionality missing

### **GUTT_Trigger_F1 Formula**
```
GUTT_Trigger_F1 = 2 × (GUTT_Trigger_Precision × GUTT_Trigger_Recall) / (GUTT_Trigger_Precision + GUTT_Trigger_Recall)
```

**Interpretation**:
- **0.9-1.0**: Exceptional trigger performance
- **0.8-0.89**: Excellent trigger performance
- **0.7-0.79**: Good trigger performance
- **0.6-0.69**: Acceptable trigger performance
- **<0.6**: Inadequate trigger performance

---

## Track 2: Individual GUTT Rubric Scoring

### **4-Level Quality Rubric (Per GUTT)**

#### **Level 1: Critical Failure (1.0 points)**
- Task triggered but completely failed execution
- Factually incorrect information provided
- System error or malfunction during task execution
- **Example**: GUTT.17 triggered but retrieves wrong meeting entirely

#### **Level 2: Basic Attempt (2.0 points)**  
- Task executed with significant limitations or gaps
- Partially correct information with notable omissions
- Functional but requires substantial user correction
- **Example**: GUTT.20 provides generic meeting summary without specific goals

#### **Level 3: Functional Success (3.0 points)**
- Task successfully executed with minor limitations
- Accurate and relevant information with good context
- User can proceed with minimal additional work
- **Example**: GUTT.14 correctly identifies stakeholders with basic context

#### **Level 4: Excellence (4.0 points)**
- Task expertly executed, exceeding basic requirements
- Comprehensive, accurate, well-formatted, actionable output  
- Adds significant user value beyond core requirement
- **Example**: GUTT.17 provides meeting content plus related documents and insights

### **Individual GUTT Quality Score Formula**
```
GUTT_X_Quality = Rubric_Score_for_GUTT_X (1.0 to 4.0)
```

---

## GUTT_Rubric_Aggregate Calculation

### **Simple Average Method**
```
GUTT_Rubric_Aggregate = Σ(Individual_GUTT_Quality_Scores) / Number_of_Triggered_GUTTs

Example:
- GUTT.14 Quality: 3.0
- GUTT.17 Quality: 2.0  
- GUTT.20 Quality: 4.0
- GUTT_Rubric_Aggregate = (3.0 + 2.0 + 4.0) / 3 = 3.0
```

### **Weighted Average Method (Optional)**
```
GUTT_Rubric_Aggregate_Weighted = Σ(Individual_GUTT_Quality × GUTT_Weight) / Σ(GUTT_Weights)

Where GUTT_Weight reflects business priority:
- Core Meeting Intelligence GUTTs: Weight = 1.0
- Supporting Task GUTTs: Weight = 0.8  
- Advanced Enterprise GUTTs: Weight = 1.2
- Communication GUTTs: Weight = 0.9
- Specialized Function GUTTs: Weight = 0.7
```

---

## Complete GUTT Metrics Dashboard

### **Example Evaluation Output**

```yaml
System_Evaluation:
  Query: "what are the goals we aim to achieve by the end of this Bi-weekly 1:1 Chin-Yew | Dongmei"
  
  Trigger_Metrics:
    Expected_Tasks: ["GUTT.14", "GUTT.17", "GUTT.20"]
    Triggered_Tasks: ["GUTT.14", "GUTT.17"]
    Correctly_Triggered: ["GUTT.14", "GUTT.17"]
    
    GUTT_Trigger_Precision: 1.00  # 2/2 correct triggers
    GUTT_Trigger_Recall: 0.67     # 2/3 expected tasks
    GUTT_Trigger_F1: 0.80         # F1 score
    
  Quality_Metrics:
    GUTT_14_Quality: 4.0  # Excellent stakeholder identification
    GUTT_17_Quality: 3.0  # Good meeting content retrieval
    GUTT_20_Quality: 0.0  # Not triggered (no quality score)
    
    Triggered_GUTT_Count: 2
    GUTT_Rubric_Aggregate: 3.5    # (4.0 + 3.0) / 2
    
  Performance_Band: "Good Performance"
  Primary_Issues: ["Missing goal summarization (GUTT.20)"]
```

---

## GUTT-Specific Weight Classifications

### **Core Meeting Intelligence (Weight: 1.0)**
1. **GUTT.14**: Identify [project/team/person] from context
2. **GUTT.17**: Find content of [artifact] for [event]  
3. **GUTT.20**: Summarize [meeting objectives] into [specific goals]
4. **GUTT.12**: Extract [key information] from [data source]
5. **GUTT.05**: Analyze [data/content] to identify [patterns/insights]

### **Advanced Enterprise (Weight: 1.2)**
6. **GUTT.11**: Research [topic] across [multiple sources/domains]
7. **GUTT.15**: Validate [information] against [standards/requirements]
8. **GUTT.23**: Integrate [system A] data with [system B] for [outcome]
9. **GUTT.21**: Monitor [metrics/indicators] and alert on [conditions]
10. **GUTT.24**: Optimize [process/resource] for [objective/constraint]

### **Communication & Collaboration (Weight: 0.9)**
11. **GUTT.02**: Communicate [message] to [audience] via [channel]
12. **GUTT.06**: Facilitate [interaction] between [parties] for [goal]
13. **GUTT.13**: Distribute [content] to [stakeholders] based on [criteria]
14. **GUTT.16**: Collect [feedback/input] from [sources] about [topic]
15. **GUTT.19**: Negotiate [agreement] between [parties] on [issues]

### **Supporting Tasks (Weight: 0.8)**
16. **GUTT.01**: Compare [item A] with [item B] for [criteria]
17. **GUTT.03**: Generate [content type] about [topic] for [context]
18. **GUTT.07**: Provide recommendations for [situation] based on [criteria]
19. **GUTT.08**: Create [document] for [purpose/audience]
20. **GUTT.09**: Schedule/coordinate [activity] with [constraints]

### **Specialized Functions (Weight: 0.7)**
21. **GUTT.04**: Calculate [metrics] from [data] for [decision]
22. **GUTT.10**: Troubleshoot [problem] in [system/process]
23. **GUTT.18**: Transform [input format] to [output format] for [purpose]
24. **GUTT.22**: Predict [outcome] based on [historical data/trends]
25. **GUTT.25**: Audit [system/process] against [compliance/standards]

---

## Composite Scoring Framework

### **Overall System Score Options**

#### **Option 1: Balanced Approach**
```
Overall_GUTT_Score = (GUTT_Trigger_F1 × 0.4) + (GUTT_Rubric_Aggregate/4 × 0.6)
```

#### **Option 2: Quality-Focused Approach**
```
Overall_GUTT_Score = (GUTT_Trigger_F1 × 0.3) + (GUTT_Rubric_Aggregate/4 × 0.7)
```

#### **Option 3: Trigger-Focused Approach**  
```
Overall_GUTT_Score = (GUTT_Trigger_F1 × 0.6) + (GUTT_Rubric_Aggregate/4 × 0.4)
```

### **Performance Bands (Based on Overall Score)**
- **90-100%**: Exceptional Performance
- **80-89%**: Excellent Performance  
- **70-79%**: Good Performance
- **60-69%**: Acceptable Performance
- **50-59%**: Poor Performance
- **Below 50%**: Critical Failure

---

## Implementation Guidelines

### **Step 1: Task Expectation Analysis**
1. Parse user query to identify required GUTT tasks
2. Consider enterprise meeting type and context
3. Create expected task list with rationale

### **Step 2: Trigger Assessment**  
1. Analyze system processing pipeline
2. Identify which GUTTs were actually triggered
3. Calculate precision, recall, and F1 metrics

### **Step 3: Quality Evaluation**
1. Apply 4-level rubric to each triggered GUTT
2. Document evidence for each quality score
3. Calculate individual and aggregate quality metrics

### **Step 4: Composite Scoring**
1. Choose appropriate weighting approach
2. Calculate overall system performance score
3. Assign performance band and recommendations

### **Step 5: Reporting**
1. Generate comprehensive metrics dashboard
2. Provide specific improvement recommendations
3. Highlight top performing and failing GUTTs

---

## Advantages of Enhanced Framework

### **Granular Analysis**
- **Separate trigger and quality assessment** prevents conflation of different failure modes
- **Individual GUTT scoring** enables precise identification of system strengths/weaknesses
- **Weighted metrics** allow business priority alignment

### **Actionable Insights**  
- **Trigger metrics** guide task detection improvements
- **Quality scores** focus response generation enhancements
- **F1 score** provides balanced trigger performance view

### **Business Alignment**
- **Weight classifications** reflect enterprise priorities
- **Performance bands** enable deployment decisions
- **Composite scoring** supports ROI calculations

This enhanced framework provides the precision and granularity needed for enterprise-grade AI system evaluation while maintaining clear actionability for system improvement initiatives.