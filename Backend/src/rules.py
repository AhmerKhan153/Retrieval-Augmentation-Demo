# src/rules.py
import json
import os

RULES_FILE = "data/domain_rules.json"

def load_domain_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def match_rule(query, rules):
    query_lower = query.lower()
    for rule in rules:
        if all(word in query_lower for word in rule["keywords"]):
            return rule["response"]
    return None