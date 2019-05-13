import logging
import os
import shutil
import uuid
import zipfile

from epub.ncx_maker import NcxMaker
from epub.opf_maker import OpfMaker

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class EPubCreator:

    def __init__(self, work_folder: str):
        self.work_folder = work_folder
        self.novel_name = ''
        self.path = ''
        self.ncx_maker = NcxMaker()
        self.opf_maker = OpfMaker()
        self.chapter_index = 0

    def start_book(self, name: str, author: str = '', publisher: str = '', description: str = '', tags: list = None):
        self.novel_name = name
        self.path = os.path.join(self.work_folder, name)
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        os.makedirs(self.path, exist_ok=True)

        self._create_mimetype_file()
        self._create_container_xml()

        uuid_ = str(uuid.uuid4())

        self.path = os.path.join(self.path, 'OPS')
        os.makedirs(self.path, exist_ok=True)
        self.ncx_maker.start_with_folder(self.path, uuid_, name)

        meta = self._create_meta(uuid_, name, author, publisher, description, tags)
        self.opf_maker.start_with_folder(self.path, **meta)

        self.chapter_index = 1

    def append_chapter(self, title: str, content: str):
        lines = content.split('\n')
        filename = f'chapter_{self.chapter_index}.html'
        with open(os.path.join(self.path, filename), 'w') as ofile:
            ofile.write(
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<html xmlns="http://www.w3.org/1999/xhtml">\n'
                '    <head>'
                f'        <title>{title}</title>\n'
                '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n'
                '    </head>'
                '    <body>\n'
                f'        <h2>{title}</h2>\n'
            )
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                line = f'        <p>　　{line}</p>\n'
                ofile.write(line)
            ofile.write('    </body>\n</html>')
        self.ncx_maker.append_chapter(title, filename)
        self.opf_maker.append_chapter(filename)
        self.chapter_index += 1

    def finish_book(self) -> str:
        self.ncx_maker.end()
        self.opf_maker.end()

        epub_file = zipfile.ZipFile(os.path.join(self.work_folder, f'{self.novel_name}.epub'), 'w',
                                    zipfile.ZIP_DEFLATED)
        path = os.path.join(self.work_folder, self.novel_name)

        abs_path = os.path.abspath(os.path.join(path, 'mimetype'))
        arc_name = os.path.relpath(abs_path, path)
        epub_file.write(abs_path, compress_type=zipfile.ZIP_STORED, arcname=arc_name)

        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename == '.DS_Store' or filename == 'mimetype':
                    continue
                abs_path = os.path.join(root, filename)
                arc_name = os.path.relpath(abs_path, path)
                epub_file.write(abs_path, arcname=arc_name)
        epub_file.close()
        return ''

    def _create_mimetype_file(self):
        with open(os.path.join(self.path, 'mimetype'), 'w') as ofile:
            ofile.write('application/epub+zip')

    def _create_container_xml(self):
        path = os.path.join(self.path, 'META-INF')
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'container.xml'), 'w') as ofile:
            data = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                    '    <rootfiles>\n'
                    '        <rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml" />\n'
                    '    </rootfiles>\n'
                    '</container>')
            ofile.write(data)

    @staticmethod
    def _create_meta(uuid_: str, name: str, author: str, publisher: str, description: str, tags: list) -> dict:
        meta = {}
        if uuid_:
            meta['identifier'] = uuid_
        if name:
            meta['title'] = name
        if author:
            meta['creator'] = author
        if publisher:
            meta['publisher'] = publisher
        if description:
            meta['description'] = description
        meta['language'] = 'zh-CN'
        meta['subject'] = tags if tags else []
        return meta
