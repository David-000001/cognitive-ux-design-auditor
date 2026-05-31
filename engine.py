import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Tuple

SEVERITY_SCORE = {"Low": 1, "Medium": 2, "High": 3}
DEFAULT_RULE_FILE = Path(__file__).with_name("rules.json")


def load_rules(rule_file: Path = DEFAULT_RULE_FILE) -> List[Dict[str, Any]]:
    """Load IF-THEN expert rules from the external knowledge base file."""
    with open(rule_file, "r", encoding="utf-8") as file:
        rules = json.load(file)

    required_rule_keys = {"id", "category", "issue", "conditions", "severity", "recommendation", "explanation"}
    for rule in rules:
        missing = required_rule_keys - set(rule.keys())
        if missing:
            raise ValueError(f"Rule {rule.get('id', '<unknown>')} is missing keys: {sorted(missing)}")
        if rule["severity"] not in SEVERITY_SCORE:
            raise ValueError(f"Rule {rule['id']} has invalid severity: {rule['severity']}")
        if not isinstance(rule["conditions"], list) or not rule["conditions"]:
            raise ValueError(f"Rule {rule['id']} must contain at least one condition")
    return rules


def _normalise(value: Any) -> Any:
    """Normalise string values so Yes/No comparisons are less fragile."""
    if isinstance(value, str):
        return value.strip()
    return value


def compare(actual: Any, operator: str, expected: Any) -> bool:
    """Compare one fact value with one rule condition value."""
    actual = _normalise(actual)
    expected = _normalise(expected)

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
    if operator == "in":
        return actual in expected
    if operator == "not in":
        return actual not in expected
    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_rule(rule: Dict[str, Any], facts: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
    """Evaluate one rule and return whether it fired plus a condition-by-condition trace."""
    condition_trace = []
    fired = True

    for condition in rule["conditions"]:
        fact_name = condition["fact"]
        operator = condition["operator"]
        expected = condition["value"]
        actual = facts.get(fact_name)

        if fact_name not in facts:
            passed = False
        else:
            try:
                passed = compare(actual, operator, expected)
            except TypeError:
                passed = False

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


def condition_to_text(condition: Dict[str, Any]) -> str:
    return f"{condition['fact']} {condition['operator']} {condition['value']}"


def run_forward_chaining(facts: Dict[str, Any], rules: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Forward chaining inference.

    The system starts with known facts from the questionnaire, checks every IF-THEN rule,
    fires every rule whose conditions are true, and returns the conclusions plus a trace.
    """
    fired_rules = []
    reasoning_trace = []

    for rule in rules:
        fired, condition_trace = evaluate_rule(rule, facts)
        reasoning_trace.append(
            {
                "Rule": rule["id"],
                "Category": rule["category"],
                "Theory": rule.get("theory", ""),
                "Key Concept": rule.get("concept", ""),
                "IF": " AND ".join(condition_to_text(c) for c in rule["conditions"]),
                "THEN": rule["issue"],
                "Fired?": "Yes" if fired else "No",
                "Severity": rule["severity"],
                "Score": rule.get("score", SEVERITY_SCORE[rule["severity"]]),
                "Condition Trace": condition_trace,
            }
        )
        if fired:
            fired_rules.append(rule)

    return fired_rules, reasoning_trace


def calculate_overall_risk(fired_rules: List[Dict[str, Any]]) -> Tuple[str, int]:
    """Convert fired rule severities into one final UX risk level."""
    if not fired_rules:
        return "Low", 0

    total_score = sum(int(rule.get("score", SEVERITY_SCORE[rule["severity"]])) for rule in fired_rules)
    high_count = sum(1 for rule in fired_rules if rule["severity"] == "High")
    medium_count = sum(1 for rule in fired_rules if rule["severity"] == "Medium")

    if high_count >= 2 or total_score >= 8:
        return "High", total_score
    if high_count == 1 or medium_count >= 2 or total_score >= 3:
        return "Medium", total_score
    return "Low", total_score


def category_summary(fired_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Summarise fired rules by UX category."""
    summary: Dict[str, Dict[str, Any]] = {}
    for rule in fired_rules:
        category = rule["category"]
        score = int(rule.get("score", SEVERITY_SCORE[rule["severity"]]))
        current = summary.setdefault(
            category,
            {
                "Category": category,
                "Rules Fired": 0,
                "Category Score": 0,
                "Highest Severity": "Low",
                "Issues": [],
            },
        )
        current["Rules Fired"] += 1
        current["Category Score"] += score
        current["Issues"].append(rule["issue"])
        if SEVERITY_SCORE[rule["severity"]] > SEVERITY_SCORE[current["Highest Severity"]]:
            current["Highest Severity"] = rule["severity"]

    return list(summary.values())


def make_report(
    facts: Dict[str, Any],
    fired_rules: List[Dict[str, Any]],
    reasoning_trace: List[Dict[str, Any]],
    overall_risk: str,
    total_score: int,
) -> Dict[str, Any]:
    return {
        "system": "Cognitive UX Design Auditor",
        "system_type": "Rule-based expert system",
        "inference_method": "Forward chaining",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_facts": facts,
        "overall_risk": overall_risk,
        "severity_score": total_score,
        "category_summary": category_summary(fired_rules),
        "triggered_rules": fired_rules,
        "reasoning_trace": reasoning_trace,
    }
