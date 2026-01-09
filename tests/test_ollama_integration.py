"""
Ollama integration tests for langextract.

These tests require a running Ollama server and local models.
They are marked as integration tests and are skipped in CI.
"""

import pytest
import shutil
import subprocess

from langextract import extract

# Mark entire file as integration test
pytestmark = pytest.mark.integration


def _ollama_available() -> bool:
    """
    Check whether Ollama CLI is installed and available.
    """
    return shutil.which("ollama") is not None


def _ollama_running() -> bool:
    """
    Check whether Ollama service is running.
    """
    try:
        subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except Exception:
        return False


def test_ollama_basic_inference():
    """
    Basic Ollama inference test using a local model.
    """
    if not _ollama_available():
        pytest.skip("Ollama is not installed")

    if not _ollama_running():
        pytest.skip("Ollama service is not running")

    result = extract(
        text="Alice lives in Paris and works as a data scientist.",
        schema={
            "name": "Person name",
            "city": "City name",
            "profession": "Job title",
        },
        provider="ollama",
        model="llama3",
    )

    assert result is not None
    assert "name" in result
    assert "city" in result
    assert "profession" in result


def test_ollama_missing_model_raises_error():
    """
    Ensure missing model configuration raises an error.
    """
    if not _ollama_available():
        pytest.skip("Ollama is not installed")

    if not _ollama_running():
        pytest.skip("Ollama service is not running")

    with pytest.raises(Exception):
        extract(
            text="Test text",
            schema={"field": "value"},
            provider="ollama",
            model="non-existent-model",
        )
