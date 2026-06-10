import pytest
from momoru.core.scanner import BuzzerScanner

def test_similarity_empty():
    scanner = BuzzerScanner([], "target")
    assert scanner.calculate_similarity() == 0.0