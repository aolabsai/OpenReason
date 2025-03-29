

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# "I would have written a shorter letter, but I did not have the time." -- Blaise Pascal

# There are so many different ways of training large models through large-scale reinforcement learning (RL) similar in the style of DeepSeek-R1 that attempting to find "the best" is a futile effort; too much variance.
# Instead, why not try to build the absolute simplest possible training paradigm; simpler than R1-Zero, even simpler than other projects.


# system prompt
thinker_system_prompt = """
Please respond with the very best of your abilities. Your task is to generate four distinct possible next thinking steps in a problem-solving process. Given a Question and a Chain of Thoughts, you will:

- Analyze and understand the question.
- Propose 4 different possible next thinking steps that need not be the correct final answer but could lead to it building off the chain of thoughts.
- Keep each next thinking step as concise, short, and simple as possible.

An example is below--

Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.

output = [
"Next, let's do 64*2=129.",

"Next, I multiply 64 * 2, which yields 128.",

"Now we can directly calculate 64 * 12 = 768.",

"I now need to add 64 to 640 which gives 704."]

Respond only with a python list containing 4 strings. Be sure to strictly follow the above example and make sure the output is always only a list of 4 strings corresponding to 4 different (unrelated) possible next thinking steps.
"""


# after system prompt, should output only a list of 4 strings
thinker_initial_test = """
Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.
"""
