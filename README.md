# Python Linter
![license: MIT](https://img.shields.io/badge/license-MIT-success)

## About
A small Python command-line linter that checks for three common Python bugs in a file's syntax structure using the `ast` module.
<br><br>
Developed as part of a learning plan I am following to go back to the basics of Python and programming, in order to prepare for interviews and technical assessments. Best to go back to basics before moving onto more complex projects and new fields. 
<br>
_Learning plan created by Claude, **the code solution was not**, other than a few corrections and the test cases to identify bugs quicker._ 

### Demo
```python
(venv) python-linter % python3 python_linter/linter.py examples/bad_example_2.py
```
The Output: <br>
<img width="768" height="58" alt="Screenshot 2026-11-22 at 19 32 16 copy" src="https://github.com/user-attachments/assets/c88e7e7d-0721-4031-beb4-60fd8ce41d7f" /><br>

The Code:<br>
<img width="286" height="238" alt="Screenshot 2026-11-22 at 19 32 35" src="https://github.com/user-attachments/assets/200508bc-b6ad-475f-a3c8-a0103a863b3e" /><br>

### Rules
| Code | Finds | Example |
|---|---|---|
| GL001 | Mutable default argument (list, dict or set) in a function | `def f(items=[])` |
| GL002 | `is` or `is not` used in an expression with a literal | `if x is 5` |
| GL003 | Variable assignment that overwrites a built-in name. | `list = [1, 2]` |

### Design Decisions
##### 1) A command-line script
- Run as `python python_linter/linter.py <filepath>`, as a standalone Python script using `ast`.
- Quick and easy to implement with high maintainability for adding future rules.
- _Trade-of_: Possible slow execution with larger files. 
##### 2) Read the code's structure, not its text
- Parse the file with the `ast` module instead of searching the file's text.
- A text search cannot tell between `list = []` in the code from `list = []` inside a comment or string.
- _Trade-of_: Only works on valid Python.
##### 3) Visitor Pattern, one method per rule
- `Linter` extends `ast.NodeVisitor`. Each rule has its own method: `visit_FunctionDef` (GL001), `visit_Compare` (GL002), `visit_Assign` (GL003).
- `visit(node)` starts the walk through the node's children, at each child it checks for a method `visit_` + the node type and calls it, if it exists, if not it carries on walking through the tree.
- A new rule is a new method, with no change to the others.
- _Trade-off_: 2 rules that need the same node type have to share one method.
##### 3) Collect findings in a list, don't print them
- `Linter.__init__` creates an empty list. Each rule adds `(line, message)` to it, or nothing is nothings flagged.
- Tests can check the list directly. The output format can change without affecting any rules.
- _Trade-off_: Slightly more code than printing straight away.
##### 4) Keep logic separate from file reading and findings printing
- `Linter` stores findings as `(line, message)` in a list. `lint(source)` takes the text of a file, parses it and returns that list. `Main()` checks the command-line arguments, reads the file and prints the findings.
- Tests can pass a string straight to `lint` and check the result, with no files or printed output. The output format or the way files are read can change without affecting any rules.
- _Trade-off_: an extra layer for a small script. `lint` does not know the file name, so `Main()` adds it. 

---
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
