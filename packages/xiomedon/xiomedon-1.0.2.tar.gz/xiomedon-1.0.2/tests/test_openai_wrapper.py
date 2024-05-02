from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env
import xiomedon as x
def test_invoke_openai_pakistan():
    assert x.invoke_openai("What is the capital of pakistan? Answer in one word") == "Islamabad"
def test_invoke_openai_pakistan():
    assert x.invoke_openai("What is the capital of Srilanka? Answer in one word") == "India"
