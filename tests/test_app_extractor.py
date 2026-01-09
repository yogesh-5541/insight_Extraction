from app.extractor import extract_insights

def test_extract_insights_basic():
    text = "On 15 September 2024, Suresh booked a train ticket for Rs. 850 from Chennai to Bangalore."

    result = extract_insights(text)

    assert isinstance(result, dict)
    assert result["person"] == "Suresh"
    assert result["transaction_type"] == "train ticket booking"
    assert result["amount"] == "Rs. 850"
    assert result["source"] == "Chennai"
    assert result["destination"] == "Bangalore"
