import os
import re
import yaml

def create_config(num_nodes, first_node, ngpus):
    '''
      create the config file for each node
    '''
    # load the template
    with open('config_template.yaml', 'r') as fid:
        config = yaml.safe_load(fid)

    # these should be the same for every file
    # num_processes should be ngpus in most cases
    config['main_process_ip'] = first_node
    config['num_machines'] = num_nodes
    config['num_processes'] = ngpus

    # only the rank is different
    for i in range(ngpus):
        config['machine_rank'] = i
        with open(f'config_{i}.yaml', 'w') as fid:
            yaml.safe_dump(config, fid)
    
    return

def parse_nodelist(nodelist):
    """
    Parse the nodelist string to calculate the number of nodes and extract the first node.
    Example: 
        "demon[089,111-113]" -> 4 nodes, first node: "demon089", output_nodelist: "demon089 demon111 demon112 demon113"
        "demon089" -> 1 node, first node: "demon089", output_nodelist: "demon089"
    """
    # Check if the nodelist is a single node (e.g., "demon089")
    single_node_match = re.match(r"(\w+\d+)", nodelist)
    if single_node_match:
        return 1, nodelist, nodelist  # Single node, return 1 node and the node itself as the first node

    # Handle nodelist with ranges (e.g., "demon[089,111-113]")
    match = re.match(r"(\w+)\[(.+)\]", nodelist)
    if not match:
        raise ValueError("Invalid nodelist format. Expected format: 'name[range1, range2, ...]' or 'nameXXX'")
    
    prefix = match.group(1)
    ranges = match.group(2).split(",")
    num_nodes = 0
    first_node = None
    output_nodelist = []

    for r in ranges:

        if "-" in r:  # Handle ranges like 111-113
            start, end = map(int, r.split("-"))
            num_nodes += end - start + 1
            if first_node is None:
                first_node = f"{prefix}{start:03d}"  # Extract the first node
            for i in range(start, end+1):            # loop from start:end+1 to add the node into the list
                output_nodelist.append(f"{prefix}{i:03d}")

        else:  # Handle single nodes like 089
            num_nodes += 1
            if first_node is None:
                first_node = f"{prefix}{int(r):03d}"  # Extract the first node
            output_nodelist.append(f"{prefix}{int(r):03d}")

    return num_nodes, first_node, ' '.join(output_nodelist)
    

if (__name__ == "__main__"):
    nodelist = os.getenv("SLURM_JOB_NODELIST")
    ngpus = int(os.getenv("SLURM_GPUS"))

    # parse the nodelist
    num_nodes, first_node, output_nodelist = parse_nodelist(nodelist)

    # need a config file for each node
    create_config(num_nodes, first_node, ngpus)

    # get the output to the calling bash script
    print("node list=", output_nodelist)