from flask import Flask, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel
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
        return jsonify({"response": response})

def main():
        global persist_directory
        global multimodal_model
        global agent
        parser = argparse.ArgumentParser()
        parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
        parser.add_argument("--region", type=str, default=0.5, help="Your cloud provider region.")
        parser.add_argument("--agent", type=str, help="Name of the agent to query.")
        parser.add_argument("--model", type=str, default=0.5, help="Your cloud model on VertexAI.")
        args = parser.parse_args()
        agent=args.agent
        persist_directory = os.path.join('db', agent)
        vertexai.init(project=args.projectid, location=args.region)
        # Load the model
        multimodal_model = GenerativeModel(model_name=args.model)
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
