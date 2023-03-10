import socket
import pandas as pd
import openpyxl

# Get the host name
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Write the IP address to a file
with open("ip_address.txt", "w") as file:
	file.write(ip_address)
print("IP address: ", ip_address)


# take user input for username, password and command
username = input("Enter username: ")
password = input("Enter password: ")
command = input('Enter command: ')

# read IP addresses from txt file
with open('ip_address.txt') as f:
    ip_list = [line.strip() for line in f]
    
# read the list of commands and matches from the excel file
df = pd.read_excel("CIS-Benchmark.xlsx", sheet_name="Sheet1")
commands = list(df["Command"])
outputs = list(df["Match"])

# check if the user input command matches any command in the excel file
if command in commands:
        result = "Pass"
        output = outputs[commands.index(command)]
else:
        result = "fail"
        output=""

# create a new DataFrame to store the results
results_df = pd.DataFrame(columns=["IP Address", "Command", "Output", "Result"])

# iterate over each IP address and store the result in the DataFrame
for ip in ip_list:
  new_result = results_df.append({'IP Address': ip, 'Command': command, 'Output': output, 'Result': result}, ignore_index=True)
  results_df = results_df.append(new_result, ignore_index=True)

#try to read existing results file, if it exists
  try:
       existing_results_df = pd.read_csv('results.xlsx')
       results_df = pd.concat([existing_results_df, results_df], ignore_index=True)
  except FileNotFoundError:
   pass

# write the results to a new excel file
results_df.to_csv('results.xlsx', index=False, mode='w')