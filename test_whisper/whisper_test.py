import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
print(torch.__version__)
print(torch.cuda.is_available())  # Трябва да върне False без грешка

