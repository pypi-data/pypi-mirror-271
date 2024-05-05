import os
from openai import AzureOpenAI
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


# key='ba810c12512c4efe83d3736a2014780e'
# version='2024-02-01'
# endpoint='https://allm.openai.azure.com/'

# global endpoint
# global key
# global version
# global model
config_file_path = os.path.join('model', 'azureopenaiconfig.txt')
if not os.path.exists(config_file_path):
    # Create apiconfig.txt with default values
    with open(config_file_path, 'w') as file:
        file.write('Endpoint=""\n')
        file.write('key=""\n')
        file.write('version=""\n')
        file.write('model=""\n')

# Read host and port from apiconfig.txt
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as file:
        for line in file:
            key1, value = line.strip().split('=')
            if key1 == 'Endpoint':
                endpoint = value
            elif key1 == 'key':
                key = value
            elif key1 == 'version':
                version = value
            elif key1 == 'model':
                model = value

keyy='ba810c12512c4efe83d3736a2014780e'
endpointt= 'https://allm.openai.azure.com/'
versionn='2024-02-01'

print(keyy, versionn,endpointt)

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
        api_key = (str(args.key) if args.key else str(keyy)),
        api_version = str(args.version) if args.version else str(versionn),
        azure_endpoint = (str(args.endpoint) if args.endpoint else str(endpointt))
    )

    final_model = model if model else args.model

    infer(final_model, client, args.agent)

if __name__=='__main__':
     main()
