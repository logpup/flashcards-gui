from dataclasses import dataclass
from typing import Optional

@dataclass
class Word:
    """Core concept: A word in any language"""
    id: str
    text: str  # The actual word
    language: str
    
    def __str__(self) -> str:
        return f"{self.text} ({self.language})"