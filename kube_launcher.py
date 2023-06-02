import subprocess
import random
import os
import json
from time import sleep

# ---------------------------- initial_rolls

#command1 = "kubectl delete -n default configmap base-config-initial-rolls"
command2 = f"kubectl create configmap base-config-initial-rolls \
             --from-file=/home/arshavee/Desktop/MASSA\ internship/massa-cloud-simulator-main/config/initial_rolls.json"

command3 = f"kubectl create configmap base-config-initial-peers --from-file=/home/arshavee/Desktop/MASSA\ internship/massa-cloud-simulator-main/initial_peers.json"
    # Execute the command and capture the output
#output1 = subprocess.check_output(command1, shell=True)
output2 = subprocess.check_output(command2, shell=True)
output3 = subprocess.check_output(command3, shell=True)
    # Decode the output from bytes to string
#output1 = output1.decode("utf-8")
output2 = output2.decode("utf-8")
output3 = output3.decode("utf-8")
    
#print(output1)
print(output2)
print(output3)

             


# Define the file path
file_path = "/home/arshavee/Desktop/MASSA internship/massa-cloud-simulator-main/initial_peers.json"

num_nodes = int(input("Enter the number of nodes(For more than one nodes): "))
num_initial_peer=(num_nodes // 10)+1 
# hopeing one peer can connect with 10 nodes and puting 2 peer extra 
# if num_nodes<2: initial_peer={}, command = "kubectl apply -f node1.yaml"

start_range = 2
end_range = num_nodes
num_numbers = num_initial_peer

# Choosing initial_peers Randomly
peers = random.sample(range(start_range, end_range + 1), num_numbers)
print(peers)


# Define the path from where you want to run the Kubernetes deployments
path = "/home/arshavee/Desktop/MASSA internship/massa-cloud-simulator-main/kubernetes-cluster-files/deployments/"

# Change the working directory
os.chdir(path)

# Define the command you want to run
command = "kubectl apply -f node1.yaml"
command1 = "kubectl get service | grep \"massa-node-1\" | awk '{print $3}'"
# Execute the command and capture the output
output = subprocess.check_output(command, shell=True)
output1 = subprocess.check_output(command1, shell=True)
# Decode the output from bytes to string
output = output.decode("utf-8")
output1 = output1.decode("utf-8")
# Print the output
print(output)
print(output1)
# ------------------------------------initial-peer-configmap new 

def update_initial_peer():
    command2 = "kubectl delete -n default configmap base-config-initial-peers"
    command3 = f"kubectl create configmap base-config-initial-peers --from-file=/home/arshavee/Desktop/MASSA\ internship/massa-cloud-simulator-main/initial_peers.json"
    # Execute the command and capture the output
    output2 = subprocess.check_output(command2, shell=True)
    output3 = subprocess.check_output(command3, shell=True)
    # Decode the output from bytes to string
    output2 = output2.decode("utf-8")
    output3 = output3.decode("utf-8")
    print(output2)
    print(output3)





# -------------------------- def for appending initial peer


def append_initial_peer(key_number):
    
    #ip for i node
    command_ip = f"kubectl get service | grep \"massa-node-{key_number}\" |awk '{{print $3}}'"
    # Execute the command and capture the output
    ip_address = subprocess.check_output(command_ip, shell=True)
    # Decode the output from bytes to string

    ip_address = ip_address.decode("utf-8")
    # Print the output
    print(key_number)
    print (ip_address)

    
    # Define the path to the existing JSON file
    json_file_path = f"/home/arshavee/Desktop/MASSA internship/massa-cloud-simulator-main/config/node_keypair_{key_number}.key"

    # Read the contents of the file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Fetch the value of the public key
    public_key = data["public_key"]
    
    
    
    file_path = "/home/arshavee/Desktop/MASSA internship/massa-cloud-simulator-main/initial_peers.json"
    # Read the existing JSON file
    with open(file_path, "r") as file:
        existing_data = json.load(file)

    # Define the new data to append
    new_data = {
        public_key: {
            "listeners": {
                ip_address.strip() + ":31244": "Tcp"
            },
            "category": "Bootstrap"
        }
    }

    # Append the new data to the existing data
    existing_data.update(new_data)
    
    
    # Write the updated JSON data back to the file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    print("File write complete.")
append_initial_peer(1) 
update_initial_peer()    
for i in range(1, num_nodes + 1):
    filename = f"node{i}.yaml"
    command = f"kubectl apply -f {filename}"
    subprocess.run(command, shell=True)
    sleep(5)
    if (i in peers):
        print ("hello")
        sleep(20)
        # append in initial peer
        append_initial_peer(i)
        update_initial_peer()
    
    