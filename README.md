TinyGen

TinyGen is a FastAPI application that generates unified diffs based on a given GitHub repository and a textual command. It utilizes the OpenAI API to generate the diffs and perform a reflection step to ensure the accuracy of the generated diffs.

Prerequisites

Before running the TinyGen application, ensure that you have the following prerequisites installed on your Mac OS machine:
* Python 3.7 or higher
* pip package manager
* Virtualenv

Setup Instructions

Follow these steps to set up and run the TinyGen application on your Mac OS machine:
1. Clone the repository:   git clone https://github.com/nancycheng028/tinygen.git
2. Navigate to the project directory:   cd tinygen  
3. Create a virtual environment:   python3 -m venv tinygen_venv  
4. Activate the virtual environment:   source tinygen_venv/bin/activate  
5. Install the required dependencies:   pip install -r requirements.txt

Running the API Locally
To run the TinyGen API locally, follow these steps:
1. Make sure you are in the project directory (tinygen) and the virtual environment is activated.
2. Set the OpenAI API key as an environment variable:     export OPENAI_API_KEY="your-api-key"   Replace "your-api-key" with your actual OpenAI API key.
3. Start the FastAPI server:     uvicorn main:app --reload  
4. The API will be accessible at http://localhost:8000/generate_diff.

Accessing the API
To generate a unified diff using the TinyGen API, you can send a POST request to the /generate_diff endpoint with the following JSON payload:
json
{
  "repoUrl": "https://github.com/jayhack/llm.sh",
  "prompt": "The program doesn't output anything in Windows 10 "
}
Replace "https://github.com/jayhack/llm.sh" with the URL of the GitHub repository you want to use, and adjust the "prompt" as needed.

You can use tools like cURL or Postman to send the POST request to the API endpoint.
Example using cURL:
curl -X POST -H "Content-Type: application/json" -d '{"repoUrl": "https://github.com/jayhack/llm.sh", "prompt": "The program doesn't output anything in Windows 10"}' http://localhost:8000/generate_diff

The API will respond with the generated unified diff as a JSON object.

Troubleshooting
If you encounter any issues or errors while setting up or running the TinyGen application, please refer to the error messages and logs for troubleshooting. Common issues include:
* Missing dependencies: Ensure that all the required dependencies are installed correctly.
* OpenAI API key not set: Make sure you have set the OpenAI API key as an environment variable before running the application.
* OpenAI API quota exceeded: If you receive an error indicating that you have exceeded your OpenAI API quota, you may need to upgrade your plan or wait for the quota to reset.
If you need further assistance, please open an issue on this GitHub repository, and we'll be happy to help you.
