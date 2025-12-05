import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file_content import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
    )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    

    if response.function_calls:
        tool_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=args.verbose)
            parts = function_call_result.parts
            if not parts or not parts[0].function_response or not parts[0].function_response.response:
                raise Exception("Fatal error: Couldn't find tool response.")
            tool_responses.append(parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
    else:
        print("Response:")
        print(response.text)

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)
        

if __name__ == "__main__":
    main()
