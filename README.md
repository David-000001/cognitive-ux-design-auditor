# Cognitive UX Design Auditor - Fixed Expert System Version

## Project title

**Cognitive UX Design Auditor**  
An explainable rule-based expert system for auditing cognitive usability issues in user interface design.


1. Expert System Architecture tab
2. Run UX Audit tab
3. Forward Chaining Reasoning Trace tab
4. Knowledge Base tab
5. Testing Evidence tab
6. Visible fact base table
7. Rule-by-rule fired/not-fired trace
8. Full JSON report with reasoning trace

## Expert system components

| Component | Implementation |
|---|---|
| Domain expertise | Cognitive UX / usability audit knowledge |
| Knowledge Base | `rules.json` stores IF-THEN rules |
| Fact Base | User answers from the questionnaire |
| Inference Engine | Forward chaining functions in `app.py` |
| Explanation Facility | Triggered rules, condition trace, explanations, severity, recommendations |
| Output | Overall risk, severity score, triggered issues, downloadable JSON report |

## How the system works

```text
User answers audit questions
        ↓
Answers become facts
        ↓
System loads IF-THEN rules from rules.json
        ↓
Forward chaining checks facts against every rule
        ↓
Matching rules fire
        ↓
System shows UX issues, severity, explanation, and recommendation
        ↓
System exports a JSON audit report
```

## How to run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Recommended demo scenario

Use **Overloaded dashboard**.

Expected result:

- Overall Risk: High
- Rules Fired: 6
- Triggered issues:
  - High Cognitive Load
  - Poor Visual Hierarchy
  - Label Inconsistency
  - Unclear Navigation
  - No Current Location Indicator
  - Crowded Layout

## Correct way to explain the project

This is a **rule-based expert system prototype**, not a machine learning system. It does not automatically inspect screenshots. It audits a UI based on user-provided facts and expert IF-THEN rules.
