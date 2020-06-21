import sys

# writes the type of gate and saves the children of each wire
def output_nodes():
    for input in inputlist:
        # Checks if line is empty, if so continues
        if input == "\n":
            continue

        # checks if line is commented out
        if input.startswith("#"):
            continue

        # processes input wires of input, adds input wires into a list
        if input.startswith("INPUT"):
            index = input.find(")")
            intValue = int(input[6:index])
            inputList.append(intValue)
            f.write("    ")
            f.write(str(intValue))
            f.write (" [color = brown]")
            f.write ("\n")

        # processes output wires of output, adds output wires into a list
        elif input.startswith("OUTPUT"):
            index = input.find(")")
            outputList.append(int(input[7:index]))

        # processes all the logic gates and creates nodes for intermediate wires
        else:
            index = input.find(" = ")
            nodeIndex = int(input[0:index])
            f.write("    ")
            strVal = ""
            f.write(str(nodeIndex))
            f.write(" [fontcolor = white, label = \"\", color = black")

            if input.find("NAND") != -1:
                f.write(", image = \"nand.png\"]")
            elif input.find("NOR") != -1:
                f.write(", image = \"nor.png\"]")
            elif input.find("AND") != -1:
                f.write(", image = \"and.png\"]")
            elif input.find("NOT") != -1:
                f.write(", image = \"not.png\"]")
            elif input.find("XOR") != -1:
                f.write(", image = \"xor.png\"]")
            elif input.find("OR") != -1:
                f.write(", image = \"or.png\"]")
            else:
                f.write(", image = \"buff.png\"]")

            f.write("\n")

            # creates a list of children nodes and appends it into masterlist of child nodes
            children = []
            children.append(nodeIndex)
            index = input.find("(") + 1
            endvalue = input.find(")")

            while index < endvalue:
                indexen = input.find(",", index)
                if indexen == -1:
                    children.append(int(input[index:endvalue]))
                    break
                children.append(int(input[index:indexen]))
                index = indexen + 1

            listOfChildren.append(children)

# main function starts
# get input from command line
if len(sys.argv) != 3:
    print("USAGE: python convertDotLanguage.py  CIRCUIT_FILE  OUTPUT_FILE")
    print (len(sys.argv))
    exit()
circuitFile = sys.argv[1]
outputFile = sys.argv[2]

# Step 1: read circuit file
file1 = open(circuitFile,"r")
inputlist = file1.readlines()
file1.close()
outputList = []
inputList = []
listOfChildren = []
#keyValue = ["space"] * MAX_LINES

# Step 2: generate output file
f = open(outputFile, "w")
f.write("digraph G {\n\n")
f.write("    rankdir = LR\n")
f.write("    node [style = unfilled, imagescale = true, shape = square]\n")
f.write("    graph [splines = ortho]\n")
f.write("    edge [arrowtail = none]\n\n")

# processes the data and writes all the nodes into the output file
output_nodes()

f.write ("\n")
f.write("    {rank = source")

for i in inputList:
    f.write("; ")
    f.write(str(i))

f.write("}\n")



# write the relationship between nodes to the output file
for i in listOfChildren:

    for j in range(len(i)):
        if j == 0:
            continue
        f.write("    ")
        f.write(str(int(i[j])))
        #f.write(str(keyValue[int(i[j])]))
        f.write (" -> ")
        f.write(str(i[0]))
        f.write("\n")

for i in outputList:
    f.write ("    ")
    f.write (str(i))
    f.write (" -> O")
    f.write (str(i))
    f.write("\n")

f.write("\n    {rank = sink")

for i in outputList:
    f.write("; O")
    f.write(str(i))

f.write ("} \n }")

f.close()
