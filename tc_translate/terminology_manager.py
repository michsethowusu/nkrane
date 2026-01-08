import os
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import json

from .language_codes import convert_lang_code, detect_lang_code_format, is_google_supported

@dataclass
class Term:
    id: int
    term: str
    translation: str
    google_lang_code: str  # Google-compatible language code

class TerminologyManager:
    def __init__(self, csv_path: str = None):
        """Initialize terminology manager with a single CSV file.
        
        Args:
            csv_path: Path to the terminology CSV file. 
                     If None, looks for terminologies_{lang}.csv in terminologies/ folder
                     inside the package directory.
        """
        self.csv_path = csv_path
        self.terms = {}  # Dictionary of terms for the language
        self.language = None
        self.google_lang_code = None
        self._load_terminologies()
    
    def _find_terminology_file(self) -> str:
        """Find the terminology CSV file."""
        if self.csv_path and os.path.exists(self.csv_path):
            return self.csv_path
            
        # Look in terminologies/ folder inside package directory (for installed packages)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        terminologies_dir = os.path.join(package_dir, 'terminologies')
        
        if os.path.exists(terminologies_dir):
            for filename in os.listdir(terminologies_dir):
                if filename.startswith('terminologies_') and filename.endswith('.csv'):
                    return os.path.join(terminologies_dir, filename)
        
        # Look in current directory (for development)
        current_dir = os.getcwd()
        for filename in os.listdir(current_dir):
            if filename.startswith('terminologies_') and filename.endswith('.csv'):
                return os.path.join(current_dir, filename)
        
        # Look in parent directory (for development)
        parent_dir = os.path.dirname(current_dir)
        for filename in os.listdir(parent_dir):
            if filename.startswith('terminologies_') and filename.endswith('.csv'):
                return os.path.join(parent_dir, filename)
        
        raise FileNotFoundError(
            "No terminology CSV file found. Looking for 'terminologies_{lang}.csv' "
            f"in terminologies/ folder ({terminologies_dir}), {current_dir}, or {parent_dir}"
        )
    
    def _load_terminologies(self):
        """Load terminology from the CSV file."""
        csv_file = self._find_terminology_file()
        
        # Extract language from filename (terminologies_lang.csv)
        basename = os.path.basename(csv_file)
        language = basename.replace('terminologies_', '').replace('.csv', '')
        
        self.language = language
        self.google_lang_code = convert_lang_code(language, to_google=True)
        
        # Check if Google Translate supports this language
        if not is_google_supported(language):
            print(f"Warning: Language '{language}' may not be fully supported by Google Translate")
            print(f"  Using code: '{self.google_lang_code}' for Google Translate")
        
        # Load the CSV file
        df = pd.read_csv(csv_file)
        
        # Create terms dictionary
        self.terms = {}
        for _, row in df.iterrows():
            term_id = int(row['id'])
            term = Term(
                id=term_id,
                term=str(row['term']).lower().strip(),
                translation=str(row['translation']),
                google_lang_code=self.google_lang_code
            )
            self.terms[term.term] = term
    
    def get_google_lang_code(self, language: str = None) -> str:
        """Get Google-compatible language code."""
        if language and language != self.language:
            return convert_lang_code(language, to_google=True)
        return self.google_lang_code
    
    def _match_case(self, original: str, replacement: str) -> str:
        """Match the case pattern of the original text.
        
        Args:
            original: The original text that was matched
            replacement: The replacement text from terminology
            
        Returns:
            Replacement text with matched case pattern
        """
        # If original is all uppercase
        if original.isupper():
            return replacement.upper()
        
        # If original is all lowercase
        if original.islower():
            return replacement.lower()
        
        # If original is title case (first letter capitalized)
        if original.istitle():
            return replacement.capitalize()
        
        # If original has first letter capitalized (sentence case)
        if original[0].isupper() and original[1:].islower():
            return replacement.capitalize()
        
        # If original is mixed case, preserve the replacement's original case
        # but capitalize first letter if original starts with capital
        if original[0].isupper():
            return replacement.capitalize()
        
        return replacement.lower()
    
    def preprocess_text(self, text: str) -> Tuple[str, Dict[str, Term], Dict[str, str]]:
        """Replace terms in text with their IDs.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (preprocessed_text, id_to_term_mapping, original_case_mapping)
        """
        if not self.terms:
            raise ValueError(f"No terminology loaded for language '{self.language}'")
        
        # Sort terms by length (longest first) to handle compound terms
        sorted_terms = sorted(self.terms.values(), key=lambda x: len(x.term), reverse=True)
        
        preprocessed_text = text
        replacements = {}  # Map of placeholder to term
        original_cases = {}  # Map of placeholder to original text for case matching
        
        for term_obj in sorted_terms:
            # Case-insensitive replacement with word boundaries, but capture original case
            pattern = re.compile(r'\b(' + re.escape(term_obj.term) + r')\b', re.IGNORECASE)
            
            def replace_with_placeholder(match):
                original_text = match.group(1)
                placeholder = f"<{term_obj.id}>"
                replacements[placeholder] = term_obj
                original_cases[placeholder] = original_text  # Store original case
                return placeholder
            
            preprocessed_text = pattern.sub(replace_with_placeholder, preprocessed_text)
        
        return preprocessed_text, replacements, original_cases
    
    def postprocess_text(self, text: str, replacements: Dict[str, Term], 
                        original_cases: Dict[str, str]) -> str:
        """Replace IDs in translated text with their translations, preserving original case.
        
        Args:
            text: Translated text with placeholders
            replacements: Mapping from placeholders to Term objects
            original_cases: Mapping from placeholders to original text for case matching
            
        Returns:
            Postprocessed text with actual translations and matched case
        """
        for placeholder, term_obj in replacements.items():
            original_text = original_cases.get(placeholder, '')
            if original_text:
                # Match the case of the original text
                matched_case_translation = self._match_case(
                    original_text, 
                    term_obj.translation
                )
                text = text.replace(placeholder, matched_case_translation)
            else:
                # Fallback to original translation if no case info
                text = text.replace(placeholder, term_obj.translation)
        
        return text
