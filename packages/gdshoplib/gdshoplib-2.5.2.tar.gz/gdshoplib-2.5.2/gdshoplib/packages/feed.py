import datetime

from lxml import etree, objectify

from gdshoplib.apps.products.product import Product
from gdshoplib.core.settings import FeedSettings
from gdshoplib.packages.s3 import S3, SimpleS3Data


class Feed:
    DESCRIPTION_TEMPLATE = "basic.txt"
    KEY = "basic"

    @classmethod
    def get_platform_class(cls, key):
        for platform in cls.__subclasses__():
            if platform.KEY.lower() == key.lower():
                return platform
        return cls

    def __init__(self):
        self.feed_settings = FeedSettings()
        self.root = self.get_root()

    def get_root(self):
        root = etree.Element("yml_catalog")
        objectify.deannotate(root, cleanup_namespaces=True, xsi_nil=True)
        root.attrib["date"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        return root

    def get_shop(self):
        shop = objectify.Element("shop")

        shop.name = self.feed_settings.SHOP_NAME
        shop.company = self.feed_settings.COMPANY_NAME
        shop.url = self.feed_settings.SHOP_URL
        currencies = objectify.Element("currencies")
        currency = etree.Element("currency")
        currency.attrib["id"] = "RUB"
        currency.attrib["rate"] = "1"
        objectify.deannotate(currency, cleanup_namespaces=True, xsi_nil=True)
        objectify.deannotate(currencies, cleanup_namespaces=True, xsi_nil=True)
        currencies.append(currency)
        shop.currencies = currencies
        objectify.deannotate(shop, cleanup_namespaces=True, xsi_nil=True)

        return shop

    def get_offers(self, products):
        offers = etree.Element("offers")
        objectify.deannotate(offers, cleanup_namespaces=True, xsi_nil=True)
        for product in products:
            offers.append(self.get_offer(product))

        return offers

    @classmethod
    def get_old_price(cls, product):
        if (
            product.price.now <= product.price.profit / 1.05
        ):  # Старую цену можно указывать, только если разница больше 5%
            return product.price.profit

    def get_media_url(self, media):
        badged = S3(
            SimpleS3Data(
                None,
                None,
                None,
                file_info={
                    "id": media.id,
                    "format": "png",
                    "prefix": "BADGED",
                },
                parent=media.parent,
            )
        )
        if badged.exists():
            return media.get_url(file_key=badged.data.file_key)
        return media.get_url()

    def get_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.attrib["available"] = str(product.available()).lower()
        appt.currencyId = "RUB"
        appt.price = product.price.now
        appt.title = product.name
        appt.name = product.name
        appt.vendor = product.brand.title
        appt.delivery = "true"
        appt.description = product.description.generate(self)

        if self.get_old_price(product):
            appt.oldprice = self.get_old_price(product)

        for image in product.images:
            appt.addattr("picture", self.get_media_url(image))

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt

    def get_feed(self):
        shop = self.get_shop()
        shop.append(self.get_offers(self.products))
        self.root.append(shop)
        return etree.tostring(
            self.root,
            pretty_print=True,
            encoding="utf-8",
            xml_declaration=True,
            standalone=True,
        )

    @property
    def products(self):
        return Product.query(filter=self.product_filter)

    @property
    def product_filter(self):
        return dict(status_description="Готово", status_publication="Публикация")

    def get_s3_container(self, content):
        return S3(
            SimpleS3Data(
                content, file_key=f"feed.{self.KEY.lower()}", mime="application/xml"
            )
        )

    def push_feed(self):
        s3 = self.get_s3_container(self.get_feed())
        s3.put()
