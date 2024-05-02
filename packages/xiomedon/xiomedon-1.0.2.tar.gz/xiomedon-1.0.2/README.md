# xiomedon

Library to call Open AI gpt3.5t-turbo and collect reponses and check for Accuracy

## Features

- `v0.0.1` Call Open AI gpt3.5 and fetch respones

## Installation

1. Download and install the latest version of [python](https://www.python.org/downloads/). Open a terminal and check that it is installed.

   Windows
   ```
   py --version
   ```

   Linux/MAC OS
   ```
   python3 --version
   ```

2. Make sure you have upgraded version of pip.

   Windows
   ```
   py -m pip install --upgrade pip
   ```

   Linux/MAC OS
   ```
   python3 -m pip install --upgrade pip
   ```

3. Install xiomedon using pip.

   Windows
   ```
   pip install xiomedon
   ```

   Linux/MAC OS
   ```
   python3 -m pip install xiomedon
   ```

4. Check that the package was installed

   ```
   pip show xiomedon
   ```

## Usage


   ```
   import os
   import xiomedon as x

   # Set your OpenAI API key
   os.environ["OPENAI_API_KEY"] = "your-openai-key"

   # 'xiomedon` provides a function `invoke_openai` caling gpt3.5 turbo  and returns string with response
   response = x.invoke_openai("what is the capital of Austria?")
   print(response)

   ```
 