# OpenReason
Let's build DeepSeek-R1's large-scale reinforcement learning dataset and generation pipeline, open source

----

[_Video Annoucement_](https://www.youtube.com/watch?v=dm5R3xCM8hY)


Many amazing teams have reverse-engineered [DeepSeek’s seminal R1-Zero and R1](https://arxiv.org/abs/2501.12948); reverse-engineered is perhaps not the best term, since to DeepSeek’s credit they did important work by open sourcing large parts of their efforts. Unlike traditional LLMs pre-trained on any/all data, reasoning models are LLMs usually as mixture of experts that are further fine-tuned on generated chain-of-thought data.

This brings to bear two related points:
- Every team reproducing R1 or building new reasoning models is constructing their own data pipeline (the data and code used to generate it) for large-scale reinforcement learning that distinguishes these models from the base LLMs they are fine-tuned from.
- And it is precisely this part that DeepSeek did not open source ([this post succinctly lays out how DeepSeek is 2/4 with being fully open](https://www.linkedin.com/posts/timnit-gebru-7b3b407_friends-for-something-to-be-open-source-activity-7290232331468967936-6vea))-- they didn’t open source the data used for large scale RL nor did they share the code and data sources used to generate that data

For the sake of an open AI ecosystem and to positively accelerate development, let’s build a **large scale reinforcement learning data pipeline open source**.

Specifically, we are talking about building the components of the R1 series that have not been open sourced by DeepSeek--  reward models (OR5 and OR6) and CoT-SFT data generation scripts, the parts highlighted in green boxes on this helpful diagram ([source](https://www.reddit.com/r/LocalLLaMA/comments/1i66j4f/deepseekr1_training_pipeline_visualized/)):

<h1 align="center">
<img src="https://raw.githubusercontent.com/aolabsai/OpenReason/refs/heads/main/diagram.png">
</h1><br>

Let's flesh this out, collaborative Miro board link: https://miro.com/app/board/uXjVLi42Wug=/ Password: airebelfromrepo

Beyond the proven benefits of open source, for reasoning in particular building an open dataset like this makes sense if we want reasoning to improve over time. While some of this improvement is likely to be at the model level, a lot will depend on the data used for large-scale reinforcement; an open source effort ensures we collect as wide, as modern, and as unbiased data as possible.

Reasoning, after all, is a fluid quality– is it possible to be a reasoning agent if it cannot self-correct or re-learn? Re-training LLMs is not possible; the best we could do is provide up-to-date reasoning training data as more reasoning models are trained and deployed. We can help them stay current with the world and with our dynamic preferences.

Also, Large-scale RL data pipelines involve generating training data instead of scraping it, so with an open source effort we can generate data from multiple base models/LLMs at various temperatures.



### Projects Replicating R1 & Building New Reasoning Models:

- [Open-R1 by HuggingFace](https://github.com/huggingface/open-r1)
- [TinyZero by Jiaya Pan et al](https://github.com/Jiayi-Pan/TinyZero)


### Possible partners:

- Nomic.ai
- DAIR
- HuggingFace
- Meta / Llama
- Yoehi / BabyAGI
- OLlama


# Next steps:

- How we’d build it
   - seed repo with initial file structure/scripts
- Make issues
- Open some issues as bounties
- Share 
   - with possible open source partners
   - with developers



[Open source example of R1 by huggingface– see how much their data generation part is lacking](https://github.com/huggingface/open-r1?tab=readme-ov-file#data-generation).
