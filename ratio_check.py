from rapidfuzz import fuzz
from tabulate import tabulate

string1 = "X"
string2 = "X"
string3 = "AA"
string4 = "BB"
results1 = []
results2 = []
head = ["string length", "string1", "string2", "ratio", "ratio/length"]

for i in range(0, 9):
    string1 += "AXX"
    string2 += "BXX"
    string3 += "X"
    string4 += "X"
    
    ratio1 = fuzz.ratio(string1, string2)
    ratio2 = fuzz.ratio(string3, string4)
    
    results1.append([len(string1),string1, string2, ratio1, ratio1/len(string1)])
    #results2.append([string3, string4, ratio2, ratio2/len(string3)])
    
    #print(str(len(string1)) + "," + str(ratio1) + "," + str(ratio1/len(string1)) + "," + str(ratio2) + "," + str(ratio2/len(string1)))
    
    
print(tabulate(results1, headers=head, tablefmt="grid"))
#print(tabulate(results2, headers=head, tablefmt="grid"))

