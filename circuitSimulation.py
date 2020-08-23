# Class used to store information for a wire
class Node(object):
    def __init__(self, i, v, op, inlist, ii, io):
        self.name = i         # string
        self.value = v        # char: '0', '1', 'U' for unknown
        self.operator = op    # string such as "AND", "OR" etc
        self.interms = []     # list of nodes (first as strings, then as nodes), each is a input wire to the gate
        self.interm_names = inlist
        self.is_input = ii    # boolean: true if this wire is a primary input of the circuit
        self.is_output = io   # boolean: true if this wire is a primary output of the circuit
    
    def set_interms(self, interms):
        self.interms = interms
    
    def set_output(self, io):
        self.is_output = io
    
    def set_operator(self, op):
        self.operator = op
    
    def set_value(self, v):
        self.value = v
    
    def __repr__(self):     # defines how print(node) should behave
        nodevalue = self.value
        
        if self.is_input:
            return f"node: {str(self.name[5:]):2s} = {str(nodevalue):10s}"
        
        interm_str = ""
        interm_val_str = ""
        for i in self.interms:
            interm_str += str(i.name[5:])
            interm_val_str += str(i.value)
        
        return f"node: {str(self.name[5:]):2s} = {str(nodevalue):10s} || is the output of {str(self.operator):7s}"\
        f"gate with interms {interm_str} = {interm_val_str}"
    
    # Function that calculates value of the node based on its interm
    def calculate_value(self):
        for i in self.interms:
            if i.value == "U":
                return "U"
    
        if self.operator == "AND":
            val = "1"
            for i in self.interms:
                if i.value == "0":
                    val = "0"
            self.value = val
            return val
elif self.operator == "OR":
    val = "0"
        for i in self.interms:
            if i.value == '1':
                val = "1"
            self.value = val
            return val
        elif self.operator == "NAND":
            flag = "1"
            for i in self.interms:
                if i.value == "0":
                    flag = "0"
            val = not flag
            self.value = val
            return val
    elif self.operator == "NOT":
        val = self.interms[0].value
        self.value = str(1-int(val))
        return val
        elif self.operator == "XOR":
            numberOf1 = 0
            for i in self.interms:
                if self.interms.value == "1":
                    numberOf1 = numberOf1 + 1
            val = numberOf1 % 2
            val = str(val)
            self.value = val
            return val
        elif self.operator == "XNOR":
            numberOf1 = 0
            for i in self.interms:
                if self.interms.value == "1":
                    numberOf1 = numberOf1 + 1
            val = numberOf1 % 2
            self.value = str(1-val)
            return val
elif self.operator == "NOR":
    flag = "0"
        for i in self.interms:
            if i.value == "1":
                flag = "1"
            val = str(1-int(flag))
            self.value = val
            return val


# Take a line from the circuit file which represents a gate operation and returns a node that stores the gate

def process_gate(strVal):
    # result wire, operation, input wires
    name_end_idx = strVal.find(" = ")
    node_name = str(strVal[0:name_end_idx])
    op_start_idx = strVal.find("=") + 2
    op_end_idx = strVal.find("(")
    node_operator = strVal[op_start_idx:op_end_idx]
    
    # store children in list
    interm_start_idx = strVal.find("(") + 1
    end_position = strVal.find(")")
    
    temp_str = strVal[interm_start_idx:end_position]
    
    interm_name_list = temp_str.split(", ")
    curr_node = Node("wire_" + node_name, "U", node_operator, interm_name_list, False, False)
    return curr_node


# Create trees from input file, store all the input wires and output wires in a list
# Creates a new node for each gate operation
def construct_nodelist():
    o_name_list = []
    
    for fileline in input_file_values:
        if fileline == "\n":
            continue
        
        if fileline.startswith("#"):
            continue
        
        if fileline.startswith("INPUT"):
            index = fileline.find(")")
            intValue = str(fileline[6:index])
            name = "wire_" + str(intValue)
            node_list.append(Node(name, "U", "interms", [], True, False))
        
        
        elif fileline.startswith("OUTPUT"):
            index = fileline.find(")")
            name = "wire_" + str(fileline[7:index])
            o_name_list.append(name)
        
        
        else:
            new_node = process_gate(fileline)
            node_list.append(new_node)

for i in node_list:
    if i.name in o_name_list:
        i.set_output(True)
    
    
    # Convert the interm from a list of names (string) to a list of references (nodes)
    for node in node_list:
        for j in range(len(node.interm_names)):
            interm_name = "wire_" + node.interm_names[j]
            for interm_node in node_list:
                if interm_node.name == interm_name:
                    node.interms.append(interm_node)


# Helper function to clear values in tree
def clear_values():
    for i in node_list:
        i.set_value("U")


# Main function starts

# Step 1: get circuit file name from command line
wantToInputCircuitFile = str(
                             input("The default circuit bench file is circuit.bench, type a file name if you want to change it.\n"))

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
construct_nodelist()
# printing list of constructed nodes
for i in node_list:
    print (i)

print ("---------------")

line = input("please input a value (return to exit):\n")

while len(line) != 0:
    clear_values()
    print("currently running: ", line.strip())
    
    strindex = 0
    
    # Set value of input node
    for i in node_list:
        if i.is_input:
            i.set_value(line[strindex])
            print(i.name[5:], " set value to ", line[strindex])
            strindex = strindex + 1

# Compute value of the gate nodes
complete = False
    while complete == False:
        complete = True
        for i in node_list:
            val = 0
            if i.value == "U":
                val = i.calculate_value()
            # print(i.name, val)
            
            print (i)
            
            if val == "U":
                complete = False


print("\n--- value of output nodes ---")
# Print the value of the output nodes
print("input [", end="")
    curlen = 0
    for i in node_list:
        if i.is_input:
            print(i.name[5:], end="")
            if curlen != 2:
                print(", ", end="")
            curlen = curlen + 1

print("] = ", line.strip())

print("output [", end="")
curlen = 0
    for i in node_list:
        if i.is_output:
            print(i.name[5:], end="")
            if curlen != 3:
                print(", ", end="")
            curlen = curlen + 1

print("] = ", end="")


for i in node_list:
    if i.is_output:
        print(i.value, end="")
    
    print("\n\n")
    line = input("please input a value (return to exit): ")
