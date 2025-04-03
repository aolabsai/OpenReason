from collections import Counter
from functools import partial
import random

import datasets
from decontaminate_util import *

from functools import partial
from huggingface_hub import login
from R-Null import combined 

#loading key
with open("D:/AO/S1/OpenReason/hugging_key.txt", "r") as file:
    key = file.read().strip()

print(f"Token: {key}")  # Check if the token looks correct
login(key)



# All datasets have the same columns
DS_COLUMNS = {"question", "solution", "cot_type", "source_type", "metadata"}


def load_numinamath(sample_limit=None):
    ds = datasets.load_dataset("AI-MO/NuminaMath-CoT", trust_remote_code=True)["train"]
    ds_aops = ds.filter(lambda x: x["source"] == "aops_forum")
    ds = datasets.concatenate_datasets([ds, ds_aops])
    
    ds = ds.map(lambda x: {
        "question": x.pop("problem"),
        "solution": x.pop("solution"),
        "cot_type": "math",
        "source_type": "AI-MO/NuminaMath-CoT/" + x["source"],
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds


def load_theoremqa(sample_limit=None):
    ds = datasets.load_dataset("TIGER-Lab/TheoremQA", trust_remote_code=True)["test"]
    ds = ds.filter(lambda x: x["Picture"] is None)

    ds = ds.map(lambda x: {
        "question": x.pop("Question"),
        "solution": x.pop("Answer"),
        "cot_type": "math",
        "source_type": "TIGER-Lab/TheoremQA/" + x['Answer_type'],
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds


def load_generic(name, split, question_field="question", solution_field="solution", cot_type="math", version_tag=None, sample_limit=None):
    conf = "gpqa_diamond" if name == "Idavidrein/gpqa" else None
    ds = datasets.load_dataset(name, conf, token=key, trust_remote_code=True)[split]

    ds = ds.map(lambda x: {
        "question": x.pop(question_field),
        "solution": x.pop(solution_field, None),
        "cot_type": cot_type,
        "source_type": name,
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds

def load_scieval():
    """
    Category Physics; Task: SocraticQA
    What is the moment of inertia of a pendulum with a mass of $2 kg$ that is $7  m$ from the pivot?\n\nA. 56 kgm^2\nB. 196 kgm^2\nC. 84 kgm^2\nD. 98 kgm^2\n\nAnswer:

    Category Chemistry; Task: SocraticQA
    What is the molecular geometry of the $PF_3$ molecule?\n\nA. Trigonal planar\nB. Bent\nC. Trigonal pyramidal\nD. Tetrahedral\n\nAnswer:
    Category Chemistry; Task: reagent selection
    Given the rest of reaction components:\nreactant 1: Ic1ccc2ncccc2c1\nreactant 2: Cc1ccc2c(cnn2C2CCCCO2)c1B1OC(C)(C)C(C)(C)O1\nligand: c1ccc(P(c2ccccc2)c2ccccc2)cc1\nbase: C(=O)(O)[O-].[Na+]  \nSolvent list for selection:\nC1CCOC1,CN(C)C=O,CO\nOptimal solvent:

    Category Biology; Task: MedQA
    A 74-year-old man was admitted to the intensive care ward due to progressive dyspnea, cough with pink sputum, and diaphoresis. He had 2 myocardial infarctions at the age of 66 and 69 years and suffers from chronic heart failure. At the time of presentation, his vital signs are as follows: blood pressure 90/50 mm Hg, heart rate 108/min, respiratory rate 29/min, and temperature 35.5°C (95.9°F). On physical examination, the patient sits upright. He is lethargic and cyanotic. Lung auscultation reveals widespread bilateral fine rales. Cardiac examination is significant for S3, accentuation of the pulmonic component of S2, and a systolic murmur heard best at the apex of the heart. Soon after hospitalization, the patient develops ventricular fibrillation and dies despite adequate resuscitation measures. Which microscopic finding would you expect to see in this patient on autopsy?\n\nA. Brownish inclusions in the pulmonary macrophages on H&E staining\nB. Positive Prussian-blue staining of the kidney tissue\nC. Ground-glass hepatocytes\nD. Positive Congo-red staining of the cardiac tissue\n\nAnswer:
    Category Biology; Task: PubMedQA
    Polymorphisms in the oestrogen receptor 1 (ESR1) and oestrogen receptor 2 (ESR2) genes are associated with intermediate or endpoint markers of cardiovascular disease and with the efficacy of postmenopausal hormone therapy (HT). Contradictory findings have been described in the past and the role of these genetics variants remains unclear.\nA cross-sectional study was carried out with 266 postmenopausal women, of whom 115 received oral HT (HT+) and 151 did not receive any HT (HT-). We analysed three single-nucleotide polymorphisms (SNPs) in ESR1 (rs1801132, rs7757956 and rs2813544) and two in ESR2 (rs3020450 and rs7154455) and derived haplotypes with three additional polymorphisms that had been previously investigated by our group (ESR1 rs2234693 and ESR2 rs1256049 and rs4986938).\nThe ESR1 rs2813544 polymorphism was associated with low-density lipoprotein cholesterol (LDL-C) in HT+ postmenopausal women (p\u2009=\u20090.044; pC\u2009=\u20090.388), while one ESR2 gene haplotype was associated with total cholesterol (T-chol) (p\u2009=\u20090.015; pC\u2009=\u20090.090) and LDL-C in HT+ postmenopausal women (p\u2009=\u20090.021; pC\u2009=\u20090.126).\n\nAre polymorphisms in oestrogen receptors genes associated with lipid levels in response to hormone therapy?\n\nAnswer:
    Category Biology; Task: SocraticQA
    What substance is transported across the inner membrane of the mitochondria?\n\nA. Glucose\nB. Protons\nC. Oxygen\nD. Electrons\n\nAnswer:
    """
    ds = datasets.load_dataset("OpenDFM/SciEval", trust_remote_code=True)
    ds = datasets.concatenate_datasets([ds['test'], ds['validation']])
    # As there's enough samples, filter out ones without answer (13011 out of 27533)
    ds = ds.filter(lambda x: x["answer"] is not None)
    # Remove the "\n\nAnswer:"; Replace "\nOptimal solvent:" with "\nWhat is the optimal solvent?"; "\nOptimal ligand:" with "\nWhat is the optimal ligand?"; "\nOptimal reactant" with "\nWhat is the optimal reactant?"
    def clean_question(x):
        x["question"] = x["question"].split("\n\nAnswer:")[0].replace("\nOptimal solvent:", "\nWhat is the optimal solvent?").replace("\nOptimal ligand:", "\nWhat is the optimal ligand?").replace("\nOptimal reactant:", "\nWhat is the optimal reactant?")
        return x
    ds = ds.map(clean_question)
    task_to_o1domain = {"SocraticQA": "science", "reagent selection": "science", "MedQA": "health science", "PubMedQA": "health science"}
    ds = ds.map(lambda x: {"question": x.pop("question"), "solution": x.pop("answer")[0], "cot_type": task_to_o1domain[x['task_name']], "source_type": "OpenDFM/SciEval/" + x['category'] + "/" + x['type'] + "/" + x['task_name'], "metadata": str(x)})
    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])
    # ds = ds.shuffle(seed=42).select(range(len(ds) // 4))
    return ds


def select_examples_scieval(ds, n_examples):
    import math
    tasks = set([eval(x)['task_name'] for x in ds['metadata']])
    tasks_to_num_samples = {task: math.ceil(n_examples / len(tasks)) for task in tasks}
    
    # Only SocraticQA has topics
    topics = set([eval(x)['topic'] for x in ds['metadata']])
    socratic_qa_samples = tasks_to_num_samples.get("SocraticQA", 0)
    topics_to_num_samples = {topic: math.ceil(socratic_qa_samples / len(topics)) for topic in topics}
    
    selected_examples = []
    ds = ds.shuffle(seed=42)
    
    for i, ex in enumerate(ds):
        meta = eval(ex['metadata'])
        
        if meta['topic'] in topics and topics_to_num_samples[meta['topic']] > 0:
            selected_examples.append(ex)
            topics_to_num_samples[meta['topic']] -= 1
            tasks_to_num_samples["SocraticQA"] -= 1
        
        if meta['task_name'] in tasks and tasks_to_num_samples[meta['task_name']] > 0:
            selected_examples.append(ex)
            tasks_to_num_samples[meta['task_name']] -= 1
        
        if len(selected_examples) == n_examples:
            break

    return datasets.Dataset.from_list(selected_examples)

def decontaminate_train_data(train_questions, test_questions, ds, ngram_size=8):    
    # Build ngram lookups
    train_lookup = build_ngram_lookup(train_questions, ngram_size)
    test_lookup = build_ngram_lookup(test_questions, ngram_size)

    # Find contaminated questions
    contaminated_ids = find_contaminated_questions(train_lookup, test_lookup)

    # Remove contaminated examples
    not_contaminated_ids = set(range(len(train_questions))) - contaminated_ids
    ds = ds.select(list(not_contaminated_ids))
    print(f"\nDecontamination Results:")
    print(f"Total train questions: {len(train_questions)}")
    print(f"Contaminated questions: {len(contaminated_ids)}")
    print(f"Contamination rate: {(len(contaminated_ids)/len(train_questions)*100):.2f}%")
    print(f"Clean examples remaining: {len(ds)}")
    return ds


def load_olympiad_bench():
    # Only EN & TO (text-only); Both OE (open-ended) and TP (Theorem proof)
    confs = ["OE_TO_maths_en_COMP", "OE_TO_physics_en_COMP", "TP_TO_maths_en_COMP", "TP_TO_physics_en_COMP"]
    # Multimodal: "OE_MM_maths_en_COMP", "OE_MM_physics_en_COMP", "TP_MM_maths_en_COMP", "TP_MM_physics_en_COMP"
    ds = [datasets.load_dataset("Hothan/OlympiadBench", c, trust_remote_code=True)['train'] for c in confs]
    ds = datasets.concatenate_datasets(ds)
    ### TODO: Is solution ever longer than 1?
    ### TODO: forgot to add context to question
    # The physics one is also rather math-heavy
    ds = ds.map(lambda x: {"question": x.pop("question"), "solution": x.pop("solution")[0], "cot_type": "math", "source_type": "Hothan/OlympiadBench/" + x['question_type'] + "/" + x['subject'], "metadata": str(x)})
    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])
    return ds


def load_gpqa_extended(sample_limit=None):
    gpqa_to_o1domain = {"Chemistry": "science", "Biology": "science", "Physics": "science"}
    ds = datasets.load_dataset("Idavidrein/gpqa", "gpqa_extended", token=key, trust_remote_code=True)['train']
    
    # Filter against diamond
    ds_diamond = datasets.load_dataset("Idavidrein/gpqa", "gpqa_diamond", token=key, trust_remote_code=True)['train']
    ds = ds.filter(lambda x: x["Question"] not in ds_diamond["Question"])

    ds = ds.map(lambda x: {
        "question": x.pop("Question"),
        "solution": x.pop("Explanation"),
        "cot_type": gpqa_to_o1domain[x['High-level domain']],
        "source_type": "Idavidrein/gpqa",
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds


def load_usaco(sample_limit=None):
    ds = datasets.load_dataset("codegenning/usacobench_formatted")['test']
    ds = ds.map(lambda x: {
        "question": x.pop("question").strip(),
        "solution": None,
        "cot_type": "coding",
        "source_type": "codegenning/usacobench_formatted",
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds


def load_numinamath_tir(sample_limit=None):
    ds = datasets.load_dataset("AI-MO/NuminaMath-TIR", trust_remote_code=True)["train"]

    ds = ds.map(lambda x: {
        "question": x.pop("problem"),
        "solution": x.pop("solution"),
        "cot_type": "math",
        "source_type": "AI-MO/NuminaMath-TIR",
        "metadata": str(x)
    })

    ds = ds.remove_columns([c for c in ds.column_names if c not in DS_COLUMNS])

    # Apply sample limit
    if sample_limit is not None:
        ds = ds.select(range(min(sample_limit, len(ds))))

    return ds



def extract_question_dolphin(messages):
        for msg in messages:
            if msg["role"] == "user":
                return msg["content"]
        return "" 

def load_dolphin_r1(sample_limit=None):
    # Load the dataset with the correct config name
    ds = datasets.load_dataset("cognitivecomputations/dolphin-r1", "reasoning-deepseek", trust_remote_code=True, split="train")
    
    # Transform dataset
    ds = ds.map(lambda x: {
        "question": extract_question_dolphin(x["messages"]), 
        "solution": x["answer"],
        "cot_type": "math",
        "source_type": "cognitivecomputations/dolphin-r1",
        "metadata": str({"reasoning": x.get("reasoning", "")})
    })
    
    # Retain only required columns
    ds = ds.remove_columns(set(ds.column_names) - set(DS_COLUMNS))
    
    # Apply sample limit
    if sample_limit:
        ds = ds.select(range(min(sample_limit, len(ds))))
    
    return ds




# DS_TO_SELECTION = {
#     # Name: [load function, selection function, #samples]
#     # Take all (720)
#     "TheoremQA": [load_theoremqa, None, None],
#     # Pretty big (434,778) and unclear how high quality so take 500
#     "NuminaMath": [load_numinamath, None, 500],
#     # Take all as super high-quality (3329)
#     # "Omni-MATH": [partial(load_generic, name="KbsdJames/Omni-MATH", question_field="problem", split="test"), select_examples_omni_math, None],
#     "Omni-MATH": [partial(load_generic, name="KbsdJames/Omni-MATH", question_field="problem", split="test"), None, None],
#     # Not super diverse (only 4 subtasks which same question format) so do not take all (14228)
#     "SciEval": [load_scieval, select_examples_scieval, 250],
#     # Very high-quality so take all (626)
#     "OlympiadBench": [load_olympiad_bench, None, None],
#     # # Very high-quality so take all
#     "GPQA": [load_gpqa_extended, None, None],
#     # # Very high-quality so take all (520)
#     "USACO": [load_usaco, None, 520], 

#     "Dolphin-R1": [load_dolphin_r1, None, 200],

#     "NuminaMath-TIR": [load_numinamath_tir, None, 500],
# }

DS_TO_SELECTION = {
    "TheoremQA": [partial(load_theoremqa, sample_limit=None), None, None],
    "NuminaMath": [partial(load_numinamath, sample_limit=500), None, None],
    "Omni-MATH": [partial(load_generic, name="KbsdJames/Omni-MATH", question_field="problem", split="test", sample_limit=500), None, None],
    "SciEval": [load_scieval, select_examples_scieval, 250],
    "OlympiadBench": [load_olympiad_bench, None, None],
    "GPQA": [partial(load_gpqa_extended, sample_limit=500), None, None],
    "USACO": [partial(load_usaco, sample_limit=520), None, None],
    "Dolphin-R1": [partial(load_dolphin_r1, sample_limit=200), None, None],
    "NuminaMath-TIR": [partial(load_numinamath_tir, sample_limit=500), None, None],
}


if __name__ == "__main__":
    random.seed(42)
    
    ds_all = []
    for ds_name, (load_fn, selection_fn, n_samples) in DS_TO_SELECTION.items():
        print(f"Processing {ds_name}...")
        ds = load_fn()
        
        if selection_fn:
            # Outdated, needs to be updated
            if ds_name == "Omni-MATH":
                ds_list = list(ds)
                selected_examples, selected_subdomains, selected_difficulties = selection_fn(ds_list, n_samples)
                ds = datasets.Dataset.from_list(selected_examples)
            else:
                ds = selection_fn(ds, n_samples)
        else:
            ds = ds.shuffle(seed=42)
            if n_samples:
                ds = ds.select(range(min(n_samples, len(ds)))) 
        ds_all.append(ds)
    
    ds = datasets.concatenate_datasets(ds_all)
    
    # Add empty/none cot column
    ds = ds.map(lambda x: {"cot": combined.answer(x["question"])[1], **x})
    
    # Simple deduplication
    memory = set()
    def is_unique(elem, column, memory):
        if elem[column] in memory: return False
        memory.add(elem[column])
        return True

    # Drop duplicates in `ds` on "question"
    ds = ds.filter(partial(is_unique, column="question", memory=memory))
    
    ds.push_to_hub("aolabs/OR_verified", token=key)
