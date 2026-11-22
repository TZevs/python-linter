import ast
import sys
import builtins


class Linter(ast.NodeVisitor):
    def __init__(self):
        """
        Initialises a Linter instance, giving it an empty list.
        """
        self.findings = []

    def visit_FunctionDef(self, node):
        """
        GL001: Checks for functions with mutable default arguments.
        """
        defaults = node.args.defaults

        if any(isinstance(d, (ast.Dict, ast.Set, ast.List)) for d in defaults):
            self.findings.append((node.lineno, f"GL001 mutable default argument"))
        
        self.generic_visit(node)

    def visit_Compare(self, node):
        """
        GL002: Checks for 'is' comparison expressions with a variable and a literal.
        """
        uses_is = any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops)
        for comparator in node.comparators:
            if uses_is and isinstance(comparator, ast.Constant):
                if type(comparator.value) in (str, int, float, complex):
                    self.findings.append((node.lineno, f"GL002 'is' used with a literal"))

        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        GL003: Checks for variable names that match with builtin identifiers. 
        """
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in dir(builtins):
                self.findings.append((node.lineno, f"GL003 built-in name `{target.id}` overwritten"))

        self.generic_visit(node)

def lint(source):
    linter = Linter()
    tree = ast.parse(source)
    linter.visit(tree)

    return sorted(linter.findings)

def Main():
    if len(sys.argv) != 2:
        print("Usage: python linter.py <filepath>", file=sys.stderr)
        return 2
    
    path = sys.argv[1]
    try:
        with open(sys.argv[1], "r") as file:
            findings = lint(file.read())
    except FileNotFoundError as e:
        return e

    for line, message in findings:
        print(f"{path}:{line} - {message}")

if __name__ == "__main__":
    Main()
