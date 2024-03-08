from fastapi import FastAPI, Request
from pydantic import BaseModel
from github import Github
import openai
import os
from fastapi.responses import JSONResponse
from openai.error import OpenAIError, RateLimitError
import logging

app = FastAPI()

class InputData(BaseModel):
    repoUrl: str
    prompt: str

def get_repo_contents(repo_url):
    # Extract the repository owner and name from the URL
    owner, repo_name = repo_url.split('/')[-2:]
    
    # Create a GitHub API client
    g = Github()
    
    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")
    
    # Get the repository contents
    contents = repo.get_contents("")
    
    # Return the contents as a dictionary
    return {
        content.path: content.decoded_content.decode("utf-8") 
        for content in contents
        if content.encoding == "base64"
    }


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_diff(repo_contents, prompt):
    # Combine the repository contents into a single string
    code = "\n".join(repo_contents.values())
    
    # Log the API request details
    logger.info(f"Sending API request to OpenAI with model: text-davinci-003, prompt: {prompt}")
    
    try:
        # Call the OpenAI API to generate the diff
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"{code}\n\n{prompt}\n\nHere are the changes to make:",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        
        # Print the API response
        print("OpenAI API response:", response)
        
        diff = response.choices[0].text.strip()
        
        # Run the reflection step
        reflection_prompt = f"Here is the generated diff:\n\n{diff}\n\nAre you sure this is correct, or would you like to make any corrections?"
        reflection_response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=reflection_prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        
        # Print the reflection API response
        print("Reflection API response:", reflection_response)
        
        reflection = reflection_response.choices[0].text.strip()
        
        if "correct" in reflection.lower():
            return diff
        else:
            # Generate a new diff based on the reflection
            new_diff_response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=f"{code}\n\n{prompt}\n\nHere are the updated changes based on the reflection:\n\n{reflection}\n\nUpdated diff:",
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            )
            
            # Print the new diff API response
            print("New diff API response:", new_diff_response)
            
            new_diff = new_diff_response.choices[0].text.strip()
            return new_diff
    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Error occurred while generating diff: {e}")
        raise
@app.post("/generate_diff")
async def generate_diff_endpoint(input_data: InputData):
    try:
        repo_contents = get_repo_contents(input_data.repoUrl)
        diff = generate_diff(repo_contents, input_data.prompt)
        return {"diff": diff}
    except RateLimitError:
        # This specific block handles rate limit errors from OpenAI
        return JSONResponse(
            status_code=429,
            content={"message": "API request limit exceeded. Please try again later."}
        )
    except OpenAIError as e:
        # This block can catch other OpenAI API errors
        print(f"OpenAIError encountered: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred with the OpenAI service."}
        )
    except Exception as e:
        # This block catches all other unforeseen errors
        print(f"An unexpected error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred. Please try again."}
        )