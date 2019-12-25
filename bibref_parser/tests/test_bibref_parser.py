from ..parser import BibRefParser
import os
import re

# 101 references. Errors: 9 year (8.9%), 19 title (18.8%), 7 authors (6.9%)
# test_filename = 'test_dataset.csv'
test_filename = 'anystyle-gold.csv'

# target : year: 4%, authors: 9%, titles: 9%
# test   : year: 2%, authors: 5%, titles: 7%
# any 1k :           authors:16%, titles: 25%


class Tester:
    def test_parse_test_dataset(self):
        parser = BibRefParser()

        errors = ParsingErrors()

        #included = [2, 3, 4, 9, 15, 20, 21]
        # included = []
        # included = [2, 3, 4]
        # included = range(500, 102)
        included = range(1, 1003)
        # included = [8]
        # included = [19, 80, 20, 69, 4]
        # included = [32, 34, 38, 39]
        # included = range(46, 53)
        # included = [3, 7, 10]
        # included = [68, 70, 72, 73]
        # included = [75]

        input_path = os.path.join(os.path.dirname(__file__), test_filename)

        import csv
        with open(input_path) as fh:
            reader = csv.reader(fh)
            line = 0
            reference_count = 0
            for row in reader:
                line += 1
                if line < 2 or (included and line not in included):
                    continue
                if 1 and re.search(r'^[A-Z]{4}', row[1]):
                    # removes french styled references with uppercase names
                    # print(row[1])
                    continue
                if 1:
                    p = re.findall(r'\b(1st|2nd|3rd|\dth) [Ee]d\b', row[1])
                    if p:
                        # print(p, row[1])
                        pass

                reference_count += 1
                parser.parse(row[1])
                if 0:
                    errors.test_field(
                        line, 'year', row[3], parser.date,
                        row[1], row[0], parser._ref
                    )
                if 1:
                    errors.test_field(
                        line, 'title', row[4], parser.title,
                        row[1], row[0], parser._ref
                    )
                if 0:
                    errors.test_field(
                        line, 'authors', row[2], parser.authors,
                        row[1], row[0], parser._ref
                    )

        errors.do_assert(reference_count)


def normalise(s, field):
    ret = s
    if field == 'year':
        years = re.findall(r'\d{4,4}', s)
        if years:
            ret = years[0]

    ret = BibRefParser._normalise(ret)

    if field == 'title':
        ret = re.sub(r', \d[a-z]{2} ed\.?$', r'', ret)

    ret = re.sub(r'^[",. ]*(.*?)[",. ]*$', r'\1', ret)
    return ret


class ParsingErrors(list):

    def test_field(self, line, field, expected, parsed, reference, style, annotated):
        expected = normalise(expected, field)
        parsed = normalise(parsed, field)
        if expected == '' or (expected != parsed):
            if not(expected == 'NONE' and parsed == ''):
                self.append(ParsingError(
                    line, field, expected, parsed, reference, style, annotated
                ))

    def get_message(self, reference_count):
        ret = '\n'

        ret += '\n'.join([
            error.get_message()
            for error
            in self
        ])

        ret += '\n' + '-' * 10 + '\n'

        stats = {}
        for error in self:
            if error.field not in stats:
                stats[error.field] = 0
            stats[error.field] += 1

        ret += '{} references. Errors: '.format(reference_count)

        ret += ', '.join([
            '{} {} ({:.1f}%)'.format(c, field, c / reference_count * 100)
            for field, c in stats.items()
        ])

        return ret

    def do_assert(self, reference_count):
        if len(self):
            assert False, self.get_message(reference_count)


class ParsingError:

    def __init__(self, *args, **kwargs):
        self.reset(*args, **kwargs)

    def reset(self, line, field, expected, parsed, reference, style, annotated):
        self.line = line
        self.field = field
        self.expected = expected
        self.parsed = parsed
        self.reference = reference
        self.style = style
        self.annotated = annotated

    def get_message(self):
        ret = '#{e.line} {e.style}, {e.field}:'
        ret += '\n  {e.expected!r} [expected]'
        ret += '\n  {e.parsed!r} [parsed]'
        ret += '\n  {e.reference!r}'
        ret += '\n  {e.annotated!r}'
        return ret.format(e=self)
