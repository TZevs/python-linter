def add_item(x, items=[]):
    items.append(x)
    return

def fixed_add_item(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return


x = 5
if x is 5:
    print("x is 5")

list = [1, 2, 3]

def print_hello(name: str) -> str:
    if name is "Natalie":
        print("Hello, Nat")
    else:
        print("Hello, ", name)