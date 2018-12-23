import re
from datetime import datetime


EXTENSIONS = (
    'wiki'
)


class WikiReport:

    def __init__(self, content):
        self._content = content

    def parse(self):
        name = None
        tags = []
        for line in self._content.split('\n'):
            if line.startswith('- '):
                elements = line.split('#')
                name = elements[0][2:].rstrip()
                tags = [i.rstrip() for i in elements[1:]]
            elif name and re.match(
                    r'  \* \d{4}-\d{2}-\d{2} \d{2}:\d{2} - '
                    r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                    line):
                start, end = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', line)
                start = datetime.strptime(start, '%Y-%m-%d %H:%M')
                end = datetime.strptime(end, '%Y-%m-%d %H:%M')
                yield (name, tags, start, end)
