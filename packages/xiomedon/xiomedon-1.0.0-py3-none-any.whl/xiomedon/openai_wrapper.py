from openai import OpenAI
client = OpenAI()
def invoke_openai(prompt):
    sys_prompt = "You are a helpful assistant that always answers questions."
    res = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return res.choices[0].message.content