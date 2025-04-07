from torch import nn
import numpy as np
import torch
from torch.utils.data import DataLoader
from accelerate.utils import set_seed
from accelerate import Accelerator
import time
import socket

set_seed(42)

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(1000, 10000)
        self.layer2 = nn.Linear(10000, 50000)
        self.layer3 = nn.Linear(50000, 5000)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

if (__name__ == '__main__'):

    hostname = socket.gethostname()

    x = torch.randn(8,1000)
    loader = DataLoader(x, batch_size=2, shuffle=False)
    model = MyModel()

    accelerator = Accelerator()
    model, loader = accelerator.prepare(model, loader)
    
    for x in loader:
        print("in hostname=", hostname, x[:, 0])
    
    for i in range(100):
        for x in loader:
            time.sleep(1)
            tmp = model(x)
            if (i==0):
                print("in hostname=", hostname, tmp)
    