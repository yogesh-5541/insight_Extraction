from langextract import extract
from langextract.data import ExampleData, Extraction, Document

def extract_insights(text: str):
    documents = [
        Document(
            document_id="doc1",
            text=text
        )
    ]

    schema = {
        "person": "Name of the person",
        "transaction_type": "Type of booking",
        "amount": "Amount paid",
        "date": "Date of transaction",
        "source": "From location",
        "destination": "To location"
    }

    examples = [
        ExampleData(
            text="Ravi booked a bus ticket for Rs. 500 from Madurai to Trichy on 10 August 2024.",
            extractions=[
                Extraction("person", "Ravi"),
                Extraction("transaction_type", "bus ticket booking"),
                Extraction("amount", "Rs. 500"),
                Extraction("date", "10 August 2024"),
                Extraction("source", "Madurai"),
                Extraction("destination", "Trichy"),
            ]
        )
    ]

    result = extract(
        documents,
        schema,
        examples=examples
    )

    final_output = {}
    for doc in result:
        for ext in doc.extractions:
            final_output[ext.extraction_class] = ext.extraction_text

    return final_output
