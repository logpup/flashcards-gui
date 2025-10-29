# src/domain/enums/language.py
from enum import Enum

class Language(Enum):
    KOREAN = "ko"
    ENGLISH = "en"
    
    @property
    def display_name(self) -> str:
        names = {
            Language.KOREAN: "Korean",
            Language.ENGLISH: "English"
        }
        return names[self]