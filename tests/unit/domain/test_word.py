from src.domain.models import Word

def test_word_creation():
    """Test we can create a word"""
    word = Word(
        id="1",
        text="안녕",
        language="ko"
    )
    assert word.text == "안녕"
    assert word.language == "ko"

def test_word_string_representation():
    """Test string output"""
    word = Word(id="1", text="안녕", language="ko")
    assert str(word) == "안녕 (ko)"