


from datasets import load_dataset


# accessing dataset subset (training, testing, validation, etc.) ## https://huggingface.co/docs/datasets/access#dataset
dataset = load_dataset("rotten_tomatoes", split="train")

# accessing particular data (indexing) ## https://huggingface.co/docs/datasets/access#indexing

for i in dataset[:]:
    
    q = dataset[i]["Question"]

    a = if dataset[i]["Answer"]

    selector_model
