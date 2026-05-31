import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from engine import (
    category_summary,
    calculate_overall_risk,
    load_rules,
    make_report,
    run_forward_chaining,
)

APP_TITLE = "Cognitive UX Design Auditor"
RULE_FILE = Path(__file__).with_name("rules.json")

CATEGORY_THEORY_MAP = [
    {
        "UX Category": "Cognitive Load",
        "Relevant Cognitive Theory": "Cognitive Load Theory, Miller's Law, Working Memory Model",
        "Measurable Inputs Used": "main options, task steps, unrelated information blocks, grouping",
    },
    {
        "UX Category": "Visual Hierarchy",
        "Relevant Cognitive Theory": "Gestalt Principles, Feature Integration Theory, Signal Detection Theory",
        "Measurable Inputs Used": "primary CTA count, contrast score, visual hierarchy rating",
    },
    {
        "UX Category": "Consistency",
        "Relevant Cognitive Theory": "Schema Theory, Habit Formation Theory, Recognition Priming",
        "Measurable Inputs Used": "inconsistent labels count, layout inconsistency count, navigation position changes",
    },
    {
        "UX Category": "Recognition vs Recall",
        "Relevant Cognitive Theory": "Recognition over Recall, Encoding Specificity, Long-term vs Working Memory",
        "Measurable Inputs Used": "items to remember, hidden information screens, visible hints",
    },
    {
        "UX Category": "Error Prevention",
        "Relevant Cognitive Theory": "Norman's Gulf of Execution, Human Error Theory, Affordance Theory",
        "Measurable Inputs Used": "confirmation, validation, risky action placement",
    },
    {
        "UX Category": "Feedback & Recovery",
        "Relevant Cognitive Theory": "Feedback Loop Theory, Reinforcement Learning, Norman's Gulf of Evaluation",
        "Measurable Inputs Used": "feedback delay, error clarity score, undo/retry availability",
    },
    {
        "UX Category": "Navigation Clarity",
        "Relevant Cognitive Theory": "Cognitive Map Theory, Information Scent Theory, Wayfinding Theory",
        "Measurable Inputs Used": "clicks to main task, current-location cue, menu clarity score",
    },
    {
        "UX Category": "Readability",
        "Relevant Cognitive Theory": "Perceptual Fluency Theory, Dual Coding Theory, Attention Theory",
        "Measurable Inputs Used": "font size, text block length, contrast score, text-visual balance",
    },
]


def yes_no(label: str, default_value: str, key: str) -> str:
    return st.radio(label, ["Yes", "No"], index=["Yes", "No"].index(default_value), key=key, horizontal=True)


