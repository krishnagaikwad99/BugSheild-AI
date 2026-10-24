
import ast


def extract_features(code):
    tree = ast.parse(code)

    features = {
        "lines_of_code": len(code.splitlines()),
        "function_count": 0,
        "class_count": 0,
        "if_count": 0,
        "loop_count": 0,
        "exception_count": 0,
        "function_arguments": 0
    }

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            features["function_count"] += 1
            features["function_arguments"] += len(node.args.args)

        elif isinstance(node, ast.ClassDef):
            features["class_count"] += 1

        elif isinstance(node, ast.If):
            features["if_count"] += 1

        elif isinstance(node, (ast.For, ast.While)):
            features["loop_count"] += 1

        elif isinstance(node, ast.Try):
            features["exception_count"] += 1

    return features
