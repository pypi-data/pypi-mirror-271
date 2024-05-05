import vertexai
from vertexai.generative_models import GenerativeModel
import argparse


# Query the model
def infer(multimodal_model):
    while True:
        user_input = input("\n\nUser:")
        response = multimodal_model.generate_content(user_input)
        print(response.text)
# return response.text



def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
    parser.add_argument("--region", type=str, default=None, help="Your cloud provider region.")
    parser.add_argument("--model", type=str, default='gemini-1.0-pro-002', help="Your cloud model deployed on VertexAI.")
    args = parser.parse_args()
    # Initialize Vertex AI
    vertexai.init(project=args.projectid, location=args.region)
    # Load the model
    multimodal_model = GenerativeModel(model_name=args.model)

    infer(multimodal_model)

if __name__=='__main__':
     main()