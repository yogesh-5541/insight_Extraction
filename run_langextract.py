from langextract import extract
from langextract.data import ExampleData, Extraction, Document

# 1️⃣ Input documents (MUST be Document objects)
documents = [
    Document(
        document_id="doc1",
        text="On 15 September 2024, Suresh booked a train ticket for Rs. 850 from Chennai to Bangalore."
    )
]

# 2️⃣ Schema
schema = {
    "person": "Name of the person",
    "transaction_type": "Type of booking",
    "amount": "Amount paid",
    "date": "Date of transaction",
    "source": "From location",
    "destination": "To location"
}

# 3️⃣ Required example (correct & grounded)
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

# 4️⃣ Run extraction
result = extract(
    documents,
    schema,
    examples=examples
)

# print(result)


# Convert result to clean JSON-like dict
final_output = []

for doc in result:
    record = {}
    for ext in doc.extractions:
        record[ext.extraction_class] = ext.extraction_text
    final_output.append(record)

print("\nFINAL JSON OUTPUT:")
print(final_output)
