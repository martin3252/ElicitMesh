#!/usr/bin/env python3
"""Validate the structural invariants of a ElicitMesh artifact bundle.

This is not a professional, legal, engineering, or factual validator.
Requires PyYAML. Run: python scripts/validate_spec.py examples/legal-unfair-dismissal
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML is required: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

EVIDENCE = {"source_supported", "inferred", "unknown"}
APPROVAL = {"pending", "approved", "rejected", "needs_info"}
REVIEW = {"pending", "completed", "blocked"}
CHECKS = {"deterministic", "human_review", "llm_assisted"}
YAML_FILES = ("role-map.yaml", "workflow.yaml", "io-contract.yaml", "review-log.yaml", "quality-rules.yaml")
MARKDOWN_FILES = ("role-map.md", "sources.md", "workflow.md", "expert-questions.md", "sample-output.md", "acceptance-criteria.md")


def _nonblank(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _list(x: Any) -> list:
    return x if isinstance(x, list) else []


def _object(x: Any) -> dict:
    return x if isinstance(x, dict) else {}


def validate_project(folder: Path) -> list[str]:
    folder = Path(folder)
    errors: list[str] = []
    documents: dict[str, dict] = {}

    for name in YAML_FILES:
        path = folder / name
        if not path.is_file():
            errors.append(f"{name}: missing file")
            continue
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                errors.append(f"{name}: root must be a mapping")
                continue
            documents[name] = loaded
        except (yaml.YAMLError, UnicodeError) as exc:
            errors.append(f"{name}: cannot parse YAML: {exc}")

    for name in MARKDOWN_FILES:
        path = folder / name
        if not path.is_file():
            errors.append(f"{name}: missing file")
        elif not path.read_text(encoding="utf-8").strip():
            errors.append(f"{name}: empty file")

    # Continue wherever possible so users see all structural issues at once.
    role_doc = documents.get("role-map.yaml", {})
    project = _object(role_doc.get("project"))
    if not _nonblank(project.get("goal")):
        errors.append("role-map.yaml: project.goal must be nonempty")
    roles = role_doc.get("roles")
    if not isinstance(roles, list) or len(roles) < 2:
        errors.append("role-map.yaml: roles must contain at least two roles")
    role_ids: set[str] = set()
    for i, role in enumerate(_list(roles)):
        label = f"role-map.yaml: roles[{i}]"
        r = _object(role)
        role_id = r.get("id")
        if not _nonblank(role_id):
            errors.append(f"{label}.id must be a nonempty string")
        elif role_id in role_ids:
            errors.append(f"{label}.id duplicate '{role_id}'")
        else:
            role_ids.add(role_id)
        if not _nonblank(r.get("title")):
            errors.append(f"{label}.title must be a nonempty string")
        for key in ("expertise", "provides", "needs", "responsibilities", "can_approve"):
            if not isinstance(r.get(key), list):
                errors.append(f"{label}.{key} must be a list (can be empty)")

    def check_state(record: dict, label: str) -> None:
        ev = record.get("evidence_status")
        ap = record.get("approval_status")
        if ev not in EVIDENCE:
            errors.append(f"{label}.evidence_status must be one of {sorted(EVIDENCE)}")
        if ap not in APPROVAL:
            errors.append(f"{label}.approval_status must be one of {sorted(APPROVAL)}")
        refs = record.get("source_refs", [])
        if not isinstance(refs, list):
            errors.append(f"{label}.source_refs must be a list")
            refs = []
        if ev == "source_supported" and not refs:
            errors.append(f"{label}: source_supported must include source_refs")
        if ap == "approved":
            if not _nonblank(record.get("approved_by")):
                errors.append(f"{label}: approved requires approved_by")
            if not record.get("approved_at"):
                errors.append(f"{label}: approved requires approved_at")

    wf = documents.get("workflow.yaml", {})
    nodes = wf.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append("workflow.yaml: nodes must be a nonempty list")
    node_ids: set[str] = set()
    for i, item in enumerate(_list(nodes)):
        label = f"workflow.yaml: nodes[{i}]"
        node = _object(item)
        nid = node.get("id")
        if not _nonblank(nid):
            errors.append(f"{label}.id must be a nonempty string")
        elif nid in node_ids:
            errors.append(f"{label}.id duplicate '{nid}'")
        else:
            node_ids.add(nid)
        if not _nonblank(node.get("title")):
            errors.append(f"{label}.title must be a nonempty string")
        if node.get("owner_role") not in role_ids:
            errors.append(f"{label}.owner_role must refer to a declared role")
        check_state(node, label)
    edges = wf.get("edges")
    if not isinstance(edges, list):
        errors.append("workflow.yaml: edges must be a list")
    for i, item in enumerate(_list(edges)):
        label = f"workflow.yaml: edges[{i}]"
        edge = _object(item)
        for key in ("from", "to"):
            if edge.get(key) not in node_ids:
                errors.append(f"{label}.{key} must refer to a declared node")
        if not _nonblank(edge.get("condition")):
            errors.append(f"{label}.condition must be a nonempty string")
        check_state(edge, label)

    contract_doc = documents.get("io-contract.yaml", {})
    contracts = contract_doc.get("contracts")
    if not isinstance(contracts, list):
        errors.append("io-contract.yaml: contracts must be a list")
    seen_contracts: set[str] = set()
    for i, item in enumerate(_list(contracts)):
        label = f"io-contract.yaml: contracts[{i}]"
        contract = _object(item)
        node_id = contract.get("node_id")
        if node_id not in node_ids:
            errors.append(f"{label}.node_id must refer to a workflow node")
        elif node_id in seen_contracts:
            errors.append(f"{label}.node_id duplicate '{node_id}'")
        else:
            seen_contracts.add(node_id)
        for direction in ("inputs", "outputs"):
            entries = contract.get(direction)
            if not isinstance(entries, list):
                errors.append(f"{label}.{direction} must be a list")
                continue
            names: set[str] = set()
            for j, e in enumerate(entries):
                item_label = f"{label}.{direction}[{j}]"
                entry = _object(e)
                if not _nonblank(entry.get("name")):
                    errors.append(f"{item_label}.name must be a nonempty string")
                elif entry["name"] in names:
                    errors.append(f"{item_label}.name duplicate '{entry['name']}'")
                else:
                    names.add(entry["name"])
                check_state(entry, item_label)
                if entry.get("approver_role") not in role_ids:
                    errors.append(f"{item_label}.approver_role must refer to a declared role")
                if direction == "inputs":
                    if entry.get("required") not in (True, False, "unknown"):
                        errors.append(f"{item_label}.required must be true, false or unknown")
                    if not _nonblank(entry.get("type")):
                        errors.append(f"{item_label}.type must be a nonempty string")
                else:
                    if not _nonblank(entry.get("format")):
                        errors.append(f"{item_label}.format must be a nonempty string")
                    if not isinstance(entry.get("quality_criteria"), list):
                        errors.append(f"{item_label}.quality_criteria must be a list")
    for missing in node_ids - seen_contracts:
        errors.append(f"io-contract.yaml: node '{missing}' has no I/O contract")

    review_doc = documents.get("review-log.yaml", {})
    reviews = review_doc.get("reviews")
    if not isinstance(reviews, list):
        errors.append("review-log.yaml: reviews must be a list")
    review_ids: set[str] = set()
    completed_reviews: set[str] = set()
    for i, item in enumerate(_list(reviews)):
        label = f"review-log.yaml: reviews[{i}]"
        review = _object(item)
        rid = review.get("id")
        if not _nonblank(rid):
            errors.append(f"{label}.id must be nonempty")
        elif rid in review_ids:
            errors.append(f"{label}.id duplicate '{rid}'")
        else:
            review_ids.add(rid)
        if review.get("reviewer_role") not in role_ids:
            errors.append(f"{label}.reviewer_role must refer to a declared role")
        if review.get("status") not in REVIEW:
            errors.append(f"{label}.status must be {sorted(REVIEW)}")
        if not isinstance(review.get("feedback"), list):
            errors.append(f"{label}.feedback must be a list")
        if review.get("status") == "completed":
            if not _nonblank(review.get("reviewer_identity")) or not review.get("received_at"):
                errors.append(f"{label}: completed review requires reviewer_identity and received_at")
            elif _nonblank(rid):
                completed_reviews.add(rid)

    rule_doc = documents.get("quality-rules.yaml", {})
    rules = rule_doc.get("rules")
    if not isinstance(rules, list):
        errors.append("quality-rules.yaml: rules must be a list")
    rule_ids: set[str] = set()
    for i, item in enumerate(_list(rules)):
        label = f"quality-rules.yaml: rules[{i}]"
        rule = _object(item)
        rid = rule.get("id")
        if not _nonblank(rid):
            errors.append(f"{label}.id must be nonempty")
        elif rid in rule_ids:
            errors.append(f"{label}.id duplicate '{rid}'")
        else:
            rule_ids.add(rid)
        if not _nonblank(rule.get("statement")) or not _nonblank(rule.get("scope")):
            errors.append(f"{label}: statement and scope must be nonempty")
        if rule.get("approver_role") not in role_ids:
            errors.append(f"{label}.approver_role must refer to a declared role")
        if rule.get("check_type") not in CHECKS:
            errors.append(f"{label}.check_type must be {sorted(CHECKS)}")
        if not _nonblank(rule.get("test_case")):
            errors.append(f"{label}.test_case must be nonempty")
        check_state(rule, label)
        if rule.get("originating_feedback") and rule["originating_feedback"] not in review_ids:
            errors.append(f"{label}.originating_feedback must refer to a declared review id")
        if rule.get("approval_status") == "approved":
            if not rule.get("originating_feedback") and not _list(rule.get("source_refs")):
                errors.append(f"{label}: approved rule requires originating_feedback or source_refs")
            if rule.get("originating_feedback") and rule["originating_feedback"] not in completed_reviews:
                errors.append(f"{label}: approved feedback-based rule requires a completed review with identified reviewer")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Folder containing ElicitMesh artifacts")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation summary")
    args = parser.parse_args()
    problems = validate_project(args.directory)
    if args.json:
        print(json.dumps({"valid": not problems, "errors": problems}, indent=2))
    else:
        print(f"ElicitMesh structural validation: {'PASS' if not problems else 'FAIL'}")
        print(f"Directory: {args.directory}")
        if problems:
            for issue in problems:
                print(f"  - {issue}")
        else:
            print("No structural problems found. Domain facts and approvals remain unverified by this script.")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
