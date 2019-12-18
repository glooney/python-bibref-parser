import re


class BibRefParser:

    def __init__(self):
        self.reset()

    def reset(self):
        self.reference = ''
        self.title = ''
        self.authors = ''
        # publication date
        self.date = ''
        self.publisher = ''

    def parse(self, reference):
        self.reset()

        reference = reference.replace('“', '"')
        reference = reference.replace('”', '"')

        self.reference = reference

        # get quoted title
        titles = re.findall(r'"[^"]+"', reference)
        if len(titles) == 1:
            reference = reference.replace(titles[0], '')
            self.title = titles[0].strip('"').strip(',')

        dates = re.findall(r'\d{4,4}', reference)
        if len(dates) == 1:
            reference = reference.replace(dates[0], '')
            self.date = dates[0]
        else:
            # TODO: negative look back
            dates = re.findall(r'\([^)]*(\d{4,4})[^)]*\)', reference)
            if len(dates) == 1:
                reference = reference.replace(dates[0], '')
                self.date = dates[0]

        reference = re.sub(r'([^A-Z])\. ', r'\1@ ', reference)

        return reference
