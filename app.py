import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

APP_TITLE = "Cognitive UX Design Auditor"
RULE_FILE = Path(__file__).with_name("rules.json")
SEVERITY_SCORE = {"Low": 1, "Medium": 2, "High": 3}


# ------------------------------------------------------------
# KNOWLEDGE BASE LOADING
# ------------------------------------------------------------
def load_rules():
    """Load IF-THEN expert rules from the external knowledge base file."""
    with open(RULE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------------------------
# INFERENCE ENGINE
# ------------------------------------------------------------
def compare(actual, operator, expected):
    """Compare one fact value with one rule condition value."""
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


def evaluate_rule(rule, facts):
    """Evaluate a rule and return whether it fired plus condition-by-condition trace."""
    condition_trace = []
    fired = True

    for condition in rule["conditions"]:
        fact_name = condition["fact"]
        operator = condition["operator"]
        expected = condition["value"]
        actual = facts.get(fact_name, None)

        if fact_name not in facts:
            passed = False
        else:
            passed = compare(actual, operator, expected)

        condition_trace.append(
            {
                "Fact": fact_name,
                "Actual Value": actual,
                "Operator": operator,
                "Expected Value": expected,
                "Condition Result": "True" if passed else "False",
            }
        )

        if not passed:
            fired = False

    return fired, condition_trace


def run_forward_chaining(facts, rules):
    """
    Forward chaining inference:
    1. Start with known facts from the questionnaire.
    2. Check every IF-THEN rule in the knowledge base.
    3. Fire every rule whose IF conditions are true.
    4. Return conclusions and a reasoning trace.
    """
    fired_rules = []
    reasoning_trace = []

    for rule in rules:
        fired, condition_trace = evaluate_rule(rule, facts)
        reasoning_trace.append(
            {
                "Rule": rule["id"],
                "Category": rule["category"],
                "IF": " AND ".join(
                    f"{c['fact']} {c['operator']} {c['value']}" for c in rule["conditions"]
                ),
                "THEN": rule["issue"],
                "Fired?": "Yes" if fired else "No",
                "Severity": rule["severity"],
                "Condition Trace": condition_trace,
            }
        )
        if fired:
            fired_rules.append(rule)

    return fired_rules, reasoning_trace


def calculate_overall_risk(fired_rules):
    """Convert fired rule severities into one final UX risk level."""
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


# ------------------------------------------------------------
# SAMPLE CASES / TEST DATA
# ------------------------------------------------------------
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


def make_report(facts, fired_rules, reasoning_trace, overall_risk, total_score):
    return {
        "system": APP_TITLE,
        "system_type": "Rule-based expert system",
        "inference_method": "Forward chaining",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_facts": facts,
        "overall_risk": overall_risk,
        "severity_score": total_score,
        "triggered_rules": fired_rules,
        "reasoning_trace": reasoning_trace,
    }


def yes_no_radio(label, default_value, key):
    return st.radio(label, ["Yes", "No"], index=["Yes", "No"].index(default_value), key=key)


# ------------------------------------------------------------
# STREAMLIT USER INTERFACE
# ------------------------------------------------------------
st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")
st.title("🧠 Cognitive UX Design Auditor")
st.caption("Explainable rule-based expert system for cognitive UX auditing.")

rules = load_rules()

with st.sidebar:
    st.header("Demo Scenario")
    scenario = st.selectbox(
        "Load a sample case",
        ["Balanced / mostly good UI", "Overloaded dashboard", "Weak form validation"],
    )
    defaults = scenario_defaults(scenario)

    st.markdown("---")
    st.subheader("Expert System Parts")
    st.write("**Facts:** questionnaire answers")
    st.write("**Knowledge Base:** `rules.json`")
    st.write("**Inference Engine:** forward chaining")
    st.write("**Explanation:** rule trace + recommendations")

st.info(
    "This is not a machine-learning app. It is a rule-based expert system. "
    "The user gives facts about a UI screen, the inference engine checks the facts against IF-THEN rules, "
    "and the system explains which UX problems were inferred."
)

architecture_tab, audit_tab, trace_tab, kb_tab, testing_tab = st.tabs(
    [
        "1. Expert System Architecture",
        "2. Run UX Audit",
        "3. Reasoning Trace",
        "4. Knowledge Base",
        "5. Testing Evidence",
    ]
)

# ------------------------------------------------------------
# TAB 1: EXPERT SYSTEM ARCHITECTURE
# ------------------------------------------------------------
with architecture_tab:
    st.subheader("What this system does")
    st.write(
        "The system acts like a basic UX expert. It checks interface facts against expert rules "
        "and produces cognitive UX issues, severity, explanations, and recommendations."
    )

    st.markdown("### Expert system workflow")
    workflow = pd.DataFrame(
        [
            {"Step": 1, "Stage": "User Input", "What happens": "User answers audit questions about a UI screen."},
            {"Step": 2, "Stage": "Fact Base", "What happens": "Answers are stored as facts such as main_options = 12."},
            {"Step": 3, "Stage": "Knowledge Base", "What happens": "The system loads IF-THEN rules from rules.json."},
            {"Step": 4, "Stage": "Inference Engine", "What happens": "Forward chaining checks all facts against all rules."},
            {"Step": 5, "Stage": "Conclusion", "What happens": "Matched rules fire and generate UX issue conclusions."},
            {"Step": 6, "Stage": "Explanation Facility", "What happens": "The system shows why each rule fired and how to fix the issue."},
        ]
    )
    st.dataframe(workflow, use_container_width=True, hide_index=True)

    st.markdown("### Why this counts as an expert system")
    components = pd.DataFrame(
        [
            {"Expert System Component": "Domain expertise", "Implementation in this project": "Cognitive UX / usability audit knowledge"},
            {"Expert System Component": "Knowledge base", "Implementation in this project": "External IF-THEN rules stored in rules.json"},
            {"Expert System Component": "Fact base", "Implementation in this project": "Questionnaire answers collected from the user"},
            {"Expert System Component": "Inference engine", "Implementation in this project": "Forward chaining rule matching in app.py"},
            {"Expert System Component": "Explanation facility", "Implementation in this project": "Triggered rule explanation, condition trace, severity, recommendation"},
            {"Expert System Component": "Output", "Implementation in this project": "Overall risk level and JSON audit report"},
        ]
    )
    st.dataframe(components, use_container_width=True, hide_index=True)

    st.markdown("### Forward chaining logic")
    st.code(
        """START with user facts
FOR each IF-THEN rule in rules.json:
    CHECK every IF condition
    IF all conditions are true:
        FIRE the rule
        ADD its UX issue to the result
CALCULATE final risk from fired rule severities
SHOW explanations and recommendations""",
        language="text",
    )

# ------------------------------------------------------------
# TAB 2: MAIN AUDIT
# ------------------------------------------------------------
with audit_tab:
    left, right = st.columns([1.05, 1])

    with left:
        st.subheader("A. UI Audit Questionnaire / Fact Collection")
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
                grouped_options = yes_no_radio("Are related options grouped?", defaults["grouped_options"], "grouped_options")
                primary_action_clear = yes_no_radio("Is the primary action clear?", defaults["primary_action_clear"], "primary_action_clear")
                same_action_uses_different_labels = yes_no_radio("Does the same action use different labels?", defaults["same_action_uses_different_labels"], "same_action_uses_different_labels")
                user_must_remember_previous_info = yes_no_radio("Must users remember previous information?", defaults["user_must_remember_previous_info"], "user_must_remember_previous_info")
                hints_available = yes_no_radio("Are hints/contextual reminders available?", defaults["hints_available"], "hints_available")
            with col2:
                required_fields_exist = yes_no_radio("Are there required fields?", defaults["required_fields_exist"], "required_fields_exist")
                required_fields_marked = yes_no_radio("Are required fields clearly marked?", defaults["required_fields_marked"], "required_fields_marked")
                error_message_actionable = yes_no_radio("Are error messages actionable?", defaults["error_message_actionable"], "error_message_actionable")
                navigation_clear = yes_no_radio("Is navigation clear?", defaults["navigation_clear"], "navigation_clear")
                current_location_visible = yes_no_radio("Is the user's current location visible?", defaults["current_location_visible"], "current_location_visible")

            col3, col4, col5 = st.columns(3)
            with col3:
                text_readable = yes_no_radio("Is text readable?", defaults["text_readable"], "text_readable")
            with col4:
                contrast_sufficient = yes_no_radio("Is contrast sufficient?", defaults["contrast_sufficient"], "contrast_sufficient")
            with col5:
                spacing_crowded = yes_no_radio("Is the layout crowded?", defaults["spacing_crowded"], "spacing_crowded")

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

    fired_rules, reasoning_trace = run_forward_chaining(facts, rules)
    overall_risk, total_score = calculate_overall_risk(fired_rules)
    report = make_report(facts, fired_rules, reasoning_trace, overall_risk, total_score)

    with right:
        st.subheader("B. Expert System Output")
        risk_label = {"High": "🔴 High", "Medium": "🟠 Medium", "Low": "🟢 Low"}[overall_risk]
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Overall Risk", risk_label)
        metric2.metric("Severity Score", total_score)
        metric3.metric("Rules Fired", len(fired_rules))

        st.markdown("### Triggered Conclusions")
        if not fired_rules:
            st.success("No major cognitive UX issue was detected based on the current facts.")
        else:
            result_rows = [
                {
                    "Rule": rule["id"],
                    "Category": rule["category"],
                    "Inferred Issue": rule["issue"],
                    "Severity": rule["severity"],
                    "Recommendation": rule["recommendation"],
                }
                for rule in fired_rules
            ]
            st.dataframe(pd.DataFrame(result_rows), use_container_width=True, hide_index=True)

            for rule in fired_rules:
                with st.expander(f"{rule['id']} — {rule['issue']} ({rule['severity']})"):
                    st.write(f"**Category:** {rule['category']}")
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

    st.markdown("---")
    st.subheader("C. Fact Base Used by the Inference Engine")
    fact_rows = [{"Fact": key, "Value": value} for key, value in facts.items()]
    st.dataframe(pd.DataFrame(fact_rows), use_container_width=True, hide_index=True)

# Make variables available for the following tabs on initial page load.
try:
    facts
except NameError:
    facts = defaults.copy()
    fired_rules, reasoning_trace = run_forward_chaining(facts, rules)
    overall_risk, total_score = calculate_overall_risk(fired_rules)
    report = make_report(facts, fired_rules, reasoning_trace, overall_risk, total_score)

# ------------------------------------------------------------
# TAB 3: REASONING TRACE
# ------------------------------------------------------------
with trace_tab:
    st.subheader("Forward Chaining Reasoning Trace")
    st.write(
        "This tab makes the inference engine visible. It shows every rule, whether it fired, "
        "and the exact conditions checked against the current facts."
    )

    trace_summary = pd.DataFrame(
        [
            {
                "Rule": item["Rule"],
                "Category": item["Category"],
                "IF": item["IF"],
                "THEN": item["THEN"],
                "Fired?": item["Fired?"],
                "Severity": item["Severity"],
            }
            for item in reasoning_trace
        ]
    )
    st.dataframe(trace_summary, use_container_width=True, hide_index=True)

    st.markdown("### Detailed condition checking")
    for item in reasoning_trace:
        icon = "✅" if item["Fired?"] == "Yes" else "❌"
        with st.expander(f"{icon} {item['Rule']} — {item['THEN']} | Fired: {item['Fired?']}"):
            st.dataframe(pd.DataFrame(item["Condition Trace"]), use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# TAB 4: KNOWLEDGE BASE
# ------------------------------------------------------------
with kb_tab:
    st.subheader("Knowledge Base Preview: IF-THEN UX Rules")
    kb_rows = [
        {
            "Rule": rule["id"],
            "Category": rule["category"],
            "IF conditions": " AND ".join(f"{c['fact']} {c['operator']} {c['value']}" for c in rule["conditions"]),
            "THEN issue": rule["issue"],
            "Severity": rule["severity"],
            "Recommendation": rule["recommendation"],
        }
        for rule in rules
    ]
    st.dataframe(pd.DataFrame(kb_rows), use_container_width=True, hide_index=True)

    st.markdown("### Raw knowledge base file")
    with st.expander("Show rules.json"):
        st.json(rules)

# ------------------------------------------------------------
# TAB 5: TESTING EVIDENCE
# ------------------------------------------------------------
with testing_tab:
    st.subheader("Testing Evidence")
    st.write("Use these expected results to prove that the system behaves correctly.")

    expected_results = pd.DataFrame(
        [
            {
                "Test Case": "Balanced / mostly good UI",
                "Expected Risk": "Low",
                "Expected Rules Fired": 0,
                "Reason": "The facts represent a mostly usable UI, so no major rule should fire.",
            },
            {
                "Test Case": "Overloaded dashboard",
                "Expected Risk": "High",
                "Expected Rules Fired": 6,
                "Reason": "Many visible options, no grouping, unclear action, inconsistent labels, unclear navigation, crowded layout.",
            },
            {
                "Test Case": "Weak form validation",
                "Expected Risk": "High",
                "Expected Rules Fired": 4,
                "Reason": "Memory load, weak required-field marking, poor error recovery, and moderate cognitive load.",
            },
        ]
    )
    st.dataframe(expected_results, use_container_width=True, hide_index=True)

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

st.markdown("---")
st.markdown(
    "**Submission description:** Rule-based expert system prototype using a separate knowledge base, "
    "forward chaining inference, explainable rule firing, severity scoring, sample test cases, and JSON report export."
)
