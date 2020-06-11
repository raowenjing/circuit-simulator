import sys

# maximum number of wires, including both input, output and intermediate wires
MAX_LINES = 10000

# data structure used to store information for a wire
class Node(object):
    def __init__(self, index, operator, childs):
        self.index = index
        self.children = childs
        self.operator = operator

# takes a line of a gate operation and returns a node that stores the data
def process_gate(str):
    #result wire, operation, input wires
    index = str.find(" = ")
    nodeIndex = int(str[0:index])
    nodeOperator = 4
    if str.find("NAND") != -1:
        nodeOperator = 2
    elif str.find("OR") != -1:
        nodeOperator = 1
    elif str.find("AND") != -1:
        nodeOperator = 0
    elif str.find("NOT") != -1:
        nodeOperator = 3
    else:
        print("Invalid Operator")

    children = []
    index = str.find("(") + 1
    endvalue = str.find(")")

    while index < endvalue:
        indexen = str.find(",", index)
        if indexen == -1:
            children.append(int(str[index:endvalue]))
            break
        children.append(int(str[index:indexen]))
        index = indexen + 1

    curr_node = Node(nodeIndex, nodeOperator, children)
    return curr_node

# creates trees from input file, stores all the input wires and output wires in a list,
# creates new node for each gate operation
def construct_tree():
    for input in inputlist:
        if input == "\n":
            continue

        if input.startswith("#"):
            continue

        if input.startswith("INPUT"):
            index = input.find(")")
            intValue = int(input[6:index])
            inputList.append(intValue)
            pointer_list[intValue] = Node(intValue, "leaf", [])

        elif input.startswith("OUTPUT"):
            index = input.find(")")
            outputList.append(int(input[7:index]))

        else:
            new_node = process_gate(input)
            pointer_list[new_node.index] = new_node

# prints out the constructed trees
def test_tree():
    for i in outputList:
        print(i)

    for i in pointer_list:
        if i != 0:
            print(i.index, i.children, i.operator)
            print()

# simulates the AND gate for a list of children
def simulate_and(children):
    for i in children:

        if value_list[i] == -1:
            calculate_value(i)

        if value_list[i] == 0:
            return 0

    return 1

# simulates the OR gate for a list of children
def simulate_or(children):
    for i in children:
        if value_list[i] == -1:
            calculate_value(i)
        if value_list[i] == 1:
            return 1
    return 0

# simulates the NAND gate for a list of children
def simulate_nand(children):
    if simulate_and(children) == 0:
        return 1
    else:
        return 0

# simulates the NOT gate for a child wire
def simulate_not(children):
    if value_list[children[0]] == -1:
        calculate_value(children[0])
    if value_list[children[0]] == 0:
        return 1
    else:
        return 0

# recursive function that traverses trees
def calculate_value(index):
    if value_list[index] != -1:
        return value_list[index]
    else:
        if pointer_list[index].operator == 0:
            val = simulate_and(pointer_list[index].children)
            value_list[index] = val
            return val
        elif pointer_list[index].operator == 1:
            val = simulate_or(pointer_list[index].children)
            value_list[index] = val
            return val
        elif pointer_list[index].operator == 2:
            val = simulate_nand(pointer_list[index].children)
            value_list[index] = val
            return val
        elif pointer_list[index].operator == 3:
            val = simulate_not(pointer_list[index].children)
            value_list[index] = val
            return val

# main function starts
# get input from command line
if len(sys.argv) != 5:
    print("USAGE: python circuitSimulations.py  CIRCUIT_FILE  INPUT_FILE  OUTPUT_FILE  MAX_LINES")
    print (len(sys.argv))
    exit()
circuitFile = sys.argv[1]
inputFile = sys.argv[2]
outputFile = sys.argv[3]
MAX_LINES = int(sys.argv[4])

# Step 1: read circuit file and construct tree
file1 = open(circuitFile,"r")
inputlist = file1.readlines()
file1.close()
pointer_list = [0] * MAX_LINES
outputList = []
inputList = []
construct_tree()
#test_tree()


# Step 2: read input file
file2 = open(inputFile, "r")
values = file2.readlines()

# Step 3: traverses tree, calculates circuit value and write answers into file
f = open(outputFile, "w")
for line in values:
    value_list = [-1] * MAX_LINES
    strlength = 0
    for i in range(len(inputList)-1, -1, -1):
        value_list[inputList[i]] = int(line[strlength])
        strlength = strlength + 1

    for i in outputList:
        f.write(str(calculate_value(i)))

    f.write("\n")

f.close()