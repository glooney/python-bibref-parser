# python-bibref-parser

Very simple parser for bibliographic references.

Extracts authors, title and year from a string.

Handcrafted with simple heuristics and regular expresions.

Aims to support most common uses of popular styles.

# Usage

```Python
from bibref_parser.parser import BibRefParser

parser = BibRefParser()
parser.parse('Baxter, C. (1997). Race equality in health care and education. Philadelphia: Ballière Tindall.')

parser.title
# 'Race equality in health care and education'
parser.date
# '1997'
parser.authors
# 'Baxter, C.'
```

# Installation

TODO

# Tests

```
pytest
```
