from ..parser import BibRefParser
import os

test_filename = 'test_dataset.csv'


class Tester:
    def test_parse_test_dataset(self):
        parser = BibRefParser()

        errors = ParsingErrors()

        #included = [2, 3, 4, 9, 15, 20, 21]
        # included = []
        included = [2, 3, 4]

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

                reference_count += 1
                r = parser.parse(row[1])
                errors.test_field(line, 'year', row[3], parser.date, row[1])
                # errors.test_field(line, 'title', row[4], parser.title, row[1])
                errors.test_field(
                    line, 'authors', row[2], parser.authors, row[1])

        errors.do_assert(reference_count)


class ParsingErrors(list):

    def test_field(self, line, field, expected, parsed, reference):
        if expected != parsed:
            self.append(ParsingError(line, field, expected, parsed, reference))

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
            '{} {}'.format(c, field)
            for field, c in stats.items()
        ])

        return ret

    def do_assert(self, reference_count):
        if len(self):
            assert False, self.get_message(reference_count)


class ParsingError:

    def __init__(self, *args, **kwargs):
        self.reset(*args, **kwargs)

    def reset(self, line, field, expected, parsed, reference):
        self.line = line
        self.field = field
        self.expected = expected
        self.parsed = parsed
        self.reference = reference

    def get_message(self):
        return '#{e.line} {e.field}:\n  {e.expected!r} [expected]\n  {e.parsed!r} [parsed]\n  {e.reference!r}'.format(e=self)
