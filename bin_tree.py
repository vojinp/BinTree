OPERATIONS = {"+": 1, "-": 1, "*": 0, "/": 0}
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"
eval = {"+": (lambda x, y: x + y), "-": (lambda x, y: x - y), "*": (lambda x, y: x * y), "/": (lambda x, y: x / y)}


class Node:
    def __init__(self, value):
        self.value = value


class Operator(Node):
    def __init__(self, value):
        super().__init__(value)


class Operation(Node):
    def __init__(self, value, right_child=None, left_child=None):
        super().__init__(value)
        self.right_child = right_child
        self.left_child = left_child


class LeftBracket():
    pass


class RightBracket():
    pass


expression = "2 * ( 2 + 2 * ( 3 + 3 ) )"

nodes = list(map(lambda x: LeftBracket() if x == LEFT_BRACKET else RightBracket() if x == RIGHT_BRACKET else Operation(
    x) if x in OPERATIONS.keys() else Operator(x), expression.split()))


def parse(list, prio):
    new_list = []
    skip = False
    for idx, node in enumerate(list):
        if skip:
            skip = False
            continue
        if isinstance(node, Operation) and OPERATIONS[node.value] == prio:
            node.left_child = new_list[-1]
            node.right_child = list[idx + 1]
            del new_list[-1]
            skip = True
        new_list.append(node)
    return new_list


def find_brackets(list, index):
    for i, node in enumerate(list):
        if i < index:
            continue
        if (isinstance(node, LeftBracket)):
            j = i + 1
            while True:
                if isinstance(list[j], RightBracket):
                    new_list = parse(list[i + 1: j], 0)
                    new_list = parse(new_list, 1)
                    res_list = list[:]
                    del res_list[i: j]
                    res_list[i] = new_list[0]
                    return res_list
                if isinstance(list[j], LeftBracket):
                    return find_brackets(list, j)
                j += 1
    return list


while True:
    new_nodes = find_brackets(nodes, 0)
    if len(new_nodes) == len(nodes):
        break
    else:
        nodes = new_nodes


def evaluate(operation, operator1, operator2):
    return eval[operation.value](float(operator1.value), float(operator2.value))


def parse_tree(root):
    if isinstance(root, Operator):
        return root
    return Operator(evaluate(root, parse_tree(root.left_child), parse_tree(root.right_child)))


nodes = parse(nodes, 0)
nodes = parse(nodes, 1)

print(nodes)
res = parse_tree(nodes[0])
print(res.value)
