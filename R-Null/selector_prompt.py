

# Inspired by https://github.com/simplescaling/s1/blob/main/data/verifier_index.txt


# system prompt
selector_system_prompt = """
Please respond with the very best of your abilities. Your task is to identify the best next thinking step in a problem-solving process. Given a Question, a Chain of Thoughts, and a list of Possible Next Thinking Steps, you will:

- Analyze and understand the question.
- Evaluate and compare each proposed next thinking step for correctness and relevance to the accumulated chain of thought and problem.
- Pick the best possible next thinking step based on how likely it could lead to the correct final answer if the chain of thought is followed from beginning to end.

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

X)
STOP thinking and provide a final answer.

output = "B"

Respond only with a python string. Be sure to strictly follow the above example and make sure the output is a string made up of only 1 character that is a capitalized letter corresponding to the best next thinking step from the list of Possible Next Thinking Steps.
"""

# after system prompt, should output only a single character string that is a capitalized letter
selector_initial_test = """
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