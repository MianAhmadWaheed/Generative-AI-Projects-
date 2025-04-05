import os
import json
import re
from glob import glob
import streamlit as st
from rank_bm25 import BM25Okapi
from transformers import pipeline

#########################
# Data Loading Functions
#########################


def load_samples(data_dir):
    """
    Walks through the samples directory and loads all JSON files.
    Assumes the folder structure:
      data_dir/samples/<Disease Category>/<PDD Category>/*.json
    """
    pattern = os.path.join(data_dir, "samples", "*", "*", "*.json")
    file_list = glob(pattern)
    samples = []
    for file in file_list:
        with open(file, "r") as f:
            sample = json.load(f)
            samples.append(sample)
    return samples


def extract_text_from_sample(sample):
    """
    Extracts the clinical note text from the sample.
    Assumes that the keys "input1" to "input6" contain the note segments.
    """
    keys = ["input1", "input2", "input3", "input4", "input5", "input6"]
    texts = [sample.get(key, "") for key in keys]
    return " ".join(texts)


def load_kg(data_dir):
    """
    Loads all knowledge graph JSON files from the diagnostic_kg directory.
    Assumes the folder structure:
      data_dir/diagnostic_kg/*.json
    """
    pattern = os.path.join(data_dir, "diagnostic_kg", "*.json")
    file_list = glob(pattern)
    kg_dict = {}
    for file in file_list:
        with open(file, "r") as f:
            kg = json.load(f)
            # Use the filename (without extension) as the disease category key.
            disease = os.path.basename(file).replace(".json", "")
            kg_dict[disease] = kg
    return kg_dict


def kg_to_text(kg):
    """
    Converts the knowledge graph JSON structure into a flat text string.
    Here we focus on the "knowledge" key, which contains the premises.
    """
    knowledge = kg.get("knowledge", {})
    texts = []
    for key, value in knowledge.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                texts.append(f"{key}: {subvalue}")
        else:
            texts.append(f"{key}: {value}")
    return " ".join(texts)


#########################
# Text Processing Helpers
#########################


def simple_tokenize(text):
    """
    Tokenizes text using regex instead of NLTK's punkt.
    Removes punctuation and splits on whitespace.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return tokens


#########################
# BM25 Retrieval Functions
#########################


def retrieve_documents(query, bm25, tokenized_docs, doc_texts, top_k=3):
    """
    Tokenizes the query, computes BM25 scores, and returns the top_k document texts.
    """
    tokenized_query = simple_tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
        :top_k
    ]
    retrieved_docs = [doc_texts[i] for i in top_indices]
    return retrieved_docs


def retrieve_kg_context(query, kg_bm25, kg_entries, top_k=1):
    """
    Tokenizes the query, computes BM25 scores for the knowledge graph entries,
    and returns the concatenated text of the top matching kg context.
    """
    tokenized_query = simple_tokenize(query)
    scores = kg_bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
        :top_k
    ]
    retrieved_kg = [kg_entries[i][1] for i in top_indices]
    return " ".join(retrieved_kg)


#########################
# Answer Generation Functions
#########################

# Initialize the text generation pipeline.
# You can choose another model if preferred.
generator = pipeline("text2text-generation", model="t5-small")


def generate_answer(query, retrieved_docs, kg_context):
    """
    Combines the query, the retrieved clinical note context, and the knowledge graph context
    to form a prompt, then generates an answer using a text generation pipeline.
    """
    context = " ".join(retrieved_docs) + " " + kg_context
    prompt = f"Question: {query} Context: {context} Answer:"
    generated = generator(prompt, max_length=200)[0]["generated_text"]
    return generated


def answer_query(
    query,
    bm25,
    tokenized_docs,
    doc_texts,
    kg_bm25,
    kg_entries,
    top_k_docs=3,
    top_k_kg=1,
):
    retrieved_docs = retrieve_documents(
        query, bm25, tokenized_docs, doc_texts, top_k=top_k_docs
    )
    kg_context = retrieve_kg_context(query, kg_bm25, kg_entries, top_k=top_k_kg)
    answer = generate_answer(query, retrieved_docs, kg_context)
    return answer, retrieved_docs, kg_context


#########################
# Main Application Logic
#########################


def main():
    st.title("Clinical Query Answering with Knowledge Graph")

    # Set the data directory (assuming the structure is in the current directory).
    data_dir = "."

    st.info("Loading annotated clinical notes...")
    samples = load_samples(data_dir)
    doc_texts = [extract_text_from_sample(s) for s in samples]

    # Build BM25 index for clinical notes.
    tokenized_docs = [simple_tokenize(doc) for doc in doc_texts]
    bm25 = BM25Okapi(tokenized_docs)

    st.info("Loading diagnostic knowledge graphs...")
    kg_dict = load_kg(data_dir)
    # Prepare a list of (disease, text) entries for knowledge graphs.
    kg_entries = []
    for disease, kg in kg_dict.items():
        text = kg_to_text(kg)
        kg_entries.append((disease, text))
    # Build BM25 index for knowledge graphs.
    kg_texts = [entry[1] for entry in kg_entries]
    kg_tokenized_docs = [simple_tokenize(text) for text in kg_texts]
    kg_bm25 = BM25Okapi(kg_tokenized_docs)

    st.success("Data loaded successfully!")

    # Streamlit input for query.
    query = st.text_input("Enter your clinical query:")

    if st.button("Get Answer") and query:
        with st.spinner("Retrieving and generating answer..."):
            answer, retrieved_docs, kg_context = answer_query(
                query, bm25, tokenized_docs, doc_texts, kg_bm25, kg_entries
            )
        st.subheader("Generated Answer")
        st.write(answer)

        st.subheader("Retrieved Clinical Note Excerpts")
        for i, doc in enumerate(retrieved_docs, start=1):
            st.markdown(f"**Document {i}:**")
            st.write(doc[:300] + " ...")

        st.subheader("Relevant Knowledge Graph Context")
        st.write(kg_context[:500] + " ...")


if __name__ == "__main__":
    main()
