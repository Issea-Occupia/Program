import pandas as pd

# Login using e.g. `huggingface-cli login` to access this dataset
df = pd.read_json("hf://datasets/liumindmind/NekoQA-10K/NekoQA-10K.json")
df