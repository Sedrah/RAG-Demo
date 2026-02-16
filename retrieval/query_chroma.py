from infrastructure.collections import get_collection

collection = get_collection()



def query_collection(query_text):

    results = collection.query(
        query_texts=[query_text],
        n_results=5
    )
   

    return results
