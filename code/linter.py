import ast
import sys

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

        if any(defaults) == dict or set or list:
            print(f"FLAGGED: `{node.name}` using mutuable default argument.")
        
        self.generic_visit(node)      

Linter().visit(tree)
