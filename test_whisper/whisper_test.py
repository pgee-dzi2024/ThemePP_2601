import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TORCH_USE_CUDA_DSA"] = "0"

import torch
print(torch.__version__)
print(torch.cuda.is_available())  # трябва да върне False

import whisper
model = whisper.load_model("small", device="cpu")
print("Whisper работи успешно на CPU")



