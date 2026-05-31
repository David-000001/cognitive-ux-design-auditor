# Cognitive UX Design Auditor - Improved Expert System Version

## Project title

**Cognitive UX Design Auditor**  
An explainable rule-based expert system for auditing cognitive usability problems in user interface design.

## What was fixed

This version fixes the main weakness from the expert feedback: the previous app used too many binary Yes/No rules. The improved version now uses measurable inputs and cognitive-theory-supported rules.

Main improvements:

1. Replaced many Yes/No questions with measurable values.
2. Added numeric questionnaire fields such as visible options, remembered items, clicks, feedback delay, font size, and 1-5 clarity scores.
3. Expanded the knowledge base from 12 rules to 30 IF-THEN rules.
4. Added cognitive theory mapping for every rule.
5. Added category-level summary.
6. Moved inference logic into `engine.py` so it is cleaner and easier to test.
7. Added `test_engine.py` to prove the rules produce expected results.
8. Updated the UI to show theory, key concept, fired rules, condition trace, severity, and recommendations.

## Expert system components

| Component | Implementation |
|---|---|
| Domain expertise | Cognitive UX / beginner usability audit knowledge |
| Knowledge Base | `rules.json` stores measurable IF-THEN rules |
| Fact Base | Numeric and Yes/No questionnaire answers from the user |
| Inference Engine | Forward chaining logic in `engine.py` |
| Explanation Facility | Triggered rules, condition trace, cognitive theory, explanation, severity, recommendations |
| Output | Overall risk, severity score, category summary, downloadable JSON report |

## Cognitive UX categories covered

1. Cognitive Load
2. Visual Hierarchy
3. Consistency
4. Recognition vs Recall
5. Error Prevention
6. Feedback & Recovery
7. Navigation Clarity
8. Readability

## Examples of measurable inputs

| UX area | Measurable input |
|---|---|
| Cognitive Load | Number of visible options, number of task steps, number of unrelated information blocks |
| Recognition vs Recall | Number of items users must remember, number of screens hiding important information |
| Visual Hierarchy | Number of primary-looking buttons, contrast score, hierarchy rating |
| Navigation Clarity | Number of clicks to main task, menu label clarity score |
| Feedback & Recovery | Feedback delay in seconds, error-message clarity score |
| Readability | Smallest font size, longest text block length, contrast score |

## How the system works

```text
User answers measurable audit questions
        ↓
Answers become facts
        ↓
System loads theory-supported IF-THEN rules from rules.json
        ↓
Forward chaining checks facts against every rule
        ↓
Matching rules fire
        ↓
System shows UX issues, severity, cognitive theory, explanation, and recommendation
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

## How to test

Run:

```bash
python test_engine.py
```

Expected result:

```text
All tests passed.
```

## Recommended demo scenario

Use **Overloaded dashboard**.

Expected result:

- Overall Risk: High
- Many rules fire across Cognitive Load, Visual Hierarchy, Consistency, Navigation Clarity, Feedback & Recovery, and Readability
- Reasoning Trace tab shows exactly why each rule fired

## Correct way to explain the project

This is a **rule-based expert system prototype**, not a machine learning system. It does not automatically inspect screenshots. It audits a UI based on user-provided measurable facts and expert IF-THEN rules.

The strongest part of the project is explainability: the system does not only say that a UI is risky; it shows the facts, rules, theory, reasoning trace, severity, and recommendation.
