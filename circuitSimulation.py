# Class used to store information for a wire
class Node(object):
    def __init__(self, i, v, op, c, ii, io):
        self.name = i
        self.value = v
        self.operator = op
        self.children = c
        self.is_input = ii
        self.is_output = io

    def set_value (self, v):
        self.value = v

    def set_children(self, c):
        self.children = c

    def set_operator (self, op):
        self.operator = op

    def set_input (self, ii):
        self.is_input = ii

    def set_output (self, io):
        self.is_output = io

    def __repr__(self):
        return str(self.name)+ " " + str(self.value)


# Take a line from the circuit file which represents a gate operation and returns a node that stores the gate
def process_gate(strVal):
    #result wire, operation, input wires
    index = strVal.find(" = ")
    nodeIndex = str(strVal[0:index])
    nodeOperator = 4
    if strVal.find("NAND") != -1:
        nodeOperator = "NAND"
    elif strVal.find("OR") != -1:
        nodeOperator = "OR"
    elif strVal.find("AND") != -1:
        nodeOperator = "AND"
    elif strVal.find("NOT") != -1:
        nodeOperator = "NOT"
    else:
        print("Invalid Operator")

    # store children in list
    children = []
    index = strVal.find("(") + 1
    endvalue = strVal.find(")")

    while index < endvalue:
        indexen = strVal.find(",", index)
        if indexen == -1:
            children.append("wire_" + str(strVal[index:endvalue].strip()))
            break
        children.append("wire_"+str(strVal[index:indexen].strip()))
        index = indexen + 1

    curr_node = Node("wire_" + str(nodeIndex), -1, nodeOperator, children, False, False)
    #print("creating ", "wire_" + str(nodeIndex))
    return curr_node

# Create trees from input file, store all the input wires and output wires in a list
# Creates a new node for each gate operation
def construct_tree():
    outputNodes = []
    for input in input_file_values:
        if input == "\n":
            continue

        if input.startswith("#"):
            continue

        if input.startswith("INPUT"):
            index = input.find(")")
            intValue = str(input[6:index])
            name = "wire_" + str(intValue)
            print ("creating input node ", name)
            node_list.append(Node(name, "leaf", -1, [], True, False))
            list_for_index.append(name)

        elif input.startswith("OUTPUT"):
            index = input.find(")")
            name = "wire_" + str(input[7:index])
            outputNodes.append(name)
            node_list.append(Node(name, "output", -1, [], False, True))
            list_for_index.append(name)

        else:
            new_node = process_gate(input)
            if str(new_node.name) in outputNodes:
                index = list_for_index.index(new_node.name)
                node_list[index].set_children(new_node.children)
                node_list[index].set_operator(new_node.operator)
            else:
                print ("creating node ", new_node.name)
                node_list.append(new_node)
                list_for_index.append(new_node.name)

    # Convert the children from a list of names to a list of references
    for i in node_list:
        for j in range(len(i.children)):
            name = i.children[j]
            listIndex = list_for_index.index(name)
            i.children[j] = node_list[listIndex]


# Helper function simulating the AND logic gate
def simulate_and(children):
    for i in children:
        if i.value == 0:
            return 0
    return 1

# Helper function simulating the OR logic gate
def simulate_or(children):
    for i in children:
        if i.value == 1:
            return 1
    return 0

# Helper function simulating the NAND logic gate
def simulate_nand(children):
    if simulate_and(children) == 0:
        return 1
    else:
        return 0

# Helper function simulating the NOT logic gate
def simulate_not(children):
    if children[0].value == 0:
        return 1
    else:
        return 0

def simulate_nor(children):
    if simulate_or(children) == 0:
        return 1
    else:
        return 0

def simulate_xor(children):
    numberOf1 = 0
    for i in children:
        if children.value == 1:
            numberOf1 = numberOf1 + 1
    if numberOf1 == 1:
        return 1
    else:
        return 0

def simulate_xnor(children):
    if simulate_xor(children) == 0:
        return 1
    else:
        return 0

# Function that calculates value of the node based on its children
def calculate_value(node):
    for i in node.children:
        if i.value == -1:
            return -1

    if node.operator == "AND":
        val = simulate_and(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "OR":
        val = simulate_or(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "NAND":
        val = simulate_nand(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "NOT":
        val = simulate_not(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "XOR":
        val = simulate_xor(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "XNOR":
        val = simulate_xnor(node.children)
        node.set_value(int(val))
        return val
    elif node.operator == "NOR":
        val = simulate_nor(node.children)
        node.set_value(int(val))
        return val

# Helper function to clear values in tree
def clear_values():
    for i in node_list:
        i.set_value(-1)


# Main function starts

# Step 1: get circuit file name from command line
wantToInputCircuitFile = str(input("The default circuit bench file is circuit.bench, type 1 to change the file.\n"))
if wantToInputCircuitFile == "1":
    circuitFile = str(input ("Please input file name\n"))
    try:
        f = open(circuitFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting circuit file to default')
        circuitFile = "circuit.bench"
else:
    circuitFile = "circuit.bench"

# Constructing the circuit tree
file1 = open(circuitFile, "r")
input_file_values = file1.readlines()
file1.close()
node_list = []
list_for_index = []
construct_tree()

line = input("please input a value (return to exit):")

while len(line) != 0:
    clear_values()
    print ("currently running: ", line.strip())

    strlength = len(line) - 1
    if line[strlength] == "\n":
        strlength = strlength - 1

    # Set value of input node
    for i in node_list:
        if i.is_input:
            i.set_value(int(line[strlength]))
            print (i.name, " set value to ", int(line[strlength]))
            strlength = strlength-1

    # Compute value of the gate nodes
    complete = False
    while complete == False:
        complete = True
        for i in node_list:
            val = calculate_value(i)
            if val == -1:
                complete = False

    # Print the value of the output nodes
    for i in node_list:
        if i.is_output:
            print(i.name, " ", i.value)

    print ("\n")
    line = input("please input a value (return to exit): ")