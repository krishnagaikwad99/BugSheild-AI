
import ast
import subprocess
import sys
import tempfile
import os


def analyze_code(code):
    results = []

    # Check Python syntax
    try:
        ast.parse(code)
        results.append({
            "type": "Syntax",
            "severity": "Info",
            "message": "No syntax errors found."
        })
    except SyntaxError as error:
        results.append({
            "type": "Syntax",
            "severity": "High",
            "message": f"Line {error.lineno}: {error.msg}"
        })
        return results

    # Run Ruff on a temporary file
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        process = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--output-format", "json", temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        import json
        issues = json.loads(process.stdout or "[]")

        for issue in issues:
            results.append({
                "type": issue.get("code", "Code"),
                "severity": "Medium",
                "message": (
                    f"Line {issue.get('location', {}).get('row')}: "
                    f"{issue.get('message')}"
                )
            })

    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        results.append({
            "type": "Analyzer",
            "severity": "Warning",
            "message": "Static analysis could not finish."
        })
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    return results
