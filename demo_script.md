# 3-4 Minute Demo Script - Fixed Version

## Opening

Good day. We are presenting our expert system prototype titled **Cognitive UX Design Auditor**.

This system helps identify cognitive UX problems in user interface designs. It uses a rule-based expert system approach, not machine learning. The system asks questions about a UI screen, converts the answers into facts, checks those facts against IF-THEN rules, and produces UX issues with explanations and recommendations.

## Show Expert System Architecture tab

This tab shows the expert-system workflow.

The user provides facts through the questionnaire. These facts are checked against the knowledge base stored in `rules.json`. The inference engine uses forward chaining. When rule conditions are true, the rule fires and the system produces a UX issue.

The main expert-system components are:

- Knowledge base
- Fact base
- Inference engine
- Explanation facility
- Final output

## Run UX Audit tab

For the demo, choose **Overloaded dashboard** from the sidebar.

This sample has too many visible options, no grouping, unclear primary action, inconsistent labels, unclear navigation, no current location indicator, and crowded layout.

Click **Run UX Audit**.

The system shows:

- Overall Risk
- Severity Score
- Number of Rules Fired
- Triggered Issues
- Explanations
- Recommendations

## Reasoning Trace tab

This is the strongest proof that the project is an expert system.

The tab shows every rule in the knowledge base. It shows whether each rule fired or did not fire. It also shows the exact condition checking process.

For example, the high cognitive load rule fires because:

- main_options is greater than 7
- grouped_options equals No

Therefore, the system infers High Cognitive Load.

## Knowledge Base tab

This tab displays the IF-THEN rules from `rules.json`. This proves that the system has a separate knowledge base.

## Testing Evidence tab

This tab shows expected results for the sample test cases.

The overloaded dashboard should produce a high-risk result with six fired rules. The balanced UI should produce low risk with zero fired rules. The weak form validation case should produce high risk with four fired rules.

## Closing

This prototype is useful because it gives explainable UX audit results. It does not only say that a UI is risky. It shows which expert rule was triggered, what facts caused the rule to fire, why the issue matters, and what recommendation should be followed.

Therefore, this project demonstrates a rule-based expert system with a knowledge base, inference engine, explanation facility, user interface, and testing evidence.
