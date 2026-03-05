import streamlit as st
import ollama
import numpy as np

st.set_page_config(page_title="RAG QA System", page_icon="🤖")

st.title("📚 RAG Question Answering System")
st.write("Ask questions from NLP, ML, and DL documents")


# 1 Load Documents 
# -----------------------------


def load_and_embed():

    files = ["nlp.txt", "ml.txt", "DL.txt"]

    all_text = ""

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            all_text += f.read() + "\n"

    # Chunking
    chunk_size = 500
    overlap = 50
    chunks = []

    for i in range(0, len(all_text), chunk_size - overlap):
        chunk = all_text[i:i + chunk_size]
        chunks.append(chunk)

    # Create embeddings
    embeddings = []

    for chunk in chunks:
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )
        embeddings.append(response["embedding"])

    embeddings = np.array(embeddings)

    return chunks, embeddings


chunks, embeddings = load_and_embed()


# 2 Cosine Similarity
# -----------------------------

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 3 Retrieve Relevant Chunks
# -----------------------------

def retrieve_chunks(query, top_k=5):

    query_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

    similarities = []

    for emb in embeddings:
        sim = cosine_similarity(query_embedding, emb)
        similarities.append(sim)

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = [chunks[i] for i in top_indices]

    return results



# 4️ Generate Answer
# -----------------------------

def generate_answer(question):

    context = retrieve_chunks(question)

    context_text = "\n\n".join(context)

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

Context:
{context_text}

Question:
{question}

Answer:
"""

    response = ollama.generate(
        model="gemma3:1b",
        prompt=prompt
    )

    return response["response"]



# 5️ Streamlit UI
# -----------------------------

user_question = st.text_input("Ask a question:")

if st.button("Get Answer"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            answer = generate_answer(user_question)

        st.success("Answer:")
        st.write(answer)