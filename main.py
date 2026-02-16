import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function


def main():


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action = "store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]       
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    )
    client = genai.Client(api_key = api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=config,
        )
    
    tokens = ("Prompt tokens: " + str(response.usage_metadata.prompt_token_count) + "\nResponse tokens: " + str(response.usage_metadata.candidates_token_count))
    if args.verbose:
        
        print("User prompt: " + args.user_prompt)
        print(tokens)

    
    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, args.verbose)
            if not function_call_result.parts:
                raise Exception("No parts in function call result")
            if not function_call_result.parts[0].function_response:
                raise Exception("No function response object")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No function result present")

            function_results.append(function_call_result.parts[0])
        
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                
if __name__ == "__main__":
    main()
