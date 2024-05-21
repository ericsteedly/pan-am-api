import json
# This code is used to renumber the pk's in the x.json template of flights

# x.json file is currently a template for 1 month of flights
# first use command + F, Option + Return to select and chang the month as needed
file_path = "/Users/ericsteedly/workspace/pan-am-api/panamapi/fixtures/x.json"

# Load the JSON data from the file
with open(file_path, "r") as file:
    data = json.load(file)

# Insert pk into the first object in json file after which you would like to start incrementing, 
# it will be grabbed as "x" for starter reference

# Iterate over the JSON data

x = data[0].get("pk")

for item in data:
    item["pk"] = x + 1
    x = item.get("pk")


# Save the modified JSON data back to the file
with open(file_path, "w") as file:
    json.dump(data, file, indent=4)