import logging

from bs4 import BeautifulSoup
# noinspection PyProtectedMember
from bs4 import Tag, NavigableString

from engine.response import Response
from engine.response_handler import ResponseHandler

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZhiHuYYLNHandler(ResponseHandler):

    def __init__(self):
        pass

    def handle_response(self, response: Response) -> Response:
        soup = BeautifulSoup(response.content, 'html.parser')

        content = Tag(name='html', attrs={
            'lang': 'zh'
        })

        content.append(self._process_head(soup))
        content.append(self._process_body(soup))

        response = Response(response.request, content.prettify())
        return response

    @staticmethod
    def _process_head(soup: BeautifulSoup) -> Tag:
        title = soup.find('h1', class_='Post-Title')
        if not title:
            raise Exception(f'failed to find title')

        title = title.string.strip()
        title_tag = Tag(name='title')
        title_tag.string = NavigableString(title)

        new_head = Tag(name='head')
        new_head.append(Tag(name='meta', attrs={'charset': 'utf-8'}, can_be_empty_element=True))
        new_head.append(title_tag)

        return new_head

    def _process_body(self, soup: BeautifulSoup) -> Tag:
        body = soup.body
        new_body = Tag(name='body')
        content = body.find('article', class_='Post-Main')

        tags = body.find_all('div', class_=self._div_class_filter)
        for tag in tags:
            tag.decompose()

        figures = body.find_all('figure')
        for figure in figures:
            figure.decompose()

        span_voters = body.find('span', class_='Voters')
        if span_voters:
            span_voters.decompose()

        new_body.append(content)
        return new_body

    @staticmethod
    def _div_class_filter(css_classes: [str]) -> bool:
        if css_classes is None:
            return False
        if 'Post-topicsAndReviewer' in css_classes:
            return True
        elif 'Post-Author' in css_classes:
            return True
        elif 'Sticky' in css_classes and 'RichContent-actions' in css_classes:
            return True
        return False


def test_zhihu_yyln_handler():
    from engine.request import Request

    logging.basicConfig(level=logging.INFO)

    handler = ZhiHuYYLNHandler()

    with open('./htmls/147779520.html') as input_file:
        data = input_file.read()
    response = Response(Request(), data)

    response = handler.handle_response(response)

    with open('./htmls/handle_result.html', 'w') as output_file:
        output_file.write(response.content)
