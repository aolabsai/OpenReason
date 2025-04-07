

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# "I would have written a shorter letter, but I did not have the time." -- Blaise Pascal

# There are so many different ways of training large models through large-scale reinforcement learning (RL) similar in the style of DeepSeek-R1 that attempting to find "the best" is a futile effort; too much variance.
# Instead, why not try to build the absolute simplest possible training paradigm; simpler than R1-Zero, even simpler than other projects.


# system prompt
unverified_concluder_system_prompt = """
Please respond with the very best of your abilities. Your task is to determine the solution in a problem-solving process. Given a Question and a Chain of Thoughts, you will:

- Analyze and understand the question.
- Following the Chain of Thoughts from the question, propose a final answer.

An example is below--

Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.
step 3: I can then multiply 64 * 2 which is 128.
step 4: Adding 640 and 128 gives 768.


output = "768"

Respond only with a string that is the final answer.
"""


# # after system prompt, should output only a list of 4 strings
# thinker_initial_test = """
# Question:
# What is 64 * 12?

# Chain of Thoughts so far:
# step 1: I need to multiply 64 and 12 with each other.
# step 2: I can first multiply 64 * 10 which is 640.
