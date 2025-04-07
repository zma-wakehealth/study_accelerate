from accelerate import Accelerator
from torch.utils.data import DataLoader
import torch.distributed as dist
import socket

if (__name__ == "__main__"):
    # Initialize the accelerator
    accelerator = Accelerator()

    # # Get the rank
    # rank = dist.get_rank()

    # Get the hostname
    hostname = socket.gethostname()

    # Print the rank and hostname
    print(f"Hostname: {hostname}")

    # Additional information
    print(f"Local Rank: {accelerator.local_process_index}")
    print(f"Process Index: {accelerator.process_index}")
    print(f"Is Main Process: {accelerator.is_main_process}")

    dataloader = DataLoader(range(10), batch_size=2, shuffle=False)
    dataloader = accelerator.prepare(dataloader)
    accelerator.wait_for_everyone()
    for a in dataloader:
        print(a)
    accelerator.wait_for_everyone()