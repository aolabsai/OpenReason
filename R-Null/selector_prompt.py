

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# system prompt
decision_initial_prompt = 
"""
Please respond with the very best of your abilities. Your task is identify the best next thinking step in a problem-solving process. Given a Question, a Chain of Thoughts, and a list of possible Next Thinking Steps, you will:

Analyze and understand the question.
Evaluate and compare each proposed next thinking step for correctness and relevance.
Pick the best possible next thinking step based on how likely it will to the correct final answer.


An example is below--

Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.

Possible Next Thinking Steps:
A)
Next, let's do 64*2=129.

B)
Next, I multiply 64 * 2, which yields 128.

C)
Now we can directly calculate 64 * 12 = 768.

D)
I now need to add 64 to 640 which gives 704.

output =
"B"

Respond only with a python string comprised a single character. Be sure to strictly follow the above example and make sure the output is a string made up of only 1 character corresponding to the best next thinking step.
"""

# after system prompt, should output only a single character string
selector_initial_test = 
"""
Question:
What is 64 * 12?

Chain of Thoughts so far:
step 1: I need to multiply 64 and 12 with each other.
step 2: I can first multiply 64 * 10 which is 640.

Possible Next Thinking Steps:
A)
Next, let's do 64*2=129.

B)
Next, I multiply 64 * 2, which yields 128.

C)
Now we can directly calculate 64 * 12 = 768.

D)
I now need to add 64 to 640 which gives 704.
"""

Question:
What is 800 divided by 4 times 3.5?


A)
"Next, I can start by dividing 800 by 4, which gives 200.",

B)
"First, I could multiply 4 and 3.5 to get 14, then divide 800 by that.",

C)
"Now, let's consider the order of operations and calculate 800 / 4 * 3.5 step-by-step.",

D)
"I might try breaking 3.5 into 3 + 0.5 and handle the multiplication separately after the division."
]