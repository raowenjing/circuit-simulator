import sys

# maximum number of wires, including both input, output and intermediate wires
MAX_LINES = 10000

# writes the type of gate and saves the children of each wire
def output_nodes():
    for input in inputlist:
        if input == "\n":
            continue

        if input.startswith("#"):
            continue

        if input.startswith("INPUT"):
            index = input.find(")")
            intValue = int(input[6:index])
            keyValue[intValue] = "input_" + str(intValue)
            inputList.append(intValue)
            f.write("    ")
            f.write("input_")
            f.write(str(intValue))
            f.write (" [color = brown, shape = invhouse]")
            f.write ("\n")


        elif input.startswith("OUTPUT"):
            index = input.find(")")
            outputList.append(int(input[7:index]))

        else:
            index = input.find(" = ")
            nodeOperation = -1;
            nodeIndex = int(input[0:index])
            f.write("    ")

            strVal = ""
            if input.find("NAND") != -1:
                strVal = "NAND_"
            elif input.find("OR") != -1:
                strVal = "OR_"
            elif input.find("AND") != -1:
                strVal = "AND_"
            elif input.find("NOT") != -1:
                strVal = "NOT_"

            f.write(strVal)

            if outputList.count(nodeIndex) != 0:
                f.write(str(nodeIndex))
                f.write(" [color = green, shape = invtriangle]")
                keyValue[nodeIndex] = strVal + str(nodeIndex)
            else:
                nodeOperation = strVal
                f.write(str(nodeIndex))
                f.write(" [color = yellow]")
                keyValue[nodeIndex] = strVal + str(nodeIndex)

            f.write("\n")

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
if len(sys.argv) != 4:
    print("USAGE: python convertDotLanguage.py  CIRCUIT_FILE  OUTPUT_FILE MAX_LINES")
    print (len(sys.argv))
    exit()
circuitFile = sys.argv[1]
outputFile = sys.argv[2]
MAX_LINES = int(sys.argv[3])

# Step 1: read circuit file
file1 = open(circuitFile,"r")
inputlist = file1.readlines()
file1.close()
outputList = []
inputList = []
listOfChildren = []
keyValue = ["space"] * MAX_LINES

# Step 2: generate output file
f = open(outputFile, "w")
f.write("digraph G {")
f.write("\n")
f.write("\n")
f.write ("    ")
f.write("node [style = filled]")
f.write("\n")
f.write("\n")

# processes the data and writes all the nodes into the output file
output_nodes()

f.write("\n")

# write the relationship between nodes to the output file
for i in listOfChildren:

    for j in range(len(i)):
        if j == 0:
            continue
        f.write("    ")
        f.write(str(keyValue[int(i[j])]))
        f.write (" -> ")
        f.write(str(keyValue[i[0]]))
        f.write("\n")

f.write ("}")
f.close()
