# python-bibref-parser

Very simple parser for bibliographic references.

Extracts authors, title and year from a string.

Handcrafted with simple heuristics and regular expresions.

Aims to support most common uses of popular styles
(APA, Chicago, MLA, IEEE, AMA, ACS, MHRA) in English literature.

It's a cheap alternative to other tools based on machine learning
such as ParsCit, GROBID, CERMINE or AnyStyle. This tool works out-of-the box
with Python 3, has no dependency and doesn't need training.

It won't work well on OCRed text or any reference that uses punctuation
loosely.

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

Will return parsing errors over 100 references of various styles.
