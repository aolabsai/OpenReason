

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# "I would have written a shorter letter, but I did not have the time." -- Blaise Pascal

# There are so many different ways of training large models through large-scale reinforcement learning (RL) similar in the style of DeepSeek-R1 that attempting to find "the best" is a futile effort; too much variance.
# Instead, why not try to build the absolute simplest possible training paradigm; simpler than R1-Zero, even simpler than other projects (to be listed).


# system prompt
thinker_initial_prompt =
"""
Please respond with the very best of your abilities. Your task is to generate four distinct possible next thinking steps in a problem-solving process. Given a Question and a Chain of Thoughts, you will:

Analyze and understand the question.
Propose 4 different possible next thinking steps that need not be the correct final answer but could lead to it.

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

Respond only with a python list containing 4 strings. Be sure to strictly follow the above example and make sure the output is always only a valid list of 4 strings corresponding to the 4 different (unrelated) next thinking steps.

Question:
What is 800 divided by 4 times 3.5?

Chain of Thoughts so far:
step 1: Now, let's consider the order of operations and calculate 800 / 4 * 3.5 step-by-step.

"""


# after system prompt, should output only a list (ideally) or a listed called `output`
thinker_initial_test =
"""
Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.
"""



think_response = [
"Next, I can start by dividing 800 by 4, which gives 200.",
"First, I could multiply 4 and 3.5 to get 14, then divide 800 by that.",
"Now, let's consider the order of operations and calculate 800 / 4 * 3.5 step-by-step.",
"I might try breaking 3.5 into 3 + 0.5 and handle the multiplication separately after the division."
]