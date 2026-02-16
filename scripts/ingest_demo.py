import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from services.ingestion_service import ingest_document


doc = """
EU enterprise contracts longer than 3 years create
pricing renegotiation risks and regulatory exposure.
"""

count = ingest_document(
    doc,
    region="EU",
    segment="enterprise",
    source="EU Pricing Policy v3",
    page=2
)

print(f"Inserted {count} chunks")
