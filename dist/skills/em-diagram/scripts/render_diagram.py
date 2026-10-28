#!/usr/bin/env python3
"""Render a workflow specification; never execute its nodes or produce their outputs."""

import argparse
import html
from pathlib import Path

import yaml


def label(value):
    return html.escape(str(value), quote=True).replace("\n", " ").replace("|", "&#124;")


def render(workflow, contracts, roles):
    owners = {r["id"]: r["title"] for r in roles["roles"]}
    io = {c["node_id"]: c for c in contracts["contracts"]}
    ids = {n["id"]: f"n{i}" for i, n in enumerate(workflow["nodes"])}
    lines = ["# Candidate workflow specification", "", "Proposed process; domain requirements and human approval remain to be confirmed.", "", "```mermaid", "flowchart TD"]
    for node in workflow["nodes"]:
        contract = io[node["id"]]
        inputs = ", ".join(e["name"] for e in contract["inputs"]) or "None (confirm)"
        outputs = ", ".join(e["name"] for e in contract["outputs"]) or "None (confirm)"
        parts = [f'{node["id"]}: {node["title"]}',
                 f'Owner: {owners[node["owner_role"]]}', f'Inputs: {inputs}',
                 f'Outputs: {outputs}',
                 f'Evidence: {node["evidence_status"]}; approval: {node["approval_status"]}']
        lines.append(f'    {ids[node["id"]]}["' + "<br/>".join(label(p) for p in parts) + '"]')
    for edge in workflow["edges"]:
        lines.append(f'    {ids[edge["from"]]} -->|"{label(edge["condition"])}"| {ids[edge["to"]]}')
    lines.extend(["```", "", "Field types, required/unknown flags, output formats, and reviewers are specified in `io-contract.yaml`.", "Outputs named above describe the future process; ElicitMesh has not generated them.", ""])
    return "\n".join(lines)


def render_project(folder):
    folder = Path(folder)
    def load(name):
        return yaml.safe_load((folder / name).read_text(encoding="utf-8"))
    return render(load("workflow.yaml"), load("io-contract.yaml"), load("role-map.yaml"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        output = render_project(args.directory)
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        parser.exit(1, f"Cannot render diagram: {exc}\n")
    (args.directory / "workflow.md").write_text(output, encoding="utf-8")
    print(f"Rendered {args.directory / 'workflow.md'}")
