# Description: This script demonstrates how to use the OpenAI Retrieval-Augmented Generation
# (RAG) API to build a simple question-answering system.

import openai
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set your OpenAI API key
from dotenv import load_dotenv
import os

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

VECTOR_DB = []


def load_dataset(file_path):
    with open(file_path, "r") as file:
        dataset = [line.strip() for line in file.readlines() if line.strip()]
    print(f"Loaded {len(dataset)} facts from the dataset.")
    return dataset


def get_embedding(text, model="text-embedding-3-small"):
    response = openai.Embedding.create(input=text, model=model)
    return response["data"][0]["embedding"]


def add_to_db(chunk):
    embedding = get_embedding(chunk)
    VECTOR_DB.append((chunk, embedding))


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, top_n=5):
    query_embedding = get_embedding(query)
    similarities = [
        (chunk, cosine_similarity(query_embedding, embedding))
        for chunk, embedding in VECTOR_DB
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return query_embedding, similarities[:top_n]


def visualize_embeddings(query, query_embedding, retrieved_chunks):
    data = []
    for chunk, similarity in retrieved_chunks:
        truncated_chunk = chunk[:50] + "..." if len(chunk) > 50 else chunk
        data.append({"Chunk": truncated_chunk, "Similarity": similarity})
    df = pd.DataFrame(data)

    print("\nSimilarities with Query:")
    print(df)

    plt.figure(figsize=(12, 6))
    plt.barh(df["Chunk"], df["Similarity"], color="skyblue")
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Text Chunks")
    plt.title(f"Cosine Similarities with Query: '{query}'")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return


def generate_response(query):
    query_embedding, retrieved_chunks = retrieve(query, top_n=5)
    visualize_embeddings(query, query_embedding, retrieved_chunks)

    if not retrieved_chunks or retrieved_chunks[0][1] < 0.5:
        return "No relevant information found."

    context = "\n".join(f" - {chunk}" for chunk, _ in retrieved_chunks)
    prompt = (
        f"You are a helpful assistant. Use only the following pieces of context to answer "
        f"the question. Don't make up any new information:\n{context}\n\n"
        f"User Query: {query}\nAnswer:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"].strip()


def main():
    file_path = "EM 624 Informatics for Engineering.txt"
    dataset = load_dataset(file_path)

    print("Indexing data into the vector database...")
    for fact in dataset:
        add_to_db(fact)
    print("Indexing complete.")

    print("\nAsk the assistant questions! Type 'exit' to quit.")
    while True:
        query = input("\nEnter your query: ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break
        response = generate_response(query)
        print("\nAssistant Response:")
        print(response)


if __name__ == "__main__":
    main()
