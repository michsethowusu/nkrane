# TC Translator (Terminology-Controlled Translator)

A Python package that extends Google Translate with terminology control. It first substitutes domain-specific terms with IDs, translates the text, then replaces the IDs with approved translations.

## Features
- Domain-specific terminology control
- Support for multiple languages and domains
- Simple API similar to Google Translate
- CLI interface for quick translations
- Automatic terminology detection from CSV files

## Installation

```bash
git clone https://github.com/yourusername/tc-translate.git
cd tc-translate
pip install -e .
```

Or install directly:

bash

```
pip install -e git+https://github.com/yourusername/tc-translate.git
```



## Usage

### As a Python package:

python

```
from tc_translate import TCTranslator

# Initialize translator for agriculture domain in Twi
translator = TCTranslator(domain='agric', target_lang='twi')

# Translate text with terminology control
result = translator.translate("The farmer uses an abattoir and acreage for farming.")
print(result.text)
```



### Command Line Interface:

bash

```
# Basic translation
tc-translate "The farmer uses an abattoir" --domain agric --target twi

# From file
tc-translate --input text.txt --domain science --target twi

# List available domains and languages
tc-translate --list
```



### Using the Google Translate-like API:

python

```
from tc_translate import Translator

translator = Translator()
result = translator.translate("abattoir and acreage", src='en', dest='twi', domain='agric')
print(result.text)
```



## Terminology Files

Add your terminology CSV files in the `terminologies/` directory with naming convention:
`{domain}_terms_{language}.csv`

CSV format:

csv

```
id,term,translation
1,abattoir,aboa kum fie
2,aboiteau,nsu ban ɔkwan
...
```



## Language Code Support

TC Translator supports both 3-letter (ISO 639-3) and 2-letter (ISO 639-1)  language codes. The system automatically converts between them:

### Using 3-letter codes:

python

```
# Your terminology files: agric_terms_twi.csv
translator = TCTranslator(domain='agric', target_lang='twi')
```



### Using 2-letter Google codes:

python

```
# Same terminology file, but using Google's code
translator = TCTranslator(domain='agric', target_lang='ak')
```



### Common Language Mappings:

- `twi` → `ak` (Akan/Twi)
- `fra` → `fr` (French)
- `deu` → `de` (German)
- `spa` → `es` (Spanish)
- `yor` → `yo` (Yoruba)

### Check supported languages:

bash

```
# List all available domains and languages
tc-translate list

# Get information about a language code
tc-translate langinfo twi
```



### Terminology File Naming:

Name your terminology files using either format:

- `{domain}_terms_{3-letter-code}.csv` (e.g., `agric_terms_twi.csv`)
- `{domain}_terms_{2-letter-code}.csv` (e.g., `agric_terms_ak.csv`)

The system will automatically detect and convert between codes as needed.
