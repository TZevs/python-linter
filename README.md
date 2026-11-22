# Python Linter
![license: MIT](https://img.shields.io/badge/license-MIT-success)

## About
A small Python command-line linter that checks for three common Python bugs in a file's syntax structure using the `ast` module.

### Rules
| Code | Finds | Example |
|---|---|---|
| GL001 | Mutable default argument (list, dict or set) in a function | `def f(items=[])` |
| GL002 | `is` or `is not` used in an expression with a literal | `if x is 5` |
| GL003 | Variable assignment that overwrites a built-in name. | `list = [1, 2]` |

### Design Decisions
- Use of a **Syntax tree** instead of a text search. A text search would not be able to tell the different between `list = []` in code and a `list = []` inside a string or a comment. The `ast` module provides the real structure of the code, including attributes, data types, etc.
- 

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
python linter.py <filepath>
```
> `<filepath>`: of the file you want the linter to check.

#### Run Tests
```terminal
pip install pytest
pytest
```
> If you have installed the dependencies from the installation command steps then Pytest will have already been installed.

## Known Issues & Improvements to be Made
### Bugs


### Next Steps


## References



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for more details.
