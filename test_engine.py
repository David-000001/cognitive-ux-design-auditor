from pathlib import Path

import pandas as pd

from engine import calculate_overall_risk, load_rules, run_forward_chaining

RULES = load_rules(Path(__file__).with_name("rules.json"))
TEST_CASES = pd.read_csv(Path(__file__).with_name("sample_test_cases.csv"))

NUMERIC_COLUMNS = {
    "main_options": int,
    "task_steps": int,
    "unrelated_info_blocks": int,
    "primary_cta_count": int,
    "primary_action_contrast_score": int,
    "visual_hierarchy_rating": int,
    "inconsistent_labels_count": int,
    "layout_inconsistency_count": int,
    "items_to_remember": int,
    "hidden_info_screens": int,
    "feedback_delay_seconds": float,
    "error_message_clarity_score": int,
    "clicks_to_main_task": int,
    "menu_label_clarity_score": int,
    "smallest_font_size": int,
    "longest_text_block_lines": int,
    "contrast_score": int,
    "text_visual_balance_score": int,
}

META_COLUMNS = {"Test ID", "Scenario", "Expected Risk"}


def row_to_facts(row):
    facts = {}
    for key, value in row.items():
        if key in META_COLUMNS:
            continue
        if key in NUMERIC_COLUMNS:
            facts[key] = NUMERIC_COLUMNS[key](value)
        else:
            facts[key] = value
    return facts


def main():
    failures = []
    print("Running cognitive UX expert-system tests...\n")
    for _, row in TEST_CASES.iterrows():
        facts = row_to_facts(row)
        fired_rules, _ = run_forward_chaining(facts, RULES)
        actual_risk, score = calculate_overall_risk(fired_rules)
        expected_risk = row["Expected Risk"]
        fired_ids = ", ".join(rule["id"] for rule in fired_rules) or "None"
        print(f"{row['Test ID']} - {row['Scenario']}")
        print(f"  Expected risk: {expected_risk}")
        print(f"  Actual risk:   {actual_risk}")
        print(f"  Score:         {score}")
        print(f"  Fired rules:   {fired_ids}\n")
        if actual_risk != expected_risk:
            failures.append((row["Test ID"], expected_risk, actual_risk))

    if failures:
        raise AssertionError(f"Risk mismatches found: {failures}")
    print("All tests passed.")


if __name__ == "__main__":
    main()
