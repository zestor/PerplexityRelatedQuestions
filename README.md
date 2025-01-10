# PerplexityRelatedQuestions

A Python-based tool designed to facilitate deep exploration of complex topics by generating and analyzing related questions. Leveraging the Perplexity.ai API and OpenAI's GPT-4, this tool recursively generates related questions up to a specified depth, retrieves detailed responses, and compiles the information for comprehensive analysis.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example](#example)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Recursive Question Generation**: Automatically generates related questions up to a specified depth to explore a topic thoroughly.
- **API Integration**: Utilizes Perplexity.ai for detailed responses and OpenAI's GPT-4 for generating related questions.
- **Rate Limiting**: Manages API rate limits to ensure compliant and efficient usage.
- **Result Logging**: Saves all generated questions and responses to a text file for easy reference and analysis.
- **Extensible Design**: Built with scalability in mind, allowing for easy integration of additional features or APIs.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7 or higher**: Ensure Python is installed on your system. You can download it from [here](https://www.python.org/downloads/).
- **API Keys**:
  - **OpenAI API Key**: Obtain from [OpenAI](https://platform.openai.com/account/api-keys).
  - **Perplexity.ai API Key**: Obtain from [Perplexity.ai](https://www.perplexity.ai/).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/question-explorer.git
   cd question-explorer
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application requires API keys for both OpenAI and Perplexity.ai. These should be set as environment variables.

1. **Set Environment Variables**

   - **Unix/Linux/macOS**

     ```bash
     export OPENAI_API_KEY='your-openai-api-key'
     export PERPLEXITY_API_KEY='your-perplexity-api-key'
     ```

   - **Windows**

     ```cmd
     set OPENAI_API_KEY=your-openai-api-key
     set PERPLEXITY_API_KEY=your-perplexity-api-key
     ```

2. **Alternatively, Create a `.env` File**

   You can create a `.env` file in the project root directory and add your API keys:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   PERPLEXITY_API_KEY=your-perplexity-api-key
   ```

   Ensure to install the `python-dotenv` package and load the `.env` file in your script if you choose this method.

## Usage

1. **Define Your Origin Question**

   Modify the `origin_question` variable in the `main()` function with the topic or question you wish to explore.

2. **Set Exploration Depth**

   Adjust the `depth` parameter to control how deep the exploration should go. A higher depth results in more extensive question generation but may increase API usage and runtime.

3. **Run the Script**

   Execute the script using Python:

   ```bash
   python main.py
   ```

4. **View Results**

   The script will generate a `perplexity_related_questions.txt` file containing all the related questions and their corresponding responses. Additionally, a summary of the responses will be printed to the console.

## Example

Here's an example of how the script operates:

1. **Origin Question**: A detailed concept or question is provided to initiate the exploration.
2. **Initial Response**: The Perplexity.ai API returns a comprehensive answer to the origin question.
3. **Related Questions**: OpenAI's GPT-4 generates five related questions based on the initial response.
4. **Recursive Exploration**: For each related question, the process repeats up to the specified depth.
5. **Output**: All questions and answers are logged to `perplexity_related_questions.txt`, and a summary is displayed.

**Sample Output:**

```
Related Question: How does dynamic precision allocation improve computational efficiency in large language models?
Research: Dynamic precision allocation optimizes computational resources by assigning varying levels of precision to tokens based on their importance, reducing memory usage and speeding up inference without significant loss in output quality.
Citations: [List of citations]

Related Question: What are the challenges in implementing dynamic precision allocation in neural network architectures?
Research: Implementing dynamic precision allocation involves challenges such as accurately determining token importance in real-time, managing precision transitions smoothly to avoid computational errors, and ensuring compatibility with existing hardware and software frameworks.
Citations: [List of citations]

...
```

## Project Structure

```
question-explorer/
├── main.py
├── requirements.txt
├── perplexity_related_questions.txt
├── README.md
└── .env (optional)
```

- **main.py**: The main script containing the implementation.
- **requirements.txt**: Lists all Python dependencies.
- **perplexity_related_questions.txt**: Generated file containing all related questions and responses.
- **README.md**: Project documentation.
- **.env**: (Optional) File to store environment variables.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Create a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

---

*Disclaimer: Ensure you comply with the usage policies of the APIs utilized in this project. Handle your API keys securely and avoid exposing them in public repositories.*
