from openai import AzureOpenAI
import argparse
import os


def infer(model, client):
    while True:
        user_input = input("\n\nUser:")
        response = client.chat.completions.create(
            model=model, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": user_input}
                
            ]
        )
        for choice in response.choices:
            print(choice.message.content)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, default=None, help="your azure openai key.")
    parser.add_argument("--version", type=str, default=None, help="Your azure api version.")
    parser.add_argument("--endpoint", type=str, default=None, help="Your azure endpoint")
    parser.add_argument("--model", type=str, default='gpt-35-turbo', help="Your cloud model deployed on azure.")
    args = parser.parse_args()

    client = AzureOpenAI(
            api_key = (args.key),
            api_version = args.version,
            azure_endpoint = (args.endpoint)
        )

    infer(args.model, client)
        

if __name__=='__main__':
     main()