"""
Example custom provider plugin tests for langextract.

This file demonstrates how a third-party or external provider plugin
can be registered and used with langextract.

These tests are OPTIONAL and are skipped in CI environments unless
the example plugin is explicitly installed.
"""

import pytest

from langextract.core.exceptions import InferenceConfigError

# Mark entire file as optional plugin test
pytestmark = pytest.mark.optional


def _plugin_available() -> bool:
    """
    Check whether the example plugin is available.
    """
    try:
        import langextract_example_plugin  # type: ignore
        return True
    except ModuleNotFoundError:
        return False


def test_example_provider_is_registered():
    """
    Ensure example provider is registered when plugin is installed.
    """
    if not _plugin_available():
        pytest.skip("Example provider plugin not installed")

    from langextract.providers import get_provider

    provider_cls = get_provider("example")
    assert provider_cls is not None


def test_example_provider_inference():
    """
    Test inference using the example provider.
    """
    if not _plugin_available():
        pytest.skip("Example provider plugin not installed")

    from langextract import extract

    result = extract(
        text="Suresh works as a Mechanical Engineer in Chennai.",
        schema={
            "name": "Person name",
            "profession": "Job title",
            "city": "City name",
        },
        provider="example",
    )

    assert result is not None
    assert "name" in result
    assert "profession" in result
    assert "city" in result


def test_example_provider_missing_configuration_raises_error():
    """
    Ensure provider raises a clear error when configuration is missing.
    """
    if not _plugin_available():
        pytest.skip("Example provider plugin not installed")

    from langextract import extract

    with pytest.raises(InferenceConfigError):
        extract(
            text="Test text",
            schema={"field": "value"},
            provider="example",
            config=None,
        )
