"""
Live API tests for langextract.

These tests require real API keys and external services.
They are marked as integration tests and are NOT run in CI by default.
"""

import os
import pytest

from langextract import extract
from langextract.core.exceptions import InferenceConfigError

# Mark the entire file as integration test
pytestmark = pytest.mark.integration


def test_live_openai_api_call():
    """
    Test live OpenAI API call.
    Requires OPENAI_API_KEY to be set in environment variables.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        pytest.skip("OPENAI_API_KEY not set, skipping live API test")

    result = extract(
        text="John works at Google as a Software Engineer.",
        schema={
            "person": "Name of the person",
            "company": "Company name",
            "role": "Job role"
        },
        provider="openai",
        model="gpt-4o-mini",
    )

    assert result is not None
    assert "person" in result
    assert "company" in result
    assert "role" in result


def test_live_api_missing_key_raises_error():
    """
    Ensure missing API key raises correct error.
    """
    with pytest.raises(InferenceConfigError):
        extract(
            text="Test text",
            schema={"field": "value"},
            provider="openai",
            model="gpt-4o-mini",
            api_key=None,
        )
