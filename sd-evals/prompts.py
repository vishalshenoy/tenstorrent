import pandas as pd

splits = {'train': 'data/train.parquet', 'test': 'data/eval.parquet'}
df = pd.read_parquet("hf://datasets/Gustavosta/Stable-Diffusion-Prompts/" + splits["train"])
df_subset = df[1:101]
df_subset.to_csv("output.txt", sep='\t', index=False)

print("First 100 rows saved to output.txt")