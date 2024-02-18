from machine import Pin
import sys

# Imported file
file_path = "loan_train_em.csv"
attributes = ["Married", "Dependents", "Education", "Self_Employed", "Applicant_Income", "Coapplicant_Income", "Loan_Amount", "Credit_History"]

# Read and format the imported data file 
def read_csv_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    header = lines[0].strip().split(",")
    data = [dict(zip(["index"] + header, [i] + line.strip().split(","))) for i, line in enumerate(lines[1:], 1)]
    return data

data = read_csv_data(file_path)
header = ["index"] + list(data[0].keys())[1:]

# def write_csv_data(file_path, header, data):
#     with open(file_path, "w") as f:
#         f.write(",".join(header) + "\n")
#         for row in data:
#             f.write(",".join([str(row[h]) for h in header]) + "\n")
        
            
# Class for each node, contains informations about the node and the split on the node
class Node:
    def __init__(self, data, attributes, target, depth=0):
        self.data = data
        self.attributes = attributes
        self.target = target
        self.depth = depth
        self.split_attr = None
        self.children = []

# Sort the data
def sort_data(data, attr):
    return sorted(data, key=lambda x: x[attr])

# Count the dependent variable for the gini
def count_credit_status(data):
    counts = {"Y": 0, "N": 0}
    for row in data:
        counts[row["Credit_Status"]] += 1
    return counts

# Calculate the gini index for the data and for each attribute 
def gini_index(data):
    counts = count_credit_status(data)
    total = sum(counts.values())
    gini = 1 - sum([(count / total) ** 2 for count in counts.values()])
    return gini

def gini_index_for_attribute(data, attr):
    sorted_data = sort_data(data, attr)
    total_gini = 0
    for i in range(len(sorted_data) - 1):
        left_data = sorted_data[: i + 1]
        right_data = sorted_data[i + 1 :]
        left_gini = gini_index(left_data)
        right_gini = gini_index(right_data)
        total_gini += (len(left_data) * left_gini + len(right_data) * right_gini) / len(sorted_data)
    return total_gini / (len(sorted_data) - 1)

# Build decision tree classifier using the informations obtained
def build_tree(node, max_depth):
    if stopping_criterion(node, max_depth):
        return

    node.split_attr = best_split(node.data, node.attributes, node.target)
    for child_data in split_data(node.data, node.split_attr):
        child_attributes = list(node.attributes)
        child_attributes.remove(node.split_attr)
        child = Node(child_data, child_attributes, node.target, node.depth + 1)
        node.children.append(child)
        build_tree(child, max_depth)

# LED on if gini exist, LED off if gini does not exist
def is_continuous_attribute(attr):
    continuous_attributes = ["Applicant_Income", "Coapplicant_Income", "Loan_Amount"]
    return attr in continuous_attributes

led = machine.Pin(25, machine.Pin.OUT)

def delay():
    for i in range(0, 195785):
        pass
    
def response():
    response = sys.stdin.readline()
    if response == "\n":
        pass
 
for attr in attributes:
    response()
    if is_continuous_attribute(attr):
        gini = 0
        led.off()
        print(f"Gini index for {attr}: {gini}")
        delay()
    else:
        gini = gini_index_for_attribute(data, attr)
        led.on()
        print(f"Gini index for {attr}: {gini}")
        delay()
        led.off()
    response()


    

