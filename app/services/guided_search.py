import json
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet

service_registry = []
with open("/content/servio_data.json", "r") as f:
    for line in f:
        try:
            # Attempt to parse each line as a JSON object
            data = json.loads(line.strip())
            service_registry.append(data)
        except json.JSONDecodeError as e:
            # Handle cases where a line is not valid JSON, e.g., empty lines or comments
            print(f"Warning: Skipping invalid JSON line: {line.strip()} - Error: {e}")


def load_model():
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return tokenizer, model

def expand_query(query):
    words = query.split()
    expanded_query = set(words)
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded_query.add(lemma.name().replace('_', ' '))
    return ' '.join(expanded_query)

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def retrieve_service(query, service_registry, tokenizer, model):
    expanded_query = expand_query(query)
    query_embedding = embed_text(expanded_query, tokenizer, model)
    registry_embeddings = [embed_text(service['docstring'], tokenizer, model) for service in service_registry]
    similarities = [cosine_similarity(query_embedding, emb)[0][0] for emb in registry_embeddings]
    best_match_idx = similarities.index(max(similarities))
    best_service = service_registry[best_match_idx]
    return best_service['func_name'], best_service['url'], best_service['docstring']

def chatbot():
    tokenizer, model = load_model()
    print("Welcome to the software service chatbot! I will ask a few questions to better understand your needs.")
    while True:
        service_type = input("What type of service are you looking for? ")
        features = input("Any specific features you need? ")
        query = f"Service type: {service_type}, Features: {features}"

        if service_type.lower() in ["exit", "quit"] or features.lower() in ["exit", "quit"]:
            break

        while True:
            func_name, url, docstring = retrieve_service(query, service_registry, tokenizer, model)
            print(f"Best match: {func_name}\nURL: {url}\nDescription: {docstring}")
            more_info = input("Would you like to refine your search? (yes/no): ")
            if more_info.lower() == "yes":
                refinement = input("Please provide additional details to refine your search: ")
                query += f", {refinement}"
            else:
                break

if __name__ == "__main__":
    chatbot()