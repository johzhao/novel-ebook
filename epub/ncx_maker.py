import os


class NcxMaker:

    def __init__(self):
        self.file = None
        self.nav_index = 0

    def start_with_folder(self, path: str, uuid: str, title: str):
        self.file = open(os.path.join(path, 'content.ncx'), 'w')
        data = ('<?xml version="1.0"?>\n'
                '<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">\n'
                '    <head>\n'
                f'        <meta name="dtb:uid" content="{uuid}" />\n'
                '        <meta name="dtb:depth" content="2" />\n'
                '        <meta name="dtb:totalPageCount" content="0" />\n'
                '        <meta name="dtb:maxPageNumber" content="0" />\n'
                '    </head>\n'
                '    <docTitle>\n'
                f'        <text>{title}</text>\n'
                '    </docTitle>\n'
                '    <navMap>\n'
                )
        self.file.write(data)
        self.nav_index = 1

    def append_chapter(self, title: str, filename: str):
        data = (
            f'        <navPoint class="chapter" id="num_{self.nav_index}" playOrder="{self.nav_index}">\n'
            '            <navLabel>\n'
            f'                <text>{title}</text>\n'
            '            </navLabel>\n'
            f'            <content src="{filename}" />\n'
            '        </navPoint>\n'
        )
        self.file.write(data)
        self.nav_index += 1

    def end(self):
        data = (
            '    </navMap>\n'
            '</ncx>\n'
        )
        self.file.write(data)
        self.file.close()
        self.file = None
