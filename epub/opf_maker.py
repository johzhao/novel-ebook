import os


class OpfMaker:

    def __init__(self):
        self.file = None
        self.chapters = []

    def start_with_folder(self, path: str, **kwargs):
        self.file = open(os.path.join(path, 'content.opf'), 'w')
        data = (
            '<?xml version="1.0"  encoding="UTF-8"?>\n'
            '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="unknown" version="2.0">\n'
            '    <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
            ' xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        )
        self.file.write(data)

        for key, value in kwargs.items():
            if key == 'identifier':
                data = f'        <dc:{key} id="unknown">{value}</dc:{key}>\n'
            else:
                data = f'        <dc:{key}>{value}</dc:{key}>\n'
            self.file.write(data)

        data = '    </metadata>\n'
        self.file.write(data)
        self.chapters = []

    def append_chapter(self, filename: str):
        self.chapters.append(filename)

    def end(self):
        data = (
            '    <manifest>\n'
            '        <item href="content.ncx" id="ncx" media-type="application/x-dtbncx+xml" />\n'
        )
        self.file.write(data)

        for index, filename in enumerate(self.chapters, 1):
            data = f'        <item href="{filename}" id="id{index}" media-type="application/xhtml+xml" />\n'
            self.file.write(data)

        data = '    </manifest>\n'
        self.file.write(data)

        data = '    <spine toc="ncx">\n'
        self.file.write(data)

        for index in range(1, len(self.chapters) + 1):
            data = f'        <itemref idref="id{index}"/>\n'
            self.file.write(data)

        data = (
            '    </spine>\n'
            # '    <guide>\n'
            # '        <reference href="chapter_1.html" title="Cover" type="cover" />\n'
            # '        <reference href="text/part0234.html#6V53K1-24f1c0ada31d49d487aeb4b6013cbf0b"'
            # ' title="Table of Contents" type="toc" />\n'
            # '    </guide>\n'
            '</package>'
        )
        self.file.write(data)

        self.file.close()
        self.file = None
