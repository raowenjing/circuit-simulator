# Class used to store information for a wire
class Node(object):
    def __init__(self, name, value, gatetype, innames):
        self.name = name  # string
        self.value = value  # char: '0', '1', 'U' for unknown
        self.gatetype = gatetype  # string such as "AND", "OR" etc
        self.interms = []  # list of nodes (first as strings, then as nodes), each is a input wire to the gatetype
        self.innames = innames  # helper string to temperarily store the interms' names, useful to find all the interms nodes and link them
        self.is_input = False  # boolean: true if this wire is a primary input of the circuit
        self.is_output = False  # boolean: true if this wire is a primary output of the circuit

    def set_value(self, v):
        self.value = v

    def display(self):  # print out the node nicely on one line

        if self.is_input:
            # nodeinfo = f"input:\t{str(self.name[4:]):5} = {self.value:^4}"
            nodeinfo = f"input:\t{str(self.name):5} = {self.value:^4}"
            print(nodeinfo)
            return
        elif self.is_output:
            nodeinfo = f"output:\t{str(self.name):5} = {self.value:^4}"
        else:  # internal nodes
            nodeinfo = f"wire:  \t{str(self.name):5} = {self.value:^4}"

        interm_str = " "
        interm_val_str = " "
        for i in self.interms:
            interm_str += str(i.name) + " "
            interm_val_str += str(i.value) + " "

        nodeinfo += f"as {self.gatetype:>5}"
        nodeinfo += f"  of   {interm_str:20} = {interm_val_str:20}"

        print(nodeinfo)
        return

        # calculates the value of a node based on its gate type and values at interms

    def calculate_value(self):

        for i in self.interms:  # skip calculating unless all interms have specific values 1 or 0
            if i.value != "0" and i.value != "1":
                return "U"

        if self.gatetype == "AND":
            val = "1"
            for i in self.interms:
                if i.value == "0":
                    val = "0"
            self.value = val
            return val
        elif self.gatetype == "OR":
            val = "0"
            for i in self.interms:
                if i.value == '1':
                    val = "1"
            self.value = val
            return val
        elif self.gatetype == "NAND":
            flag = "1"
            for i in self.interms:
                if i.value == "0":
                    flag = "0"
            val = str(1 - int(flag))
            self.value = val
            return val
        elif self.gatetype == "NOT":
            val = self.interms[0].value
            self.value = str(1 - int(val))
            return val
        elif self.gatetype == "XOR":
            num_of_1 = 0
            for i in self.interms:
                if i.value == "1":
                    num_of_1 = num_of_1 + 1
            val = num_of_1 % 2
            val = str(val)
            self.value = val
            return val
        elif self.gatetype == "XNOR":
            num_of_1 = 0
            for i in self.interms:
                if i.value == "1":
                    num_of_1 = num_of_1 + 1
            val = num_of_1 % 2
            self.value = str(1 - val)
            return val
        elif self.gatetype == "NOR":
            flag = "0"
            for i in self.interms:
                if i.value == "1":
                    flag = "1"
            val = str(1 - int(flag))
            self.value = val
            return val
        elif self.gatetype == "BUFF":
            val = self.interms[0].value
            self.value = val
            return val


# Take a line from the circuit file which represents a gatetype operation and returns a node that stores the gatetype

def parse_gate(rawline):
    # example rawline is: a' = NAND(b', 256, c')

    # should return: node_name = a',  node_gatetype = NAND,  node_innames = [b', 256, c']

    # get rid of all spaces
    line = rawline.replace(" ", "")
    # now line = a'=NAND(b',256,c')

    name_end_idx = line.find("=")
    node_name = line[0:name_end_idx]
    # now node_name = a'

    gt_start_idx = line.find("=") + 1
    gt_end_idx = line.find("(")
    node_gatetype = line[gt_start_idx:gt_end_idx]
    # now node_gatetype = NAND

    # get the string of interms between ( ) to build tp_list
    interm_start_idx = line.find("(") + 1
    end_position = line.find(")")
    temp_str = line[interm_start_idx:end_position]
    tp_list = temp_str.split(",")
    # now tp_list = [b', 256, c]

    node_innames = [i for i in tp_list]
    # now node_innames = [b', 256, c]

    return node_name, node_gatetype, node_innames


