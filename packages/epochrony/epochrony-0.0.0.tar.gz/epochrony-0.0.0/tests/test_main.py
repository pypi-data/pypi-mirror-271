"""
Test main module
"""

from epochrony.main import run


def test_main():
    """
    Ensure that main starts
    """
    result = run()
    assert result
