from infrastructure.openai_client import get_openai_client

client = get_openai_client()


def generate_answer(prompt):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