# Create circuit node list from input file
def construct_nodelist():
    o_name_list = []

    for line in input_file_values:
        if line == "\n":
            continue

        if line.startswith("#"):
            continue

        # TODO: clean this up
        if line.startswith("INPUT"):
            index = line.find(")")
            # intValue = str(line[6:index])
            name = str(line[6:index])
            n = Node(name, "U", "PI", [])
            n.is_input = True
            node_list.append(n)


        elif line.startswith("OUTPUT"):
            index = line.find(")")
            name = line[7:index]
            o_name_list.append(name)


        else:  # majority of internal gates processed here
            node_name, node_gatetype, node_innames = parse_gate(line)
            n = Node(node_name, "U", node_gatetype, node_innames)
            node_list.append(n)

    # now mark all the gates that are output as is_output
    for n in node_list:
        if n.name in o_name_list:
            n.is_output = True

    # link the interm nodes from parsing the list of node names (string)
    # example: a = AND (b, c, d)
    # thus a.innames = [b, c, d]
    # node = a, want to search the entire node_list for b, c, d
    for node in node_list:
        for cur_name in node.innames:
            for target_node in node_list:
                if target_node.name == cur_name:
                    node.interms.append(target_node)

    return

# orders the node in the best simulation order
def order_nodelist():
    templist = node_list.copy()
    node_list.clear()

    # add all input
    for i in templist:
        if i.is_input:
            node_list.append(i)

    for i in node_list:
        templist.remove(i)

    while len(templist) > 0:
        firstnode = templist[0]
        templist.remove(firstnode)
        flag = True
        for i in firstnode.interms:
            if i not in node_list:
                flag = False

        if not flag:
            templist.append(firstnode)
        else:
            node_list.append(firstnode)

# Main function starts

# Step 1: get circuit file name from command line
wantToInputCircuitFile = str(
    input("Provide a benchfile name (return to accept circuit.bench by default):\n"))

if len(wantToInputCircuitFile) != 0:
    circuitFile = wantToInputCircuitFile
    try:
        f = open(circuitFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting circuit file to default')
        circuitFile = "circuit.bench"
else:
    circuitFile = "circuit.bench"

# Constructing the circuit netlist
file1 = open(circuitFile, "r")
input_file_values = file1.readlines()
file1.close()
node_list = []
output_list = []
construct_nodelist()
for i in node_list:
    if i.is_output:
        output_list.append(i)
order_nodelist()
# printing list of constructed nodes
for n in node_list:
    n.display()

print("---------------")

while True:
    line_of_val = input("Start simulation with input values (return to exit):\n")
    if len(line_of_val) == 0:
        break
    # Clear all nodes values to U in between simulation runs
    for node in node_list:
        node.set_value("U")

    strindex = 0
    # Set value of input node
    for node in node_list:
        if node.is_input:
            print (node.name)
            if strindex > len(line_of_val) - 1:
                break
            node.set_value(line_of_val[strindex])
            strindex = strindex + 1

    print("simulating with the following input values:")

    for node in node_list:
        if node.is_input:
            node.display()


    fault_node = input ("please input the name of the node with a fault (if you do not want to input a fault, press enter):\n")

    if not len(fault_node) == 0:
        fault_value = input("please input a value for the fault:\n")

    for node in node_list:
        if node.name == fault_node:
            node.set_value(fault_value)
            node.display()

    print("--- Begin simulation: ---")

    # calculates the value of each node in the list
    for n in node_list:
        if n.value == "U":
            n.calculate_value()
        n.display()

    print("\n--- Simulation results: ---")

    input_list = [i.name for i in node_list if i.is_input]
    input_val = [i.value for i in node_list if i.is_input]

    print("input: \t", end="")
    print(*input_list, end="")
    print("\t = \t", end="")
    print(*input_val)

    output_name = [i.name for i in output_list]
    output_val = [i.value for i in output_list]

    print("output:\t", end="")
    print(*output_name, end="")
    print("\t = \t", end="")
    print(*output_val)

print(f"Finished - bye!")