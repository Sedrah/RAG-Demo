def chunk_document(text, chunk_size=300, overlap=50):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        chunk_words = words[start:start + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks
