"""
Language code mapping between ISO 639-1 (2-letter) and ISO 639-3 (3-letter) codes.
"""

# Comprehensive language code mapping
LANGUAGE_CODE_MAPPING = {
    # Common language mappings
    'twi': 'ak',  # Twi -> Akan (Google uses 'ak' for Akan which includes Twi)
    'aka': 'ak',  # Akan
    'fra': 'fr',  # French
    'deu': 'de',  # German
    'spa': 'es',  # Spanish
    'por': 'pt',  # Portuguese
    'ita': 'it',  # Italian
    'rus': 'ru',  # Russian
    'zho': 'zh-cn',  # Chinese Simplified
    'cmn': 'zh-cn',  # Mandarin
    'jpn': 'ja',  # Japanese
    'kor': 'ko',  # Korean
    'ara': 'ar',  # Arabic
    'hin': 'hi',  # Hindi
    'ben': 'bn',  # Bengali
    'urd': 'ur',  # Urdu
    'swa': 'sw',  # Swahili
    'yor': 'yo',  # Yoruba
    'ibo': 'ig',  # Igbo
    'hau': 'ha',  # Hausa
    'amh': 'am',  # Amharic
    'orm': 'om',  # Oromo
    'som': 'so',  # Somali
    'wol': 'wo',  # Wolof
    'ful': 'ff',  # Fulah
    'mand': 'man',  # Mandingo
    'ewe': 'ee',  # Ewe
    'twi': 'tw',  # Twi (alternate)
    'tir': 'ti',  # Tigrinya
    'orm': 'om',  # Oromo
}

# Reverse mapping for 2-letter to 3-letter
REVERSE_LANGUAGE_MAPPING = {v: k for k, v in LANGUAGE_CODE_MAPPING.items() if len(v) == 2}

def convert_lang_code(lang_code: str, to_google: bool = True) -> str:
    """
    Convert language codes between Google format (2-letter) and terminology format.
    
    Args:
        lang_code: Language code to convert
        to_google: If True, convert to Google format (2-letter), 
                   else convert to terminology format (3-letter)
    
    Returns:
        Converted language code
    """
    if not lang_code:
        return lang_code
    
    # If it's already a 2-letter code and we want Google format, return as-is
    if to_google and len(lang_code) == 2:
        return lang_code
    
    # If it's a 3-letter code and we want Google format, look up mapping
    if to_google and len(lang_code) == 3:
        return LANGUAGE_CODE_MAPPING.get(lang_code.lower(), lang_code)
    
    # If converting from Google to terminology format
    if not to_google and len(lang_code) == 2:
        return REVERSE_LANGUAGE_MAPPING.get(lang_code.lower(), lang_code)
    
    # Default: return as-is
    return lang_code

def detect_lang_code_format(lang_code: str) -> str:
    """Detect if a language code is 2-letter or 3-letter."""
    if len(lang_code) == 2:
        return 'iso639-1'
    elif len(lang_code) == 3:
        return 'iso639-3'
    else:
        return 'unknown'

def get_available_google_languages() -> list:
    """Get list of languages supported by Google Translate."""
    # Google Translate supports these major languages
    return [
        'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 
        'ceb', 'zh', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 
        'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 
        'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 
        'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 
        'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ny', 'or', 
        'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 
        'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg', 'ta', 
        'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 
        'yi', 'yo', 'zu'
    ]

def is_google_supported(lang_code: str) -> bool:
    """Check if a language code is supported by Google Translate."""
    google_code = convert_lang_code(lang_code, to_google=True)
    supported_languages = get_available_google_languages()
    return google_code in supported_languages
