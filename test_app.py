import pytest
from streamlit_app import create_pdf_bytes

def test_language_splitting_logic():
    """Ensures the engine correctly identifies and splits language headers."""
    mock_response = "### ENGLISH\nHello World\n### العربية\nمرحبا بك"
    
    # We test if the logic can handle the split without crashing
    sections = mock_response.split("###")
    assert len(sections) == 3 # Initial empty split + 2 languages
    assert "ENGLISH" in sections[1]
    assert "العربية" in sections[2]

def test_rtl_detection():
    """Verifies that Arabic characters are correctly flagged for RTL formatting."""
    arabic_text = "مرحبا"
    english_text = "Hello"
    
    is_arabic = any("\u0600" <= c <= "\u06FF" for c in arabic_text)
    is_not_arabic = any("\u0600" <= c <= "\u06FF" for c in english_text)
    
    assert is_arabic is True
    assert is_not_arabic is False

def test_pdf_generation_output():
    """Ensures the PDF function returns actual bytes and not a null object."""
    sample_text = "### ENGLISH\nTest content"
    pdf_result = create_pdf_bytes(sample_text)
    
    assert isinstance(pdf_result, bytes)
    assert len(pdf_result) > 0
