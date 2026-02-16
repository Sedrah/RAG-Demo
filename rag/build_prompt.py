def build_prompt(context, query, confidence_label):

    return f"""
You are a pricing decision assistant.

Rules:
- Use ONLY provided context
- Always cite sources
- Highlight uncertainty if present

Overall Confidence Level: {confidence_label}

Context:
{context}

Question:
{query}

Answer:
"""
