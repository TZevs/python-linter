# Python Linter
![license: MIT](https://img.shields.io/badge/license-MIT-success)

## About
A small Python command-line linter that checks for three common Python bugs in a file's syntax structure using the `ast` module.
<br><br>
Developed as part of a learning plan I am following to go back to the basics of Python and programming, in order to prepare for interviews and technical assessments. Best to go back to basics before moving onto more complex projects and new fields. 
<br>
_Learning plan created by Claude, **the code solution was not**, other than a few corrections and the test cases to identify bugs quicker._ 

### Rules
| Code | Finds | Example |
|---|---|---|
| GL001 | Mutable default argument (list, dict or set) in a function | `def f(items=[])` |
| GL002 | `is` or `is not` used in an expression with a literal | `if x is 5` |
| GL003 | Variable assignment that overwrites a built-in name. | `list = [1, 2]` |

### Design Decisions
1) Read the code's structure, not its text
- Parse the file with the `ast` module instead of searching the file's text.
- A text search cannot tell between `list = []` in the code from `list = []` inside a comment or string.
- Only works on valid Python.
2) Visitor Pattern, one method per rule
- `Linter` extends `ast.NodeVisitor`. Each rule has its own method: `visit_FunctionDef` (GL001), `visit_Compare` (GL002), `visit_Assign` (GL003).
- `visit(node)` starts the walk through the node's children, at each child it checks for a method `visit_` + the node type and calls it, if it exists, if not it carries on walking through the tree.
- A new rule is a new method, with no change to the others.
- _Trade-off_: 2 rules that need the same node type have to share one method.
3) 

- 
- Each method ends with `self.generic_visit(node)`. Without it, the visitor(Linter) would not look inside that node.
- Implemented the Visitor design pattern via the `ast` NodeVisitor class creating custom `visit_` methods, that run when the instance calls `.visit(tree)` calling the methods in order that the node types are found within the passed in node.
  - The `tree` node is the Module node, all nodes within are its children, if a function is written in the code first, then the `visit_FunctionDef` method is called first. At the end of the method `self.visit_generic(node)` is called to ensure that this function's children nodes are visited via the implemented methods before moving down the module structure.
  - Each rule has its own `visit_` method which aligns with the Visitor pattern, this independence will allow future rules to be easily appended.
  - `def __init__(self)` initialises the Linter instance and gives it a empty list, which will store the findings the linter flags.
- This program will run as a script as the file to be run is passed in via the 2nd command-line argument.
- A `Main()` function implemented so that the file argument can be verified before calling the `lint(source)` function to parse the file content as a `ast`, create a Linter instance, and have it call the `visit(tree)` method.
  - This is where the `ast` module comes in, because it cannot find a defined `visit` method it will automatically look for custom methods that are prefixed with `visit_` and use the suffix to match to node types. Such as `FunctionDef` in the first method. 

### Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<br>
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
<br>
![ast: Abstract Syntax Tree](https://img.shields.io/badge/ast-Abstract%20Syntax%20Tree-informational)

## Setup
### Installation
Needs python 3 or newer. 
```terminal
git clone https://github.com/TZevs/python-linter.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Usage
```terminal
python python_linter/linter.py <filepath>
```
> `<filepath>`: of the file you want the linter to check.

#### Run Tests
```terminal
pip install pytest
pytest
```
> If you have installed the dependencies from the installation command steps then Pytest will have already been installed.<br>
> Can specify which test file to run: `pytest tests/<test_file>`

## Testing
There are 36 tests all together, there are unit tests written for each of the linter rules. 
### Bugs
Results: 7 failed, 29 passed.<br>
The test cases that failed are the following:
| BugID | Rule | Test Name | Priority | Description | Resolved |
|---|---|---|---|---|---|
| 001 | GL001 | test_flags_mutable_default_args() | High | Should flag mutable default argument like `def f(x={1: 2})` | - |
| 002 | GL001 | test_flags_keyword_only_mutable_defaults() | Medium | Should flag keyword-only defaults like `def f(*, x=[])` | - |
| 003 | GL001 | test_flags_async_function_mutable_default() | Low | Should flag mutable default arguments in `async` functions | - |
| 004 | GL002 | test_chained_comparison_does_not_ flag_wrong_comparator() | Medium | Should not flag as there are multiple comparators and the one the `is` applies to is a variable like `if x is y < 5` | - |
| 005 | GL003 | test_flags_annotated_assignment() | Medium | Should flag annotated variable if name overwrites built-in syntax like `list: list = []` | - |
| 006 | GL003 | test_flags_augmented_assignment() | Medium | Should flag variable assigned with an augmented operator with a name that overwrites built-in syntax like `list += [1, 2]` | - |
| 007 | GL003 | test_flags_destructuring_assignment() | Medium | Should flag destructured variable assignment if name(s) overwrite built-in syntax like `list, number = [], 5` | - |

## Next Steps
- Resolve High priority bug, then the medium priority bugs.
- Implement visit method for `AsyncFunctionDef` to allow the linter to flag mutable default arguments in an `async` function. 

## References
[Python Docs: ast - Abstract syntax trees](https://docs.python.org/3/library/ast.html#node-classes)<br>
[Earthly: Introduction to Abstract Syntax Trees in Python](https://earthly.dev/blog/python-ast/#anatomy-of-an-ast-node)<br>
[Real Python: Defining Main Function in Python](https://realpython.com/python-main-function/)<br>
[Real Python: linter](https://realpython.com/ref/glossary/linter/)<br>
[DeepSource: Learn Python ASTs by building your own linter](https://deepsource.com/blog/python-asts-by-building-your-own-linter)<br>
[sdxpy: A Code Linter](https://third-bit.com/sdxpy/lint/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for more details.
