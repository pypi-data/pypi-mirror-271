from cytoolz.curried import curry

from genomoncology.parse import ensures, DocType, __TYPE__, __CHILD__
from .base import LazyFileSource
import csv


def do_split(delimiter, s):
    s = s.strip()
    if delimiter == ",":
        # reference: https://stackoverflow.com/a/35822856
        val = next(csv.reader([s]))
    else:
        val = s.split(delimiter)
    return val


@curry
class DelimitedFileSource(LazyFileSource):
    def __init__(
        self,
        filename,
        columns,
        delimiter="\t",
        skip_comment=False,
        comment_char="#",
        include_header=True,
        **meta
    ):
        self._mapper = None
        self.columns = ensures.ensure_collection(columns)
        self.delimiter = delimiter
        self.skip_comment = skip_comment
        self.comment_char = comment_char
        self.include_header = include_header
        self.meta = meta

        if __TYPE__ not in meta:
            self.meta[__TYPE__] = DocType.TSV.value

        super().__init__(filename)

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        iterator = super(DelimitedFileSource.func, self).__iter__()
        if self.skip_comment:
            def is_not_comment(line):
                return not line.startswith(self.comment_char)
            iterator = filter(is_not_comment, iterator)

        if not self.columns:
            self.columns = next(csv.reader(iterator, delimiter=self.delimiter))

        if self.include_header:
            yield self.create_header()

        reader = csv.DictReader(iterator, fieldnames=self.columns,
                                delimiter=self.delimiter)
        yield from map(lambda row: {**row, **self.meta}, reader)

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            "columns": self.columns,
            "meta": self.meta,
            "file_path": self.name,
        }
