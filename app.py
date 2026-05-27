import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

APP_TITLE = "Cognitive UX Design Auditor"
RULE_FILE = Path(__file__).with_name("rules.json")
SEVERITY_SCORE = {"Low": 1, "Medium": 2, "High": 3}


def load_rules():
    with open(RULE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def compare(actual, operator, expected):
    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator == ">":
        return actual > expected
    if operator == ">=":
        return actual >= expected
    if operator == "<":
        return actual < expected
    if operator == "<=":
        return actual <= expected
    raise ValueError(f"Unsupported operator: {operator}")


def rule_matches(rule, facts):
    for condition in rule["conditions"]:
        fact_name = condition["fact"]
        if fact_name not in facts:
            return False
        if not compare(facts[fact_name], condition["operator"], condition["value"]):
            return False
    return True


def run_forward_chaining(facts, rules):
    fired_rules = []
    for rule in rules:
        if rule_matches(rule, facts):
            fired_rules.append(rule)
    return fired_rules


def calculate_overall_risk(fired_rules):
    if not fired_rules:
        return "Low", 0
    total_score = sum(SEVERITY_SCORE[rule["severity"]] for rule in fired_rules)
    high_count = sum(1 for rule in fired_rules if rule["severity"] == "High")
    medium_count = sum(1 for rule in fired_rules if rule["severity"] == "Medium")
    if high_count >= 2 or total_score >= 7:
        return "High", total_score
    if high_count == 1 or medium_count >= 2 or total_score >= 3:
        return "Medium", total_score
    return "Low", total_score


def scenario_defaults(name):
    scenarios = {
        "Balanced / mostly good UI": {
            "screen_type": "Form",
            "main_options": 4,
            "grouped_options": "Yes",
            "primary_action_clear": "Yes",
            "same_action_uses_different_labels": "No",
            "user_must_remember_previous_info": "No",
            "hints_available": "Yes",
            "required_fields_exist": "Yes",
            "required_fields_marked": "Yes",
            "error_message_actionable": "Yes",
            "navigation_clear": "Yes",
            "current_location_visible": "Yes",
            "text_readable": "Yes",
            "contrast_sufficient": "Yes",
            "spacing_crowded": "No",
        },
        "Overloaded dashboard": {
            "screen_type": "Dashboard",
            "main_options": 12,
            "grouped_options": "No",
            "primary_action_clear": "No",
            "same_action_uses_different_labels": "Yes",
            "user_must_remember_previous_info": "No",
            "hints_available": "Yes",
            "required_fields_exist": "No",
            "required_fields_marked": "Yes",
            "error_message_actionable": "Yes",
            "navigation_clear": "No",
            "current_location_visible": "No",
            "text_readable": "Yes",
            "contrast_sufficient": "Yes",
            "spacing_crowded": "Yes",
        },
        "Weak form validation": {
            "screen_type": "Registration form",
            "main_options": 6,
            "grouped_options": "No",
            "primary_action_clear": "Yes",
            "same_action_uses_different_labels": "No",
            "user_must_remember_previous_info": "Yes",
            "hints_available": "No",
            "required_fields_exist": "Yes",
            "required_fields_marked": "No",
            "error_message_actionable": "No",
            "navigation_clear": "Yes",
            "current_location_visible": "Yes",
            "text_readable": "Yes",
            "contrast_sufficient": "Yes",
            "spacing_crowded": "No",
        },
    }
    return scenarios[name]


def make_report(facts, fired_rules, overall_risk, total_score):
    return {
        "system": APP_TITLE,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_facts": facts,
        "overall_risk": overall_risk,
        "severity_score": total_score,
        "triggered_rules": fired_rules,
    }


st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")
st.title("🧠 Cognitive UX Design Auditor")
st.caption("Rule-based Expert System prototype for auditing cognitive usability issues in UI design.")

with st.sidebar:
    st.header("Demo Scenario")
    scenario = st.selectbox(
        "Load a sample case",
        ["Balanced / mostly good UI", "Overloaded dashboard", "Weak form validation"],
    )
    defaults = scenario_defaults(scenario)
    st.markdown("---")
    st.subheader("Expert System Components")
    st.write("**Knowledge Base:** IF–THEN UX rules")
    st.write("**Inference Engine:** Forward chaining")
    st.write("**User Interface:** Streamlit questionnaire")
    st.write("**Output:** Issues, severity, explanation, recommendations")

rules = load_rules()

st.info(
    "This prototype starts from user-provided audit facts, checks them against the knowledge base, "
    "fires matching rules, and generates an explainable UX audit report."
)

left, right = st.columns([1.05, 1])

with left:
    st.subheader("1. UI Audit Questionnaire")
    with st.form("audit_form"):
        screen_type = st.text_input("Screen / interface type", value=defaults["screen_type"])
        main_options = st.number_input(
            "How many main visible actions/options are shown?",
            min_value=0,
            max_value=50,
            value=defaults["main_options"],
            step=1,
        )
        col1, col2 = st.columns(2)
        with col1:
            grouped_options = st.radio("Are related options grouped?", ["Yes", "No"], index=["Yes", "No"].index(defaults["grouped_options"]))
            primary_action_clear = st.radio("Is the primary action clear?", ["Yes", "No"], index=["Yes", "No"].index(defaults["primary_action_clear"]))
            same_action_uses_different_labels = st.radio("Does the same action use different labels?", ["Yes", "No"], index=["Yes", "No"].index(defaults["same_action_uses_different_labels"]))
            user_must_remember_previous_info = st.radio("Must users remember information from previous screens?", ["Yes", "No"], index=["Yes", "No"].index(defaults["user_must_remember_previous_info"]))
            hints_available = st.radio("Are hints/contextual reminders available?", ["Yes", "No"], index=["Yes", "No"].index(defaults["hints_available"]))
        with col2:
            required_fields_exist = st.radio("Are there required fields?", ["Yes", "No"], index=["Yes", "No"].index(defaults["required_fields_exist"]))
            required_fields_marked = st.radio("Are required fields clearly marked?", ["Yes", "No"], index=["Yes", "No"].index(defaults["required_fields_marked"]))
            error_message_actionable = st.radio("Are error messages actionable?", ["Yes", "No"], index=["Yes", "No"].index(defaults["error_message_actionable"]))
            navigation_clear = st.radio("Is navigation clear?", ["Yes", "No"], index=["Yes", "No"].index(defaults["navigation_clear"]))
            current_location_visible = st.radio("Is the user's current location visible?", ["Yes", "No"], index=["Yes", "No"].index(defaults["current_location_visible"]))
        col3, col4, col5 = st.columns(3)
        with col3:
            text_readable = st.radio("Is text readable?", ["Yes", "No"], index=["Yes", "No"].index(defaults["text_readable"]))
        with col4:
            contrast_sufficient = st.radio("Is contrast sufficient?", ["Yes", "No"], index=["Yes", "No"].index(defaults["contrast_sufficient"]))
        with col5:
            spacing_crowded = st.radio("Is the layout crowded?", ["Yes", "No"], index=["Yes", "No"].index(defaults["spacing_crowded"]))
        st.form_submit_button("Run UX Audit")

facts = {
    "screen_type": screen_type,
    "main_options": int(main_options),
    "grouped_options": grouped_options,
    "primary_action_clear": primary_action_clear,
    "same_action_uses_different_labels": same_action_uses_different_labels,
    "user_must_remember_previous_info": user_must_remember_previous_info,
    "hints_available": hints_available,
    "required_fields_exist": required_fields_exist,
    "required_fields_marked": required_fields_marked,
    "error_message_actionable": error_message_actionable,
    "navigation_clear": navigation_clear,
    "current_location_visible": current_location_visible,
    "text_readable": text_readable,
    "contrast_sufficient": contrast_sufficient,
    "spacing_crowded": spacing_crowded,
}

fired_rules = run_forward_chaining(facts, rules)
overall_risk, total_score = calculate_overall_risk(fired_rules)
report = make_report(facts, fired_rules, overall_risk, total_score)

with right:
    st.subheader("2. Expert System Output")
    risk_label = {"High": "🔴 High", "Medium": "🟠 Medium", "Low": "🟢 Low"}[overall_risk]
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Overall Risk", risk_label)
    metric2.metric("Severity Score", total_score)
    metric3.metric("Rules Fired", len(fired_rules))
    st.markdown("### Triggered Issues")
    if not fired_rules:
        st.success("No major cognitive UX issue was detected based on the current facts.")
    else:
        result_rows = [
            {"Rule": rule["id"], "Category": rule["category"], "Issue": rule["issue"], "Severity": rule["severity"], "Recommendation": rule["recommendation"]}
            for rule in fired_rules
        ]
        st.dataframe(pd.DataFrame(result_rows), use_container_width=True, hide_index=True)
        for rule in fired_rules:
            with st.expander(f"{rule['id']} — {rule['issue']} ({rule['severity']})"):
                st.write(f"**Category:** {rule['category']}")
                st.write(f"**Explanation:** {rule['explanation']}")
                st.write(f"**Recommendation:** {rule['recommendation']}")
                st.write("**Conditions checked:**")
                st.json(rule["conditions"])
    st.download_button(
        "Download audit report as JSON",
        data=json.dumps(report, indent=2),
        file_name="cognitive_ux_audit_report.json",
        mime="application/json",
    )

st.markdown("---")
st.subheader("3. Knowledge Base Preview")
kb_rows = [
    {
        "Rule": rule["id"],
        "Category": rule["category"],
        "Issue": rule["issue"],
        "Severity": rule["severity"],
        "IF conditions": " AND ".join(f"{c['fact']} {c['operator']} {c['value']}" for c in rule["conditions"]),
        "THEN recommendation": rule["recommendation"],
    }
    for rule in rules
]
st.dataframe(pd.DataFrame(kb_rows), use_container_width=True, hide_index=True)

st.markdown(
    """
### How this matches WID2001 requirements

- **Knowledge Base:** stored in `rules.json`
- **Inference Engine:** forward chaining in `run_forward_chaining()`
- **User Interface:** questionnaire and result dashboard
- **Explanation Facility:** every fired rule shows reason, severity, and recommendation
- **Testing:** sample scenarios can be loaded from the sidebar
"""
)
