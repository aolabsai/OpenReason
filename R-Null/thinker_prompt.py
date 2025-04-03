

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# "I would have written a shorter letter, but I did not have the time." -- Blaise Pascal

# There are so many different ways of training large models through large-scale reinforcement learning (RL) similar in the style of DeepSeek-R1 that attempting to find "the best" is a futile effort; too much variance.
# Instead, why not try to build the absolute simplest possible training paradigm; simpler than R1-Zero, even simpler than other projects.


# system prompt
thinker_system_prompt = """
Please respond with the very best of your abilities. Your task is to generate one distinct possible next thinking step in a problem-solving process. Given a Question and a Chain of Thoughts, you will:

- Analyze and understand the question.
- Propose only one possible next thinking step that need not be the correct final answer but could lead to it, building off the chain of thoughts.
- Keep each next thinking step as concise, short, and simple as possible.

Two examples are below--

Example1 -->
Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.

output = 
"I now need to add 64 to 640 which gives 704."

Example2 -->
Question:
What is the area of a rectangle with a length of 8 cm and a width of 5 cm?

Chain of Thoughts so far:
step 1: I need to calculate the area of the rectangle using the formula: Area = length × width.
step 2: I know that the length is 8 cm and the width is 5 cm.

Output:
"I can now multiply 8 by 5 to get the area."

Respond only with a single string containing the next thinking step.
"""


# after system prompt, should output only a list of 4 strings
thinker_initial_test = """
Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.
"""
