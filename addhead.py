import ast

def generate_docstrings(source_code):
    tree = ast.parse(source_code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not any(isinstance(sub_node, ast.Str) for sub_node in node.body):
                yield node.lineno, f"""
    \"\"\"{node.name} docstring.

    Parameters:
    -----------
    {', '.join([arg.arg + ' : TYPE' for arg in node.args.args])}

    Returns:
    --------
    TYPE
        Description of return value.

    \"\"\"
    """

def add_docstrings_to_code(source_code):
    docstrings = list(generate_docstrings(source_code))
    if not docstrings:
        return source_code

    lines = source_code.splitlines()
    for lineno, docstring in reversed(docstrings):
        for index, line in enumerate(docstring.splitlines()):
            lines.insert(lineno + index, line)
    return '\n'.join(lines)

if __name__ == "__main__":
    with open('zip.py', 'r') as f:
        source_code = f.read()
    
    updated_code = add_docstrings_to_code(source_code)
    
    with open('your_script_with_docstrings.py', 'w') as f:
        f.write(updated_code)

