from flask import Flask, request, jsonify
from openai import AzureOpenAI
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os


persist_directory = None

app = Flask(__name__)

# Check if apiconfig.txt exists in the model folder
config_file_path = os.path.join('model', 'apiconfig.txt')
if not os.path.exists(config_file_path):
    # Create apiconfig.txt with default values
    with open(config_file_path, 'w') as file:
       file.write('Host=127.0.0.1\n')
       file.write('Port=5000\n')
       file.write('CertFile=""\n')
       file.write('CertKey=""\n')

# Read host and port from apiconfig.txt
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == 'Host':
                host = value
            elif key == 'Port':
                port = int(value)
            elif key == 'CertFile':
                cert_file = value.strip('"')
            elif key == 'CertKey':
                cert_key = value.strip('"')
else:
    print("File doesn't exist.")
    host = '127.0.0.1'
    port = 5000
    cert_file = ""
    cert_key = ""

print("Host:", host)
print("Port:", port)
print("CertFile:", cert_file)
print("CertKey:", cert_key)



@app.route('/v1/chat/completions', methods=['POST'])
def chat():

    global persist_directory
    global multimodal_model
    global agent
    global client
    global model
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
        response = client.chat.completions.create(
            model=model, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": prompt}
                
            ]
        )
        for choice in response.choices:
            return jsonify({"response": choice.message.content})

def main():
        global persist_directory
        global multimodal_model
        global agent
        global client
        global model
        parser = argparse.ArgumentParser()
        # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
        parser.add_argument("--key", type=str, default=None, help="your azure openai key.")
        parser.add_argument("--version", type=str, default=None, help="Your azure api version.")
        parser.add_argument("--endpoint", type=str, default=None, help="Your azure endpoint")
        parser.add_argument("--model", type=str, default='gpt-35-turbo', help="Your cloud model deployed on azure.")
        parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
        args = parser.parse_args()
        client = AzureOpenAI(
            api_key = (args.key),
            api_version = args.version,
            azure_endpoint = (args.endpoint)
        )
        model=args.model

        
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
