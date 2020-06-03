class Node:
    def __init__( self, _name, _inputs, _type, _value ):
        self.name = _name            #string
        self.inputs = _inputs        #list of strings that correspond to the input nodes names
        self.type = _type            #string
        self.value = _value          #string, although limited to one character
        self.outputReady = False

    def PerformOp( self, nodes ):
        if ( self.type == 'input' or self.type == 'output' ):
            print("Error, type cannot be 'input' or 'output' for operations")
            return False

        op = self.type
        if ( op == 'AND' ):
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '0' ):
                    self.value = '0'
                    return True
                elif ( val == '1' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            self.value = '1'
        elif ( op == 'OR' ):
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '1' ):
                    self.value = '1'
                    return True
                elif ( val == '0' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            self.value = '0'
        elif ( op == 'NOR' ):
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '1' ):
                    self.value = '0'
                    return True
                elif ( val == '0' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            self.value = '1'
        elif ( op == 'NAND' ):
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '0' ):
                    self.value = '1'
                    return True
                elif ( val == '1' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            self.value = '0'
        elif ( op == 'XOR' ):
            onesCount = 0
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '1' ):
                    onesCount += 1
                elif ( val == '0' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            if ( ( onesCount % 2 ) == 1 ):   #odd number of 1s
                self.value = '1'
            else:
                self.value = '0'
        elif ( op == 'XNOR' ):
            onesCount = 0
            for inputName in self.inputs:
                val = GetVal( inputName, nodes )
                if ( val == '1' ):
                    onesCount += 1
                elif ( val == '0' ):
                    continue
                else:
                    print("Error, unsupported value at node: " + inputName )
                    return False
            if ( ( onesCount % 2 ) == 0 ):   #odd number of 1s
                self.value = '1'
            else:
                self.value = '0'
        elif ( op == 'NOT' ):
            val = GetVal( inputs[0], nodes )
            if ( val == '1' ):
                val = '0'
            elif ( val == '0' ):
                val = '1'
            else:
                print("Error, unsupported value at node: " + inputName )
                self.value = '?'
                return False
            self.value = val
        elif ( op == 'BUFF' ):
            self.value = GetVal( inputs[0], nodes )
        else:
            print("Error, unsupported operation at node: " + self.name )
            return False
        return True     #just to indicate success

def MakeNodes( benchName ):
    pass

# This function traverses the graph looking for a name match
# Once a match is found, it returns the value
def GetVal( name, nodes ):
    for node in nodes:
        if ( node.name == name ):
            return node.value
    return None   #This indicates an error since there should always be a match

def GetTestVectors( fileName ):
    pass

def Simulate( circuit, testVectors ):
    pass

def main():
    # Read-in circuit benchmark and create circuit nodes
    userInput = input()
    circuit = MakeNodes( userInput )
    # Read-in test vectors
    userInput = input()
    testVectors = GetTestVectors( userInput )
    # Performance simulation/breadth-first search through the circuit
    # Simultaneously do some other stuff depending on what the assignment calls for?
    # Ex: Calculate the critical path (longest delay path)
    Simulate( circuit, testVectors )

if __name__ == "__main__":
    main()