def scenario_defaults(name: str) -> dict:
    scenarios = {
        "Balanced / mostly good UI": {
            "screen_type": "Checkout form",
            "main_options": 4,
            "grouped_options": "Yes",
            "task_steps": 2,
            "unrelated_info_blocks": 1,
            "primary_cta_count": 1,
            "primary_action_contrast_score": 5,
            "visual_hierarchy_rating": 5,
            "inconsistent_labels_count": 0,
            "layout_inconsistency_count": 0,
            "navigation_position_changes": "No",
            "items_to_remember": 1,
            "hidden_info_screens": 0,
            "labels_hints_visible": "Yes",
            "destructive_without_confirmation": "No",
            "form_validation_present": "Yes",
            "risky_actions_near_safe_actions": "No",
            "feedback_delay_seconds": 0.5,
            "error_message_clarity_score": 5,
            "undo_retry_available": "Yes",
            "clicks_to_main_task": 2,
            "current_location_visible": "Yes",
            "menu_label_clarity_score": 5,
            "smallest_font_size": 16,
            "longest_text_block_lines": 3,
            "contrast_score": 5,
            "text_visual_balance_score": 5,
        },
        "Overloaded dashboard": {
            "screen_type": "Admin dashboard",
            "main_options": 12,
            "grouped_options": "No",
            "task_steps": 5,
            "unrelated_info_blocks": 5,
            "primary_cta_count": 4,
            "primary_action_contrast_score": 2,
            "visual_hierarchy_rating": 2,
            "inconsistent_labels_count": 3,
            "layout_inconsistency_count": 2,
            "navigation_position_changes": "Yes",
            "items_to_remember": 2,
            "hidden_info_screens": 1,
            "labels_hints_visible": "Yes",
            "destructive_without_confirmation": "No",
            "form_validation_present": "Yes",
            "risky_actions_near_safe_actions": "No",
            "feedback_delay_seconds": 3.0,
            "error_message_clarity_score": 3,
            "undo_retry_available": "Yes",
            "clicks_to_main_task": 5,
            "current_location_visible": "No",
            "menu_label_clarity_score": 2,
            "smallest_font_size": 12,
            "longest_text_block_lines": 7,
            "contrast_score": 3,
            "text_visual_balance_score": 2,
        },
        "Weak form validation": {
            "screen_type": "Registration form",
            "main_options": 6,
            "grouped_options": "No",
            "task_steps": 4,
            "unrelated_info_blocks": 2,
            "primary_cta_count": 1,
            "primary_action_contrast_score": 4,
            "visual_hierarchy_rating": 4,
            "inconsistent_labels_count": 1,
            "layout_inconsistency_count": 0,
            "navigation_position_changes": "No",
            "items_to_remember": 5,
            "hidden_info_screens": 2,
            "labels_hints_visible": "No",
            "destructive_without_confirmation": "Yes",
            "form_validation_present": "No",
            "risky_actions_near_safe_actions": "Yes",
            "feedback_delay_seconds": 2.5,
            "error_message_clarity_score": 1,
            "undo_retry_available": "No",
            "clicks_to_main_task": 3,
            "current_location_visible": "Yes",
            "menu_label_clarity_score": 4,
            "smallest_font_size": 14,
            "longest_text_block_lines": 4,
            "contrast_score": 4,
            "text_visual_balance_score": 4,
        },
        "Poor readability screen": {
            "screen_type": "Policy / instruction page",
            "main_options": 3,
            "grouped_options": "Yes",
            "task_steps": 2,
            "unrelated_info_blocks": 1,
            "primary_cta_count": 1,
            "primary_action_contrast_score": 3,
            "visual_hierarchy_rating": 3,
            "inconsistent_labels_count": 0,
            "layout_inconsistency_count": 0,
            "navigation_position_changes": "No",
            "items_to_remember": 2,
            "hidden_info_screens": 0,
            "labels_hints_visible": "Yes",
            "destructive_without_confirmation": "No",
            "form_validation_present": "Yes",
            "risky_actions_near_safe_actions": "No",
            "feedback_delay_seconds": 1.2,
            "error_message_clarity_score": 4,
            "undo_retry_available": "Yes",
            "clicks_to_main_task": 2,
            "current_location_visible": "Yes",
            "menu_label_clarity_score": 4,
            "smallest_font_size": 11,
            "longest_text_block_lines": 10,
            "contrast_score": 2,
            "text_visual_balance_score": 2,
        },
    }
    return scenarios[name]


