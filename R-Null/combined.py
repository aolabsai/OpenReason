import json
import re
import ollama

from unverified_prompts.thinker_prompt import unverified_thinker_system_prompt, thinker_initial_test
from unverified_prompts.selector_prompt import unverified_selector_system_prompt, selector_initial_test
from unverified_prompts.concluder_prompt import unverified_concluder_system_prompt

from verified_prompts.thinker_prompt import verified_thinker_system_prompt
from verified_prompts.selector_prompt import verified_selector_system_prompt
from verified_prompts.concluder_prompt import verified_concluder_system_prompt

class ChainOfThoughtRunner:
    def __init__(self, model_name='llama3.2:3b', verified=True):
        self.model_name = model_name
        self.verified = verified
        self.chain = ""
        self.problem = ""
        self.chain_steps = 0
        self.prompts = self.load_prompts(verified)

    def load_prompts(self, verified):
        return {
            "thinker": verified_thinker_system_prompt if verified else unverified_thinker_system_prompt,
            "selector": verified_selector_system_prompt if verified else unverified_selector_system_prompt,
            "concluder": verified_concluder_system_prompt if verified else unverified_concluder_system_prompt,
        }

    def think(self, chain, problem=None, answer=None):
        if answer:
            thoughts = f"""
            Question:
            {problem}

            Chain of Thoughts:
            {chain}
        
            Solution/Answer: 
            {answer}"""
            thoughts = self.prompts["thinker"] + thoughts
        else:
            thoughts = f"""
            Question:
            {problem}

            Chain of Thoughts:
            {chain}"""
            thoughts = self.prompts["thinker"] + thoughts

        new_thoughts = []
        for n in range(4):
            think_result = ollama.generate(self.model_name, thoughts)
            next_step = think_result['response']
            print(f"RAW THOUGHT-- {n+1} ---- {next_step.strip()}")
            new_thoughts.append(next_step)

        keys = ["A", "B", "C", "D", "E"]
        new_thoughts += ["STOP thinking and provide a final answer"]
        new_thoughts_dict = dict(zip(keys, new_thoughts))
        new_thoughts_formatted = f"""
        A) {new_thoughts[0]}

        B) {new_thoughts[1]}

        C) {new_thoughts[2]}

        D) {new_thoughts[3]}

        E) {new_thoughts[4]}."""

        return chain, new_thoughts_formatted, new_thoughts_dict


    def select(self, problem, chain, new_thoughts, new_thoughts_dict, answer=None):
        if answer:
            choices = f"""Question:
    {problem}

    Chain of Thoughts:
    {chain}

    Solution/Answer:
    {answer}

    Possible Next Thinking Steps: 
    {new_thoughts}"""
            prompt = self.prompts["selector"] + choices
        else:
            choices = f"""Question:
    {problem}

    Chain of Thoughts:
    {chain}

    Possible Next Thinking Steps: 
    {new_thoughts}"""
            prompt = self.prompts["selector"] + choices

        select_response = ollama.generate(self.model_name, prompt)
        model_output = select_response['response']
        print("Raw model output:\n", model_output)

        match = re.search(r'ANSWER:\s*([A-E])', model_output)
        if match:
            new_selection = match.group(1).strip().upper()
        else:
            fallback_match = re.search(r'\b([A-E])\b', model_output.strip())
            new_selection = fallback_match.group(1).strip().upper() if fallback_match else None

        if new_selection not in new_thoughts_dict:
            print(f"Invalid selection: {new_selection}")
            return chain, None

        self.chain_steps += 1
        new_chain = f"\nstep {self.chain_steps}: {new_thoughts_dict[new_selection]}"
        chain += new_chain

        return chain, new_selection

    def run(self, question, answer=None, with_select=True):
        self.problem = question
        self.chain = ""
        self.chain_steps = 0
        n = 0
        unanswered = True

        while unanswered and n < 5:
            self.chain, new_thoughts, new_thoughts_dict = self.think(self.chain, self.problem, answer=answer)
            print("Options:\n", new_thoughts_dict)

            self.chain, new_selection = self.select(self.problem, self.chain, new_thoughts, new_thoughts_dict, answer=answer)
            print("Updated Chain:\n", self.chain)

            if with_select and new_selection and new_selection.strip().upper() == "E":
                unanswered = False
                break
            n += 1

        unanswered = False
        if answer:
            conclusions = f"""
            Question:
            {self.problem}

            Chain of Thoughts:
            {self.chain}

            Solution/Answer: 
            {answer}"""
            conclusions = self.prompts["concluder"] + conclusions
        else:
            conclusions = f"""
            Question:
            {self.problem}

            Chain of Thoughts:
            {self.chain}"""
            conclusions = self.prompts["concluder"] + conclusions

        final_response = ollama.generate(self.model_name, conclusions)
        final_answer = final_response['response']

        return final_answer, self.chain, n


# problem="What is 2+2"
# answer="2"
# runner = ChainOfThoughtRunner(model_name='llama3.2:3b', verified=True)
# final_answer, chain, steps_taken = runner.run(question="What is 2+2?", answer="4")
# print("Chain of Thought:\n", chain)