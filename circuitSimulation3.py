from pprint import pprint
import time

# Class used to store information for a wire
class Node(object):
    def __init__(self, i, o, c, v, ii, io):
        self.name = i
        self.children = c
        self.operator = o
        self.value = v
        self.is_input = ii
        self.is_output = io

    def set_value (self, v):
        self.value = v

    def set_input (self, ii):
        self.is_input = ii

    def set_output (self, io):
        self.is_output = io

    def __repr__(self):
        return str(self.name)+ " " + str(self.value)


# Take a line from the input file which represents a gate operation and returns a node that stores the gate
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

    curr_node = Node("wire_" + str(nodeIndex), nodeOperator, children, -1, False, False)
    print("creating ", "wire_" + str(nodeIndex))
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
            print ("creating ", name)
            objectDict[name] = Node(name, "leaf", [], -1, True, False)

        elif input.startswith("OUTPUT"):
            index = input.find(")")
            outputNodes.append("wire_" + str(input[7:index]))

        else:
            new_node = process_gate(input)
            if new_node.name in outputNodes:
                new_node.is_output = True
            objectDict[new_node.name] = new_node

# Helper function simulating the AND logic gate
def simulate_and(children):
    print ("running AND: ", children)
    for i in children:
        if objectDict[i].value == -1:
            calculate_value(i)

        if objectDict[i].value == 0:
            print (children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 0")
            return 0
        else:
            print (children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "not returning anything")


    print (children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 1")
    return 1

# Helper function simulating the OR logic gate
def simulate_or(children):
    print ("running OR: ", children)
    for i in children:
        if objectDict[i].value == -1:
            calculate_value(i)
        if objectDict[i].value == 1:
            print(children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 1")
            return 1

    print (children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 0")
    return 0

# Helper function simulating the NAND logic gate
def simulate_nand(children):
    print ("running NAND: ", children)

    if simulate_and(children) == 0:
        print(children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 1")
        return 1
    else:
        print(children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 0")
        return 0

# Helper function simulating the NOT logic gate
def simulate_not(children):
    print ("running NOT: ", children)

    if objectDict[children[0]].value == -1:
        calculate_value(children[0])
    if objectDict[children[0]].value == 0:
        print(children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 1")
        return 1
    else:
        print(children, objectDict[i].name, objectDict[i].operator, objectDict[i].value, "returning 0")
        return 0

# Recursive function that traverses a tree and calculate logic value for each node
def calculate_value(index):
    if objectDict[index].value != -1:
        print (objectDict[index].name, " value is: ", objectDict[index].value)
        return objectDict[index].value
    else:
        if objectDict[index].operator == "AND":
            val = simulate_and(objectDict[index].children)
            objectDict[index].set_value(int(val))
            return val
        elif objectDict[index].operator == "OR":
            val = simulate_or(objectDict[index].children)
            objectDict[index].set_value(int(val))
            return val
        elif objectDict[index].operator == "NAND":
            val = simulate_nand(objectDict[index].children)
            objectDict[index].set_value(int(val))
            return val
        elif objectDict[index].operator == "NOT":
            val = simulate_not(objectDict[index].children)
            objectDict[index].set_value(int(val))
            print ("setting value of ", index, " to ", val)
            return val


# Main function starts

# Step 1: get circuit file name, input file name and output file name from terminal
# Get circuit file name from command line
wantToInputCircuitFile = str(input("Do you want to input a circuit file? (type 1 for yes, 0 for no)\n"))
if wantToInputCircuitFile == "1":
    circuitFile = str(input ("Please input file name\n"))
    try:
        f = open(circuitFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting circuit file to default')
        circuitFile = "circuit.bench"
else :
    circuitFile = "circuit.bench"

wantToInputInputFile = str(input("Do you want to input a input file? (type 1 for yes, 0 for no)\n"))
if wantToInputInputFile == "1":
    inputFile = input ("Please input file name\n")
    try:
        f = open(inputFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting input file to default')
        inputFile = "input.txt"
else :
    inputFile = "input.txt"

wantToInputOutputFile = str(input("Do you want to input a output file? (type 1 for yes, 0 for no)\n"))
if wantToInputOutputFile == "1":
    outputFile = input ("Please input file name\n")
    try:
        f = open(outputFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting output file to default')
        outputFile = "output.txt"
else :
    outputFile = "output.txt"


# Step 2: read input file
file2 = open(inputFile, "r")
values = file2.readlines()

# Step 3: Construct trees, calculates circuit value and write answers into output file
f = open(outputFile, "w")
for line in values:
    print ("currently running: ", line, "\n")

    file1 = open(circuitFile, "r")
    input_file_values = file1.readlines()
    file1.close()
    objectDict = dict()
    construct_tree()
    strlength = len(line) - 1
    if line[strlength] == "\n":
        strlength = strlength - 1

    for i in objectDict:
        if objectDict[i].is_input:
            objectDict[i].set_value(int(line[strlength]))
            print (objectDict[i].name, " set value to ", int(line[strlength]))
            strlength = strlength-1


    pprint(objectDict)
    f.write ("Calculating values for input: ")
    f.write (line.strip())
    f.write ("  ")
    for i in objectDict:
        if objectDict[i].is_output:
            answer = str(calculate_value(i))
            f.write(str(objectDict[i].name))
            f.write (": ")
            f.write(answer)
            f.write ("   ")
            print("------------------", objectDict[i].name, " ", answer)
            pprint(objectDict)
            askToContinue = input("Press a key to continue")

    print ("\n\n\n")
    f.write("\n")

f.close()