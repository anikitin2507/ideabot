"""Smoke tests for basic functionality checks."""

import pytest


def test_import_main():
    """Test that main module can be imported."""
    try:
        import main

        assert main is not None
    except ImportError as e:
        pytest.fail(f"Failed to import main module: {e}")


def test_import_config():
    """Test that config module can be imported."""
    try:
        from src.config import Config, create_config

        assert Config is not None
        assert create_config is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Config: {e}")


def test_import_option_parser():
    """Test that option parser can be imported."""
    try:
        from src.services.option_parser import OptionParser

        assert OptionParser is not None
    except ImportError as e:
        pytest.fail(f"Failed to import OptionParser: {e}")


def test_import_openai_client():
    """Test that OpenAI client can be imported."""
    try:
        from src.services.openai_client import OpenAIClient

        assert OpenAIClient is not None
    except ImportError as e:
        pytest.fail(f"Failed to import OpenAIClient: {e}")


def test_import_decision_handler():
    """Test that decision handler can be imported."""
    try:
        from src.handlers.decision_handler import DecisionHandler

        assert DecisionHandler is not None
    except ImportError as e:
        pytest.fail(f"Failed to import DecisionHandler: {e}")


def test_option_parser_basic():
    """Test basic option parser functionality."""
    from src.services.option_parser import OptionParser

    parser = OptionParser()

    # Test simple "or" format
    options = parser.parse_options("Pizza or sushi?")
    assert options is not None
    assert len(options) == 2
    assert "Pizza" in options
    assert "sushi" in options

    # Test comma separated
    options = parser.parse_options("Coffee, tea, water")
    assert options is not None
    assert len(options) == 3

    # Test insufficient options
    options = parser.parse_options("Only one option")
    assert options is None

    # Test empty input
    options = parser.parse_options("")
    assert options is None
