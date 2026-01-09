"""
Gemini batch API integration tests for langextract.

These tests require access to Google's Gemini API and valid credentials.
They are marked as integration tests and are skipped in CI environments.
"""

import os
import pytest

from langextract import extract
from langextract.core.exceptions import InferenceConfigError

# Mark entire file as integration test
pytestmark = pytest.mark.integration


def _gemini_api_key_available() -> bool:
    """
    Check whether Gemini API key is available.
    """
    return bool(os.getenv("GEMINI_API_KEY"))


def test_gemini_batch_inference():
    """
    Test Gemini batch inference with a valid API key.
    """
    if not _gemini_api_key_available():
        pytest.skip("GEMINI_API_KEY not set, skipping Gemini integration test")

    result = extract(
        text="Ravi is studying Computer Science at Anna University.",
        schema={
            "name": "Student name",
            "field": "Field of study",
            "institution": "Institution name",
        },
        provider="gemini",
        model="gemini-1.5-flash",
        batch=True,
    )

    assert result is not None
    assert "name" in result
    assert "field" in result
    assert "institution" in result


def test_gemini_missing_api_key_raises_error():
    """
    Ensure missing Gemini API key raises correct error.
    """
    if _gemini_api_key_available():
        pytest.skip("API key present, skipping missing-key test")

    with pytest.raises(InferenceConfigError):
        extract(
            text="Test text",
            schema={"field": "value"},
            provider="gemini",
            model="gemini-1.5-flash",
        )


def test_gemini_invalid_model_raises_error():
    """
    Ensure invalid model name raises an error.
    """
    if not _gemini_api_key_available():
        pytest.skip("GEMINI_API_KEY not set")

    with pytest.raises(Exception):
        extract(
            text="Test text",
            schema={"field": "value"},
            provider="gemini",
            model="invalid-gemini-model",
        )
