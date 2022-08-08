import os


class OpfMaker:

    def __init__(self):
        self.file = None
        self.chapters = []

    def start_with_folder(self, path: str, **kwargs):
        self.file = open(os.path.join(path, 'content.opf'), 'w', encoding='utf-8')
        # noinspection HttpUrlsUsage
        data = (
            '<?xml version="1.0"  encoding="UTF-8"?>\n'
            '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">\n'
            '    <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
            ' xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        )
        self.file.write(data)

        for key, value in kwargs.items():
            if key == 'subject':
                data = ''
                for item in value:
                    data = data + f'        <dc:{key}>{item}</dc:{key}>\n'
            elif key == 'identifier':
                data = f'<dc:identifier opf:scheme="uuid" id="uuid_id">{value}</dc:identifier>'
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
            '</package>'
        )
        self.file.write(data)

        self.file.close()
        self.file = None
