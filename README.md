# LinkedIn Profile Analysis

## Project Description

This project is designed to analyze LinkedIn profiles by extracting user details and posts, then generating detailed analysis using OpenAI's GPT-4. The analysis includes technical content examination, engagement level assessment, trend identification, and more.

## Features

- **User Details Extraction**: Fetches LinkedIn user details such as name, profile summary, current role, education, and professional experiences.
- **Post Extraction**: Retrieves the latest posts from the LinkedIn profile.
- **AI-Powered Analysis**: Generates a comprehensive analysis of the LinkedIn profile using GPT-4, including content analysis, engagement assessment, trend identification, and professional goals inference.

## Technologies Used

- **Python**: Core programming language.
- **FastAPI**: Web framework for building the API.
- **Requests**: HTTP library for making API calls.
- **http.client**: Module for handling HTTP connections.
- **urllib.parse**: Library for URL parsing.
- **dotenv**: Module for loading environment variables.
- **OpenAI API**: For generating text using GPT-4.
- **RapidAPI**: For accessing LinkedIn data.

## Setup

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following:
    ```env
    OPENROUTER_API_KEY=your_openrouter_api_key
    OPENAI_API_KEY=your_openai_api_key
    RAPIDAPI_KEY=your_rapidapi_key
    ```

## Usage

1. **Run the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```

2. **Make a POST request to the API**:
    Use any API client (like Postman) or `curl` to make a POST request to the server with the LinkedIn profile URL in the request body:
    ```bash
    curl -X POST "http://127.0.0.1:8000/" -H "Content-Type: application/json" -d '{"query": "https://www.linkedin.com/in/username"}'
    ```

3. **View the Analysis**:
    The server will return a detailed analysis of the LinkedIn profile.

## Example

Here's an example of how to use the API:

1. **Request**:
    ```json
    {
        "query": "https://www.linkedin.com/in/johndoe"
    }
    ```

2. **Response**:
    ```json
    {
        "analysis": "Detailed LinkedIn Profile Analysis..."
    }
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines first.

## Acknowledgements

- [OpenAI](https://openai.com) for providing the GPT-4 API.
- [RapidAPI](https://rapidapi.com) for LinkedIn data access.

## Contact

For any questions or suggestions, please contact adcan288@gmail.com.
