import pandas as pd
import spacy
import re

# Load SpaCy model only once
nlp = spacy.load("en_core_web_sm")

# Load skills only once
skills_df = pd.read_csv("skills.csv")
SKILLS = (
    skills_df["skill"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .unique()
)


def extract_skills(text):

    if not text:
        return []

    # NLP preprocessing
    doc = nlp(text)

    processed_text = " ".join(
        token.lemma_.lower()
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
    )

    found_skills = []

    for skill in SKILLS:

        # Exact word/phrase matching
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, processed_text):
            found_skills.append(skill.title())

    return sorted(set(found_skills))