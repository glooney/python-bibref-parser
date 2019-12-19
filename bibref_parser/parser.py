import re


class BibRefParser:

    def __init__(self):
        self.reset()

    def reset(self, reference=''):
        self._ref = reference
        self.reference = reference
        self.title = ''
        self.authors = ''
        # publication date
        self.date = ''
        self.publisher = ''

        self._ref = self._ref.replace('“', '"').replace('”', '"')

    def _extract(self, pattern, field):
        ret = ''

        matches = re.findall(pattern, self._ref)
        if len(matches) == 1:
            match = matches[0]
            self._ref = self._ref.replace(match[0], '{' + field + '}')
            ret = match[1]

        return ret

    def parse(self, reference):
        self.reset(reference)

        # get quoted title
        self.title = self._extract(r'("([^"]+)")', 'title')

        while not self.date:
            # get bracketed date
            self.date = self._extract(r'(\([^)]*(\d{4,4})[^)]*\))', 'date')

            # get unique date
            if not self.date:
                self.date = self._extract(r'((\d{4,4}))', 'date')

            # remove access date
            if not self.date:
                access_date = self._extract(
                    r'(\[[^\]]*(\d{4,4})[^\]]*\])', 'access_date')
                if not access_date:
                    break

        self.authors = self._extract(r'^((.*?))(?:\{|(?<=[a-z])\.)', 'authors')

        if self.authors and self.date and not self.title:
            self.title = self._extract(r'\}\s*\.*\s*(([^.{}]+))', 'title')

        if self.title:
            # Crimson peak [Motion picture]
            self.title = re.sub(r'\[[^\]]+\]$', '', self.title)
            # The New Media Monopoly, Boston: Beacon Press
            self.title = re.sub(r',[^,:]+:[^,:]+$', '', self.title)

        if self.title:
            self.title = self.title.strip(' ').strip('.').strip(',')

#         dates = re.findall(r'\d{4,4}', ref)
#         if len(dates) == 1:
#             ref = ref.replace(dates[0], '')
#             self.date = dates[0]
#         else:
#             # TODO: negative look back
#             dates = re.findall(r'\([^)]*(\d{4,4})[^)]*\)', ref)
#             if len(dates) == 1:
#                 ref = ref.replace(dates[0], '')
#                 self.date = dates[0]

#         ref = re.sub(r'([^A-Z])\. ', r'\1@ ', ref)

        print(self._ref)
