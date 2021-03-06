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

        self._ref = self._normalise(self._ref)

    @classmethod
    def _normalise(cls, s):
        return s.replace('“', '"').replace('”', '"').replace('–', '-')

    def _extract(self, pattern, field, first=False):
        ret = ''

        matches = re.findall(pattern, self._ref)
        if len(matches):
            if (len(matches) == 1) or first:
                match = matches[0]
                self._ref = self._ref.replace(match[0], '{' + field + '}')
                ret = match[1]

        return ret

    def parse(self, reference):
        self.reset(reference)

        # get quoted title
        self.title = self._extract(r'("([^"]+)")', 'title')

        datep = r'(\b(18|19|20)\d\d[abc]?\b)'

        while not self.date:
            # get bracketed year
            self.date = self._extract(
                r'(\([^)]*' + datep + r'[^)]*\))', 'date')

            # get unique year
            if not self.date:
                self.date = self._extract(r'(' + datep + r')', 'date')

            if not self.date:
                self.date = self._extract(
                    r'(\. ' + datep + r'\.)', 'date'
                )

            if not self.date:
                self.date = self._extract(
                    r'(, ' + datep + r'\.)', 'date'
                )

            if not self.date:
                self.date = self._extract(
                    r'(, ' + datep + r',)', 'date'
                )

            # get unique year not preceded or followed by -
#             if 0 and not self.date:
#                 self.date = self._extract(
#                     r'((?<![-0-9])' + datep + r'(?![-0-9]))', 'date')

            # remove access date
            if 1 and not self.date:
                access_date = self._extract(
                    r'(\[[^\]]*' + datep + r'[^\]]*\])', 'access_date')
                if not access_date:
                    break
            else:
                break

        if self.date:
            self._extract(r'({date}([.,;]))', 'date')

        if 1 and self.title and not self.authors:
            # anything in front of title (or date) that isn't a date
            # catches 40% of authors on test set
            self.authors = self._extract(
                r'^((([^{](?!\d{4,4}))+))', 'authors',
            )

#         if 0:
#             # author (without . or ,) -> title
#             # Works sometimes BUT
#             # NO: b/c title can be after
#             if self.authors and not self.title:
#                 if not re.search(r'\.|,', self.authors):
#                     self.title = self.authors
#                     self.authors = ''

        if 1 and not self.authors:
            # the authors field most likely captured the title
            # we need to split them
            #
            # #80, ACS
            # Evans, D. A.; Fitch, D. M.; Smith, T. E.; Cee, V. J.
            # #69, AMA
            # Venkat Narayan, KM.
            # #4, ?
            # Bagdikian, B.H.
            # 22, APA
            # Greene, C. (Producer), del Toro, G.(Director)
            #
            # sentence with lowercase words (other than and/et) indicate title
            #
            if not self.authors:
                # #32, IEEE
                # B. Klaus and P. Horn
                # #34
                # L. Bass, P. Clements, and R. Kazman
                # #84
                # W. Zeng, H. Yu, C. Lin
                #                 self.authors = self._extract(
                #                     r'^(((( ?[A-Z]{1,2}\.)+ [^.,]+[,.]( and)?)+))',
                #                     'authors1'
                #                 )
                self.authors = self._extract(
                    r'^((((^|,|,? and)( ?[A-Z]{1,2}\.)+ ([^,{.](?!and ))+)+))',
                    'authors1'
                )
            if not self.authors:
                # #10 xxx
                # Ellman, M., and F. Germano
                # #19 APA
                # Carter, S., & Dunbar-Odom, D.
                # #20
                # Gaudio, J. L., & Snowdon, C. T.
                # included = [19, 80, 20, 69, 4, 22]
                self.authors = self._extract(
                    # r'^((([^,.{]+,((| |-)[A-Z]{1,2}\.)+(\s*\([^)]+\))?,?)+))',
                    r'^((((^|,|,? (and|&) )[^,.{]+,((| |-)[A-Z]{1,2}\.)+(\s*\([^)]+\))?)+))',
                    'authors2'
                )
            if not self.authors:
                # #49, MLA
                # #50
                # Smith, John, and Bob Anderson
                # #51
                # Campbell, Megan, et al.
                self.authors = self._extract(
                    r'^(([A-Z][a-z]+, [A-Z][a-z]+[^.{]+\.))',
                    'authors3'
                )
            if 1 and not self.authors:
                # #68, AMA
                # Boyd B, Basic C, Bethem R, eds
                # #70, AMA
                # Guyton JL, Crockarell JR
                # #76
                # Florez H, Martinez R, Chakra W, Strickman-Stein M, Levis S
                self.authors = self._extract(
                    r'^((((^| )[A-Z][a-z][-\w]* [A-Z]{1,2}[,.])+))',
                    'authors4'
                )

            if 1 and self.authors:
                self.authors += self._extract(
                    r'(\{authors\d?\}((\.? ?(,? ?(et al|and others)\.?)?(,? ?[Ee]ds\.?))?))',
                    'authors9',
                    True
                )

        if 1 and not self.authors:
            # authors = anything from start to . or {
            # catches 80%
            # BUT also a lot of FALSE POSITIVES
            # (i.e. include title and other stuff in the authors)
            # e.g. Goh, S. L. Polymer Chemistry
            part = self._extract(
                # r'^(([^{]+?))(?:\{|(?<![A-Z)])\.)',
                r'^((((?<=[A-Z])\.|[^{.])+))',
                'authors8'
            )
            if not self.title and (
                re.match(r'(The|A|An) ', part)
                # Fast facts
                or (
                    re.search(r' [a-z]+\.?$', part)
                    and not re.search(r' et al\.?$', part)
                )
            ):
                self.title = part
            else:
                self.authors = part

            if 0 and self.authors and not self.title:
                # we might have captured the title in the authors
                # Michael Pollan, The Omnivore's Dilemma
                # if self.authors
                pass

        if self.authors and self.date and not self.title:
            # title = anything between } and { with a dot in it
            # assumes that the date is after the title
            self.title = self._extract(
                r'\}\s*\.*\s*(([^.{}]{2,}))', 'title',
                True
            )

        # clean the title

        if self.title:
            # Crimson peak [Motion picture]
            self.title = re.sub(r'\[[^\]]+\]$', '', self.title)
            # The New Media Monopoly, Boston: Beacon Press
            self.title = re.sub(r',[^,:]+:[^,:]+$', '', self.title)

            self.title = self.title.strip(' ').strip(
                '.').strip(',')

            self.title = re.sub(r"^'(.+)'$", r"\1", self.title)
