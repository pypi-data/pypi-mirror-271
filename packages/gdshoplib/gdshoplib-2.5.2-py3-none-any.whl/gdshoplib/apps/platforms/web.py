import re

from lxml import etree, objectify

from gdshoplib.apps.platforms.base import Platform
from gdshoplib.core.settings import ProductSettings
from gdshoplib.packages.feed import Feed
from gdshoplib.services.notion.database import Database


class WebManager(Platform, Feed):
    KEY = "WEB"
    DESCRIPTION_TEMPLATE = "web.txt"

    def __init__(self, *args, **kwargs):
        self._categories = set()
        super().__init__(*args, **kwargs)

    def get_categories(self):
        categories = objectify.Element("categories")
        category = etree.Element("category")
        category.attrib["id"] = str(1)
        category.text = "Конный спорт"
        categories.append(category)

        for _id, name in [
            (str(i.uid), i.title)
            for i in Database(ProductSettings().CATEGORY_DB).pages()
        ]:
            category = etree.Element("category")
            category.attrib["id"] = _id
            category.attrib["parentId"] = "1"
            category.text = name
            objectify.deannotate(category, cleanup_namespaces=True, xsi_nil=True)
            categories.append(category)

        objectify.deannotate(categories, cleanup_namespaces=True, xsi_nil=True)
        return categories

    @staticmethod
    def fetch_id(id):
        return str(sum([int(i) for i in re.sub(r"\D*", "", id)]))

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

    def get_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.count = product.quantity
        if product.quantity == 0:
            appt.attrib["type"] = "on.demand"

        appt.currencyId = "RUB"
        appt.price = product.price.base_price

        for image in product.images:
            appt.addattr("picture", image.get_url())

        if product.color:
            attr = etree.Element("param")
            attr.attrib["name"] = "Цвет"
            attr.text = str(product.color)

            objectify.deannotate(attr, cleanup_namespaces=True, xsi_nil=True)
            appt.append(attr)

        if product.size:
            attr = etree.Element("param")
            attr.attrib["name"] = "Размер"
            attr.text = str(product.size)

            objectify.deannotate(attr, cleanup_namespaces=True, xsi_nil=True)
            appt.append(attr)

        appt.sku = product.sku
        appt.oldprice = product.price.now
        appt.name = product.name
        appt.description = product.description.generate(self)
        appt.vendor = product.brand.title
        category_id = str(product.categories[0].uid)
        appt.categoryId = category_id
        self._categories.add(category_id)

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt

    def get_feed(self):
        shop = self.get_shop()
        offers = self.get_offers(self.products)
        shop.categories = self.get_categories()
        shop.append(offers)
        self.root.append(shop)
        return etree.tostring(
            self.root,
            pretty_print=True,
            encoding="utf-8",
            xml_declaration=True,
            standalone=True,
        )
