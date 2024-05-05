import os
from openai import AzureOpenAI
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


def infer(model, client, agent):
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    while True:
        user_input = input("\n\nUser:")
        docs = db.similarity_search(user_input,k=1)
        context=docs[0].page_content
        prompt = prompt_template.format(context=context, prompt=user_input)
        response = client.chat.completions.create(
            model=model, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": prompt}
                
            ]
        )
        for choice in response.choices:
            print(choice.message.content)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--key", type=str, default=None, help="your azure openai key.")
    parser.add_argument("--version", type=str, default=None, help="Your azure api version.")
    parser.add_argument("--endpoint", type=str, default=None, help="Your azure endpoint")
    parser.add_argument("--model", type=str, default='gpt-35-turbo', help="Your cloud model deployed on azure.")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
    args = parser.parse_args()

    client = AzureOpenAI(
        api_key = (str(args.key)),
        api_version = str(args.version),
        azure_endpoint = (str(args.endpoint))
    )


    infer(args.model, client, args.agent)

if __name__=='__main__':
     main()
