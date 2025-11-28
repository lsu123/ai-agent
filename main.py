import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions
from prompts import system_prompt

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose:
        #print(f"User prompt: {user_prompt}")
        #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        # (then do the parts[0] checks, print result if verbose, append to list...)
    
    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")

def main():
    print("Hello from ai-agent!")
    load_dotenv()
    verbose = "--verbose" in sys.argv   # <- define verbose here
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        generate_content(client, messages, verbose)
    else:
        print("No prompt provided. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
