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
print(ast.dump(tree, indent=4))


