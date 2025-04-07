import json
import re
import ollama

from unverified_prompts.thinker_prompt import unverified_thinker_system_prompt, thinker_initial_test
from unverified_prompts.selector_prompt import unverified_selector_system_prompt, selector_initial_test
from unverified_prompts.concluder_prompt import unverified_concluder_system_prompt

from verified_prompts.thinker_prompt import verified_thinker_system_prompt
from verified_prompts.selector_prompt import verified_selector_system_prompt
from verified_prompts.concluder_prompt import verified_concluder_system_prompt
# put your question as a string in the problem variable and then run this whole script and see the slop-magic.

problem = "Let h(x) = (x^{-1/2} + 2x)(7 - x^{-1}). What is h'(x) when x = 4?"
chain = ""
chain_steps = 0
answer = "13.609"

def clean_response(response):
    # Try to extract the final summary statement
    match = re.findall(r'</think>\s*([^\n]+)', response)
    if match:
        response = match[0]
    else:
        # Fallback: remove <think> tags and take the last non-empty line
        response = re.sub(r'<\/?think>', '', response).strip()
        response = [line.strip() for line in response.splitlines() if line.strip()]
        if response:
            response = response[-1]
        else:
            response = "Could not extract step"
    
    return response[:60] 

def think(chain, problem=problem, answer=None):

    if answer:
        thoughts = f"""
        Question:
        {problem}

        Chain of Thoughts:
        {chain}
        
        Solution/Answer: 
        {answer}"""

        thoughts = verified_thinker_system_prompt + thoughts

    else:
        thoughts = f"""
        Question:
        {problem}

        Chain of Thoughts:
        {chain}"""

        thoughts = unverified_thinker_system_prompt + thoughts

    # n = 0
    new_thoughts = []
    for n in range(4):
        think = ollama.generate('deepseek-r1:7b', thoughts)
        next_step = think['response']
        print("RAW THOUGHT-- " + str(n+1)+ " ---- "+next_step)
    
        try:
            next_step = clean_response(next_step)
        except Exception as e:
            print("cleaning failed", e)
            continue

        new_thoughts.append(next_step)
        # if with_answer:
        #     if type(next_step) is str:
        #             answer = new_thoughts.replace("\n", " ")  # stripping away line breaks  
        #             print("ANSWER RETURNED")
        #             return chain, answer, 0

    keys = ["A", "B", "C", "D", "E"]
    new_thoughts += ["STOP thinking and provide a final answer"]
    new_thoughts_dict = dict(zip(keys, new_thoughts))
    new_thoughts =f"""
    A)
    {new_thoughts[0]}

    B)
    {new_thoughts[1]}

    C)
    {new_thoughts[2]}

    D)
    {new_thoughts[3]}

    E)
    {new_thoughts[4]}."""

    return chain, new_thoughts, new_thoughts_dict


def select(problem, chain, new_thoughts, new_thoughts_dict, answer=None):
    # Compose prompt
    if answer:
        choices = f"""Question:
{problem}

Chain of Thoughts:
{chain}

Solution/Answer:
{answer}

Possible Next Thinking Steps: 
{new_thoughts}"""
        prompt = verified_selector_system_prompt + choices
    else:
        choices = f"""Question:
{problem}

Chain of Thoughts:
{chain}

Possible Next Thinking Steps: 
{new_thoughts}"""
        prompt = unverified_selector_system_prompt + choices  # You can define this separately if needed

    # Call model
    select_response = ollama.generate('deepseek-r1:7b', prompt)
    model_output = select_response['response']
    print("Raw model output:\n", model_output)

    # Try extracting the selected letter
    match = re.search(r'ANSWER:\s*([A-E])', model_output)
    if match:
        new_selection = match.group(1).strip().upper()
    else:
        # Try to fallback if it gave a plain letter
        fallback_match = re.search(r'\b([A-E])\b', model_output.strip())
        if fallback_match:
            new_selection = fallback_match.group(1).strip().upper()
        else:
            print("Could not extract valid option.")
            print(model_output)
            return chain, None

    if new_selection not in new_thoughts_dict:
        print(f" Invalid selection: {new_selection}")
        return chain, None

    # Append to chain
    global chain_steps
    chain_steps += 1
    new_chain = f"\nstep {chain_steps}: {new_thoughts_dict[new_selection]}"
    chain += new_chain

    return chain, new_selection




def answer( question, with_select=True, answer=None):

    global chain
    global problem
    problem = question

    n = 0
    unanswered = True
    while unanswered and n < 20:
        chain, new_thoughts, new_thoughts_dict = think(chain)
        print(new_thoughts_dict)

        # if with_answer:
        #     if new_thoughts_dict == 0:
        #         final_answer = new_thoughts
        #         return final_answer, chain, n


        chain, new_selection = select(problem, chain, new_thoughts, new_thoughts_dict, answer=answer)
        print(chain)
        if with_select:
            print("Selected option:", new_selection)
            if new_selection.strip().upper() == "E":
                unanswered = False
                if answer:
                    conclusions = f"""
                    Question:
                    {problem}

                    Chain of Thoughts:
                    {chain}
        
                    Solution/Answer: 
                    {answer}"""

                    conclusions = verified_concluder_system_prompt + conclusions

                else:
                    conclusions = f"""
                    Question:
                    {problem}

                    Chain of Thoughts:
                    {chain}"""

                    conclusions = unverified_concluder_system_prompt + conclusions

                final_answer = ollama.generate('deepseek-r1:7b', conclusions)
                final_answer = final_answer['response']

                return final_answer, chain, n
        
        n += 1

question= problem

final_answer, chain, n = answer(question, answer=answer)

# https://github.com/ollama/ollama/blob/main/docs/api.md#response


# final_answer = ollama.generate('llama3.2:latest', question)
# final_answer['response']



# chain, new_thoughts, new_thoughts_dict = think(chain, problem=problem, answer=None)