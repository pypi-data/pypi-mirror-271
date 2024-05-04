import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os


# Query the model
def infer(multimodal_model, agent):
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

    while True:
        user_input = input("\n\nUser:")
        docs = db.similarity_search(user_input,k=1)
        context=docs[0].page_content
        prompt = prompt_template.format(context=context, prompt=user_input)
        response = multimodal_model.generate_content(prompt)
        print(response.text)
# return response.text



def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
    parser.add_argument("--region", type=str, default=0.5, help="Your cloud provider region.")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
    args = parser.parse_args()
    # Initialize Vertex AI
    vertexai.init(project=args.projectid, location=args.region)
    # Load the model
    multimodal_model = GenerativeModel(model_name="gemini-1.0-pro-002")

    infer(multimodal_model, args.agent)

if __name__=='__main__':
     main()