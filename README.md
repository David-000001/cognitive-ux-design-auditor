# Cognitive UX Design Auditor Demo

This is a Week 13-ready prototype demo for WID2001 Knowledge Representation & Reasoning.

## Project Title

Cognitive UX Design Auditor  
A rule-based expert system for auditing cognitive usability issues in user interface design.

## What the demo does

The system asks audit questions about a UI screen and applies IF-THEN rules to detect cognitive UX problems.

It can detect:

- Cognitive load issues
- Poor visual hierarchy
- Label inconsistency
- Recognition vs recall problems
- Weak error prevention
- Poor feedback and recovery
- Navigation clarity problems
- Readability and contrast issues

## Expert system components

| Component | Implementation |
|---|---|
| Knowledge Base | `rules.json` stores IF-THEN rules |
| Inference Engine | `run_forward_chaining()` in `app.py` |
| User Interface | Streamlit questionnaire |
| Explanation Facility | Shows triggered rules, explanation, severity, and recommendation |

## How to run in VS Code

### Step 1: Open the folder

Open this folder in VS Code:

```bash
cognitive_ux_design_auditor_demo
```

### Step 2: Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install requirements

```bash
pip install -r requirements.txt
```

### Step 4: Run the app

```bash
streamlit run app.py
```

### Step 5: Use the demo

1. Choose a sample scenario from the sidebar.
2. Review or modify the questionnaire answers.
3. Click **Run UX Audit**.
4. Show the output: overall risk, severity score, rules fired, triggered issues, explanations, and recommendations.
5. Download the JSON report if needed.

## Recommended scenario for demo

Use **Overloaded dashboard** from the sidebar.

Expected output:

- High Cognitive Load
- Poor Visual Hierarchy
- Label Inconsistency
- Unclear Navigation
- No Current Location Indicator
- Crowded Layout

This looks strong in a 3-4 minute recorded demo because multiple rules fire clearly.
