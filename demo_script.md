# 3-4 Minute Demo Script - Improved Version

## Opening

Good day. We are presenting our expert system prototype titled **Cognitive UX Design Auditor**.

This system helps identify cognitive UX problems in user interface designs. It uses a rule-based expert system approach, not machine learning. The system asks measurable questions about a UI screen, converts the answers into facts, checks those facts against IF-THEN rules, and produces UX issues with explanations and recommendations.

## Expert System Architecture tab

This tab shows the expert-system workflow.

The user provides facts through the questionnaire. These facts are checked against the knowledge base stored in `rules.json`. The inference engine uses forward chaining. When rule conditions are true, the rule fires and the system produces a UX issue.

The expert-system components are:

- Knowledge base
- Fact base
- Inference engine
- Explanation facility
- Final output

The important improvement is that the rules are now linked to cognitive theories such as Cognitive Load Theory, Miller's Law, Gestalt Principles, Recognition over Recall, Norman's Gulf of Execution, Cognitive Map Theory, and Perceptual Fluency Theory.

## Run UX Audit tab

For the demo, choose **Overloaded dashboard** from the sidebar.

This sample has too many visible options, no grouping, too many steps, weak visual hierarchy, inconsistent labels, unclear navigation, slow feedback, small text, and dense text blocks.

The questionnaire is now more objective because it uses measurable values such as:

- Number of visible options
- Number of task steps
- Number of items users must remember
- Number of clicks to reach the main task
- Feedback delay in seconds
- Font size
- 1-5 clarity scores

The system shows:

- Overall risk
- Severity score
- Number of rules fired
- Triggered issues
- Cognitive theories
- Explanations
- Recommendations

## Reasoning Trace tab

This is the strongest proof that the project is an expert system.

The tab shows every rule in the knowledge base. It shows whether each rule fired or did not fire. It also shows the exact condition checking process.

For example, the rule about too many visible options fires when `main_options > 7`. The explanation connects this to Miller's Law and working-memory limitations.

## Knowledge Base + Theory tab

This tab displays the IF-THEN rules from `rules.json`. Each rule has:

- Rule ID
- UX category
- Cognitive theory
- Key concept
- IF conditions
- THEN issue
- Severity
- Recommendation

This proves that the knowledge base is separate from the interface and that the rules are theory-supported.

## Testing Evidence tab

This tab shows test cases and expected risks.

The included cases are:

- Balanced UI: expected Low risk
- Overloaded dashboard: expected High risk
- Weak form validation: expected High risk
- Poor readability screen: expected High risk

The app also includes a test script. Running `python test_engine.py` checks whether the inference engine gives the expected result for each sample case.

## Closing

This prototype is useful because it gives explainable UX audit results. It does not only say that a UI is risky. It shows which expert rule was triggered, what facts caused the rule to fire, which cognitive theory supports the rule, why the issue matters, and what recommendation should be followed.

Therefore, this project demonstrates a rule-based expert system with a knowledge base, fact base, inference engine, explanation facility, user interface, theory mapping, and testing evidence.
