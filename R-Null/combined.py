import json

import ollama

from thinker_prompt import thinker_system_prompt, thinker_initial_test
from selector_prompt import selector_system_prompt, selector_initial_test
from concluder_prompt import concluder_system_prompt

from verified_prompts.thinker_prompt import verified_thinker_system_prompt
from verified_prompts.selector_prompt import verified_selector_system_prompt
from verified_prompts.concluder_prompt import verified_concluder_system_prompt
# put your question as a string in the problem variable and then run this whole script and see the slop-magic.

problem = "what is the value of X^4 + X^2 for x = 3"
chain = """"""
chain_steps = 0
answer = ""


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

        thoughts = thinker_system_prompt + thoughts

    # n = 0
    new_thoughts = []
    for n in range(4):
        think = ollama.generate('deepseek-r1:7b', thoughts)
        next_step = think['response']
        print("NEWWWW THOUGHT-- " + str(n+1)+ " ---- "+next_step)
        try:
            next_step = json.loads(next_step)
            # n += 1
            # print("thinking counter - " + str(n))
            # if n > 1: print("stupid")
        except Exception as e:
            print(e)
            pass
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


def select(chain, new_thoughts, new_thoughts_dict, answer=None):
    choices = f"""Question:
    {problem}

    Chain of Thoughts:{chain}

    Possible Next Thinking Steps: 
    {new_thoughts}"""
    
    if answer:
        choices = f"""Question:
        {problem}

        Chain of Thoughts:
        {chain}
        
        Solution/Answer:
        {answer}

        Possible Next Thinking Steps: 
        {new_thoughts}"""
        choices = verified_concluder_system_prompt + choices

    else:
        choices = f"""Question:
        {problem}

        Chain of Thoughts:
        {chain}

        Possible Next Thinking Steps: 
        {new_thoughts}"""
        choices = selector_system_prompt + choices

    s = 0
    while True:


        select = ollama.generate('llama3.2:latest', choices)

        new_selection = select['response']
        print("NEWWW SELECTION ---- "+new_selection)

        try:
            new_selection = json.loads(new_selection)
        except:
            print(new_selection)
            print("BREAKING")
            print(chain)
            print(new_thoughts)
            print(new_thoughts_dict)
        
        s += 1
        print("selecting counter - " + str(s))
        if s > 1: print("idiot")
        if new_selection in new_thoughts_dict:
            print("BROKE SELECT WHILE LOOPs")
            break

    global chain_steps    
    chain_steps += 1
    new_chain = f"""
    step {chain_steps}: {new_thoughts_dict[new_selection]}"""
    chain += new_chain

    return chain, new_selection



def answer( question, with_select=True, answer=None):

    global chain
    global problem
    problem = question

    n = 0
    unanswered = True
    while unanswered:
        chain, new_thoughts, new_thoughts_dict = think(chain)
        print(new_thoughts_dict)

        # if with_answer:
        #     if new_thoughts_dict == 0:
        #         final_answer = new_thoughts
        #         return final_answer, chain, n


        chain, new_selection = select(chain, new_thoughts, new_thoughts_dict, answer=answer)
        print(chain)
        if with_select:
            if new_selection == "E":
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

                    conclusions = concluder_system_prompt + conclusions

                final_answer = ollama.generate('deepseek-r1:7b', conclusions)
                final_answer = final_answer['response']

                return final_answer, chain, n
        
        n += 1

question= problem
answer=None

final_answer, chain, n = answer(question, answer=answer)

# https://github.com/ollama/ollama/blob/main/docs/api.md#response


# final_answer = ollama.generate('llama3.2:latest', question)
# final_answer['response']