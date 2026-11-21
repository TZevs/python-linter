def add_item(x, items=[]):
    items.append(x)
    return

def fixed_add_item(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return


x = 5
y = 6
if x is 5:
    print("x is 5")

if x is 5 and y is 6:
    print("x is 5 and y is 6")

list = [1, 2, 3]
my_list = [4, 5, 6]

def print_hello(name: str) -> str:
    if name is "Natalie":
        print("Hello, Nat")
    else:
        print("Hello, ", name)

a = [4, 5, 6]
b = a
if a is b:
    print("Same object")