def build_facts(defaults: dict, scenario_key: str) -> dict:
    def k(name: str) -> str:
        return f"{scenario_key}_{name}"

    st.subheader("A. UI Audit Questionnaire / Fact Collection")
    st.caption("Most inputs are now measurable numbers or 1-5 scores, not only yes/no answers.")

    screen_type = st.text_input("Screen / interface type", value=defaults["screen_type"], key=k("screen_type"))

    with st.expander("1. Cognitive Load", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            main_options = st.number_input("Number of main visible actions/options", 0, 50, defaults["main_options"], 1, key=k("main_options"))
            task_steps = st.number_input("Steps needed to complete the main task", 0, 30, defaults["task_steps"], 1, key=k("task_steps"))
        with c2:
            unrelated_info_blocks = st.number_input("Unrelated information blocks on the screen", 0, 30, defaults["unrelated_info_blocks"], 1, key=k("unrelated_info_blocks"))
            grouped_options = yes_no("Are related options grouped?", defaults["grouped_options"], k("grouped_options"))

    with st.expander("2. Visual Hierarchy", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            primary_cta_count = st.number_input("Number of primary-looking CTA buttons", 0, 20, defaults["primary_cta_count"], 1, key=k("primary_cta_count"))
        with c2:
            primary_action_contrast_score = st.slider("Primary action contrast score", 1, 5, defaults["primary_action_contrast_score"], key=k("primary_action_contrast_score"))
        with c3:
            visual_hierarchy_rating = st.slider("Overall visual hierarchy rating", 1, 5, defaults["visual_hierarchy_rating"], key=k("visual_hierarchy_rating"))

    with st.expander("3. Consistency", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            inconsistent_labels_count = st.number_input("Inconsistent button/icon labels found", 0, 30, defaults["inconsistent_labels_count"], 1, key=k("inconsistent_labels_count"))
        with c2:
            layout_inconsistency_count = st.number_input("Unexpected layout inconsistencies found", 0, 30, defaults["layout_inconsistency_count"], 1, key=k("layout_inconsistency_count"))
        with c3:
            navigation_position_changes = yes_no("Does navigation position change between screens?", defaults["navigation_position_changes"], k("navigation_position_changes"))

    with st.expander("4. Recognition vs Recall", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            items_to_remember = st.number_input("Items users must remember from previous screens", 0, 20, defaults["items_to_remember"], 1, key=k("items_to_remember"))
        with c2:
            hidden_info_screens = st.number_input("Screens/tabs hiding important information", 0, 20, defaults["hidden_info_screens"], 1, key=k("hidden_info_screens"))
        with c3:
            labels_hints_visible = yes_no("Are labels, hints, summaries, or examples visible?", defaults["labels_hints_visible"], k("labels_hints_visible"))

    with st.expander("5. Error Prevention", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            destructive_without_confirmation = yes_no("Any destructive action without confirmation?", defaults["destructive_without_confirmation"], k("destructive_without_confirmation"))
        with c2:
            form_validation_present = yes_no("Is form/input validation present?", defaults["form_validation_present"], k("form_validation_present"))
        with c3:
            risky_actions_near_safe_actions = yes_no("Are risky actions placed near safe actions?", defaults["risky_actions_near_safe_actions"], k("risky_actions_near_safe_actions"))

    with st.expander("6. Feedback & Recovery", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            feedback_delay_seconds = st.number_input("Feedback delay after action, in seconds", 0.0, 30.0, float(defaults["feedback_delay_seconds"]), 0.1, key=k("feedback_delay_seconds"))
        with c2:
            error_message_clarity_score = st.slider("Error message clarity score", 1, 5, defaults["error_message_clarity_score"], key=k("error_message_clarity_score"))
        with c3:
            undo_retry_available = yes_no("Is undo/retry/back/edit available?", defaults["undo_retry_available"], k("undo_retry_available"))

    with st.expander("7. Navigation Clarity", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            clicks_to_main_task = st.number_input("Clicks needed to reach main function", 0, 30, defaults["clicks_to_main_task"], 1, key=k("clicks_to_main_task"))
        with c2:
            current_location_visible = yes_no("Is the user's current location visible?", defaults["current_location_visible"], k("current_location_visible"))
        with c3:
            menu_label_clarity_score = st.slider("Menu label clarity score", 1, 5, defaults["menu_label_clarity_score"], key=k("menu_label_clarity_score"))

    with st.expander("8. Readability", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            smallest_font_size = st.number_input("Smallest font size, px", 6, 40, defaults["smallest_font_size"], 1, key=k("smallest_font_size"))
        with c2:
            longest_text_block_lines = st.number_input("Longest unbroken text block, lines", 0, 50, defaults["longest_text_block_lines"], 1, key=k("longest_text_block_lines"))
        with c3:
            contrast_score = st.slider("Text/background contrast score", 1, 5, defaults["contrast_score"], key=k("contrast_score"))
        with c4:
            text_visual_balance_score = st.slider("Text-visual balance score", 1, 5, defaults["text_visual_balance_score"], key=k("text_visual_balance_score"))

    return {
        "screen_type": screen_type,
        "main_options": int(main_options),
        "grouped_options": grouped_options,
        "task_steps": int(task_steps),
        "unrelated_info_blocks": int(unrelated_info_blocks),
        "primary_cta_count": int(primary_cta_count),
        "primary_action_contrast_score": int(primary_action_contrast_score),
        "visual_hierarchy_rating": int(visual_hierarchy_rating),
        "inconsistent_labels_count": int(inconsistent_labels_count),
        "layout_inconsistency_count": int(layout_inconsistency_count),
        "navigation_position_changes": navigation_position_changes,
        "items_to_remember": int(items_to_remember),
        "hidden_info_screens": int(hidden_info_screens),
        "labels_hints_visible": labels_hints_visible,
        "destructive_without_confirmation": destructive_without_confirmation,
        "form_validation_present": form_validation_present,
        "risky_actions_near_safe_actions": risky_actions_near_safe_actions,
        "feedback_delay_seconds": float(feedback_delay_seconds),
        "error_message_clarity_score": int(error_message_clarity_score),
        "undo_retry_available": undo_retry_available,
        "clicks_to_main_task": int(clicks_to_main_task),
        "current_location_visible": current_location_visible,
        "menu_label_clarity_score": int(menu_label_clarity_score),
        "smallest_font_size": int(smallest_font_size),
        "longest_text_block_lines": int(longest_text_block_lines),
        "contrast_score": int(contrast_score),
        "text_visual_balance_score": int(text_visual_balance_score),
    }


def show_triggered_results(fired_rules, overall_risk, total_score, report):
    risk_label = {"High": "🔴 High", "Medium": "🟠 Medium", "Low": "🟢 Low"}[overall_risk]
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Risk", risk_label)
    m2.metric("Severity Score", total_score)
    m3.metric("Rules Fired", len(fired_rules))

    st.markdown("### Triggered Conclusions")
    if not fired_rules:
        st.success("No major cognitive UX issue was detected based on the current facts.")
    else:
        rows = [
            {
                "Rule": r["id"],
                "Category": r["category"],
                "Issue": r["issue"],
                "Severity": r["severity"],
                "Theory": r.get("theory", ""),
                "Recommendation": r["recommendation"],
            }
            for r in fired_rules
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("### Category Summary")
        st.dataframe(pd.DataFrame(category_summary(fired_rules)), use_container_width=True, hide_index=True)

        for rule in fired_rules:
            with st.expander(f"{rule['id']} — {rule['issue']} ({rule['severity']})"):
                st.write(f"**Category:** {rule['category']}")
                st.write(f"**Theory:** {rule.get('theory', 'Not specified')}")
                st.write(f"**Key concept:** {rule.get('concept', 'Not specified')}")
                st.write(f"**Explanation:** {rule['explanation']}")
                st.write(f"**Recommendation:** {rule['recommendation']}")
                st.write("**IF conditions:**")
                st.json(rule["conditions"])

    st.download_button(
        "Download full JSON audit report",
        data=json.dumps(report, indent=2),
        file_name="cognitive_ux_audit_report.json",
        mime="application/json",
    )


st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")
st.title("🧠 Cognitive UX Design Auditor")
st.caption("Explainable rule-based expert system for cognitive UX auditing.")

rules = load_rules(RULE_FILE)

with st.sidebar:
    st.header("Demo Scenario")
    scenario = st.selectbox(
        "Load a sample case",
        [
            "Balanced / mostly good UI",
            "Overloaded dashboard",
            "Weak form validation",
            "Poor readability screen",
        ],
    )
    defaults = scenario_defaults(scenario)

    st.markdown("---")
    st.subheader("Expert System Parts")
    st.write("**Facts:** questionnaire answers")
    st.write("**Knowledge Base:** `rules.json`")
    st.write("**Inference Engine:** forward chaining")
    st.write("**Explanation:** rule trace + recommendations")

st.info(
    "This version uses measurable survey inputs such as number of visible options, items to remember, clicks, feedback delay, "
    "font size, and 1-5 clarity scores. The rules are also mapped to cognitive theories so the system fits the expert feedback better."
)

architecture_tab, audit_tab, trace_tab, kb_tab, testing_tab = st.tabs(
    [
        "1. Expert System Architecture",
        "2. Run UX Audit",
        "3. Reasoning Trace",
        "4. Knowledge Base + Theory",
        "5. Testing Evidence",
    ]
)

with architecture_tab:
    st.subheader("What this system does")
    st.write(
        "The system behaves like a beginner-level cognitive UX expert. It converts questionnaire answers into facts, "
        "checks them against IF-THEN rules, and produces UX issues with severity, cognitive-theory explanations, and recommendations."
    )

    st.markdown("### Expert system workflow")
    workflow = pd.DataFrame(
        [
            {"Step": 1, "Stage": "User Input", "What happens": "User answers measurable audit questions about a UI screen."},
            {"Step": 2, "Stage": "Fact Base", "What happens": "Answers are stored as facts, e.g. items_to_remember = 5."},
            {"Step": 3, "Stage": "Knowledge Base", "What happens": "The system loads theory-supported IF-THEN rules from rules.json."},
            {"Step": 4, "Stage": "Inference Engine", "What happens": "Forward chaining checks every rule against the facts."},
            {"Step": 5, "Stage": "Conclusion", "What happens": "Matched rules fire and infer UX issues."},
            {"Step": 6, "Stage": "Explanation Facility", "What happens": "The app shows rule trace, theory, explanation, severity, and recommendation."},
        ]
    )
    st.dataframe(workflow, use_container_width=True, hide_index=True)

    st.markdown("### Cognitive UX categories and theory mapping")
    st.dataframe(pd.DataFrame(CATEGORY_THEORY_MAP), use_container_width=True, hide_index=True)

    st.markdown("### Forward chaining logic")
    st.code(
        """START with user facts
FOR each IF-THEN rule in rules.json:
    CHECK every IF condition
    IF all conditions are true:
        FIRE the rule
        ADD its UX issue to the result
CALCULATE final risk from fired rule severities
SHOW theory, explanation, recommendation, and reasoning trace""",
        language="text",
    )

with audit_tab:
    left, right = st.columns([1.05, 1])

    with left:
        scenario_key = scenario.lower().replace(" / ", "_").replace(" ", "_").replace("-", "_")
        facts = build_facts(defaults, scenario_key)

    fired_rules, reasoning_trace = run_forward_chaining(facts, rules)
    overall_risk, total_score = calculate_overall_risk(fired_rules)
    report = make_report(facts, fired_rules, reasoning_trace, overall_risk, total_score)

    with right:
        st.subheader("B. Expert System Output")
        show_triggered_results(fired_rules, overall_risk, total_score, report)

    st.markdown("---")
    st.subheader("C. Fact Base Used by the Inference Engine")
    fact_rows = [{"Fact": key, "Value": value} for key, value in facts.items()]
    st.dataframe(pd.DataFrame(fact_rows), use_container_width=True, hide_index=True)

try:
    facts
except NameError:
    facts = defaults.copy()
    fired_rules, reasoning_trace = run_forward_chaining(facts, rules)
    overall_risk, total_score = calculate_overall_risk(fired_rules)
    report = make_report(facts, fired_rules, reasoning_trace, overall_risk, total_score)

with trace_tab:
    st.subheader("Forward Chaining Reasoning Trace")
    st.write("This tab proves the expert-system reasoning process rule by rule.")

    trace_summary = pd.DataFrame(
        [
            {
                "Rule": item["Rule"],
                "Category": item["Category"],
                "Theory": item["Theory"],
                "IF": item["IF"],
                "THEN": item["THEN"],
                "Fired?": item["Fired?"],
                "Severity": item["Severity"],
                "Score": item["Score"],
            }
            for item in reasoning_trace
        ]
    )
    st.dataframe(trace_summary, use_container_width=True, hide_index=True)

    st.markdown("### Detailed condition checking")
    for item in reasoning_trace:
        icon = "✅" if item["Fired?"] == "Yes" else "❌"
        with st.expander(f"{icon} {item['Rule']} — {item['THEN']} | Fired: {item['Fired?']}"):
            st.write(f"**Theory:** {item['Theory']}")
            st.write(f"**Key concept:** {item['Key Concept']}")
            st.dataframe(pd.DataFrame(item["Condition Trace"]), use_container_width=True, hide_index=True)

with kb_tab:
    st.subheader("Knowledge Base Preview: IF-THEN UX Rules")
    kb_rows = [
        {
            "Rule": rule["id"],
            "Category": rule["category"],
            "Theory": rule.get("theory", ""),
            "Key Concept": rule.get("concept", ""),
            "IF conditions": " AND ".join(f"{c['fact']} {c['operator']} {c['value']}" for c in rule["conditions"]),
            "THEN issue": rule["issue"],
            "Severity": rule["severity"],
            "Score": rule.get("score", ""),
            "Recommendation": rule["recommendation"],
        }
        for rule in rules
    ]
    st.dataframe(pd.DataFrame(kb_rows), use_container_width=True, hide_index=True)

    st.markdown("### Category-to-theory table")
    st.dataframe(pd.DataFrame(CATEGORY_THEORY_MAP), use_container_width=True, hide_index=True)

    st.markdown("### Raw knowledge base file")
    with st.expander("Show rules.json"):
        st.json(rules)

with testing_tab:
    st.subheader("Testing Evidence")
    st.write("These sample cases are included so you can show that the inference engine is working.")

    sample_path = Path(__file__).with_name("sample_test_cases.csv")
    if sample_path.exists():
        sample_df = pd.read_csv(sample_path)
        st.dataframe(sample_df, use_container_width=True, hide_index=True)

    st.markdown("### Current selected scenario result")
    st.write(f"**Selected scenario:** {scenario}")
    st.write(f"**Actual risk:** {overall_risk}")
    st.write(f"**Actual rules fired:** {len(fired_rules)}")

    if fired_rules:
        st.write("**Actual triggered rules:**")
        st.dataframe(
            pd.DataFrame([{"Rule": r["id"], "Issue": r["issue"], "Severity": r["severity"]} for r in fired_rules]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("Current scenario fired zero rules.")

    st.markdown("### Test runner")
    st.code("python test_engine.py", language="bash")

st.markdown("---")
st.markdown(
    "**Submission description:** Rule-based expert system prototype using measurable questionnaire facts, "
    "theory-supported IF-THEN rules, forward chaining inference, explainable rule firing, severity scoring, sample test cases, and JSON report export."
)
