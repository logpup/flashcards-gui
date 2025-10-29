from dataclasses import dataclass
from typing import Optional

@dataclass
class Definition:
    """A definition of a word"""
    id: str
    word_id: str
    text: str
    part_of_speech: Optional[str] = None
    
    def __str__(self) -> str:
        pos = f"[{self.part_of_speech}] " if self.part_of_speech else ""
        return f"{pos}{self.text}"