import ast
import sys
import builtins

content = ""

try:
    with open(sys.argv[1], mode="r") as file:
        content = file.read()
except FileNotFoundError as e:
    print("FILE DOES NOT EXIST")
     
# Parse code into an AST
tree = ast.parse(content)
# Print the AST
#print(ast.dump(tree, indent=4))


class Linter(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        defaults = node.args.defaults

        if len(defaults) == 0:
            self.generic_visit(node)
            return

        if any(isinstance(default, (ast.Dict, ast.Set, ast.List)) for default in defaults):
            print(f"Line: {node.lineno}. Mutable default argument.")
        
        self.generic_visit(node)

    def visit_Compare(self, node):
        is_comparator = False

        if any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant):
                    if type(comparator.value) in (str, int, float, complex):
                        is_comparator = True

        if is_comparator:
            print(f"Line: {node.lineno}. Incorrect identity comparison.")

    def visit_Assign(self, node):
        for name in node.targets:
            if name.id in dir(builtins):
                print(f"Line: {node.lineno}. Variable name matches builtin name, `{name.id}`.")

    
Linter().visit(tree)
