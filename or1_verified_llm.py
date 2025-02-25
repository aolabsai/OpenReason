# this script is when we have both question and solution #


import openai
import json
from datasets import load_dataset


API_KEY = "..."

def openai_cot(question, solution):
   
    prompt = f"""
            Question: {question}
            Solution: {solution}

            Provide a detailed step-by-step Chain of Thought (CoT) reasoning before arriving at the solution.

            ### Chain of Thought Explanation:
            1. **Understanding the problem:** Explain the core objective of the question.
            2. **Breaking down the approach:** Outline key principles, formulas, or logic used to solve the problem.
            3. **Step-by-step solution reasoning:** Provide a detailed breakdown of calculations or logical steps.
            4. **Final verification:** Confirm why the obtained solution is correct.
            """

    
    
    response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                api_key=API_KEY
            )
    
    return response["choices"][0]["message"]["content"]
        

    




# Loading data
dataset = load_dataset("aolabs/s50k_trial1")["train"]

first_example = dataset[0]  

question = first_example["question"] 
solution = first_example["solution"]

# Generating CoT 
cot_response = openai_cot(question, solution)

print(cot_response)
