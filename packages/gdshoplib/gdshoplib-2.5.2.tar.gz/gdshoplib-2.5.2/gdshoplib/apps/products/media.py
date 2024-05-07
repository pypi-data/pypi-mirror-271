import re

import backoff
from PIL import ImageDraw, ImageFont

import requests
from gdshoplib.core.settings import GeneralSettings
from gdshoplib.packages.renderer import ImageRenderer
from gdshoplib.packages.s3 import S3
from gdshoplib.services.notion.block import Block
from gdshoplib.services.notion.page import Page


class ProductMedia(Block):
    def __init__(self, *args, **kwargs):
        super(ProductMedia, self).__init__(*args, **kwargs)
        self.response = None
        self.s3 = S3(self)

    @property
    def url(self):
        return self[self.type]["file"]["url"]

    @property
    def badges(self):
        result = []
        for badge in self.parent.badges:
            if not badge.work or not badge.file:
                continue
            result.append(badge)
        return result

    @property
    def key(self):
        return self.notion.get_capture(self) or f"{self.type}_general"

    def fetch(self):
        self.access() or self.refresh()
        self.s3.get() or self.s3.put()

        return self.s3.get()

    def get_url(self, file_key=None):
        return f"{self.s3.s3_settings.ENDPOINT_URL}/{self.s3.s3_settings.BUCKET_NAME}/{file_key or self.file_key}"

    @property
    def file_key(self):
        return f"{self.parent.sku}.{self.id}.{self.format}"

    def access(self):
        return requests.get(self.url).ok

    def exists(self):
        return self.s3.exists()

    @property
    def name(self):
        pattern1 = re.compile(r".*\/(?P<name>.*)")
        r = re.findall(pattern1, self.url)
        if not r or not r[0]:
            return None
        return r[0].split("?")[0]

    @property
    def format(self):
        pattern = re.compile(r"\/.*\.(\w+)(\?|$)")
        r = re.findall(pattern, self.url)
        return r[0][0] if r else None

    @backoff.on_exception(
        backoff.expo,
        (
            requests.ReadTimeout,
            requests.ConnectTimeout,
            requests.Timeout,
            requests.JSONDecodeError,
            requests.ConnectionError,
            requests.HTTPError,
        ),
        max_tries=8,
    )
    def request(self):
        response = requests.get(self.url)
        if not response.ok:
            raise MediaContentException
        response.raise_for_status()
        return response

    def get_content(func):
        def wrap(self, *args, **kwargs):
            if not self.response:
                if not self.access():
                    self.refresh()
                self.response = self.request()
            return func(self, *args, **kwargs)

        return wrap

    @property
    @get_content
    def content(self):
        return self.response.content

    @property
    @get_content
    def hash(self):
        return self.response.headers.get("x-amz-version-id")

    @property
    @get_content
    def mime(self):
        return self.response.headers.get("content-type")

    def get_badge_coordinates(self, badge):
        assert isinstance(badge, Page)
        # Если число отрицательное, посчитать позицию относительно координат базового изображения
        source_coordinates = [
            int(point.strip()) for point in badge.coordinates.split(",")
        ]
        plot = ImageRenderer(self.content)
        size = self.get_size(badge)
        result = []
        for i, s in enumerate(source_coordinates):
            point = s
            if s < 0:
                point = (plot.info["size"][i] + s) - size[i]
            result.append(point)

        return result

    def get_size(self, badge):
        assert isinstance(badge, Page)
        # Если указан знак %, то посчитать относительный размер
        if "%" in badge.size:
            percentage = int(re.sub(r"\W", "", badge.size))
            plot = ImageRenderer(self.content)
            result = [int(point / 100 * percentage) for point in plot.info["size"]]
        else:
            result = [int(point.strip()) for point in badge.size.split(",")]
        return result

    def apply_badges(self):
        if self.type not in ("image",):
            return self

        result = ImageRenderer(self.content)
        for badge in self.badges:
            if not requests.get(badge.file).ok:
                badge.refresh()

            _badge = ImageRenderer(badge.file)
            if badge.size:
                _badge.resize(self.get_size(badge))
            if badge.transparency:
                _badge.set_transparency(badge.transparency)
            result.paste(_badge, self.get_badge_coordinates(badge))

        # discount = ImageDraw.Draw(result)
        # myFont = ImageFont.truetype(
        #     str(GeneralSettings().TEMPLATES_PATH / 'BungeeSpice-Regular.ttf'.resolve()),
        #     72
        # )
        # discount.text((0, 0), "Sample text", font=myFont, fill=(255, 0, 0))
        return result


class MediaContentException(Exception):
    ...


class S3File:
    def __init__(self, url) -> None:
        self.response = None
        self.url = url

    def access(self):
        return requests.get(self.url).ok

    @property
    def format(self):
        pattern = re.compile(r"\/.*\.(\w+)(\?|$)")
        r = re.findall(pattern, self.url)
        return r[0][0] if r else None

    def request(self):
        response = requests.get(self.url)
        if not response.ok:
            raise MediaContentException
        return response

    def get_content(func):
        def wrap(self, *args, **kwargs):
            if not self.response:
                if not self.access():
                    raise NeedRefresh
                self.response = self.request()
            return func(self, *args, **kwargs)

        return wrap

    @property
    @get_content
    def content(self):
        return self.response.content

    @property
    @get_content
    def hash(self):
        return self.response.headers.get("x-amz-version-id")

    @property
    @get_content
    def mime(self):
        return self.response.headers.get("content-type")


class NeedRefresh(Exception):
    ...
