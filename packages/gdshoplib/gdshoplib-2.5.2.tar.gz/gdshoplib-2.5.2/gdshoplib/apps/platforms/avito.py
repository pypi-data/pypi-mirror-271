from lxml import etree, objectify

from gdshoplib.apps.platforms.base import Platform
from gdshoplib.packages.feed import Feed


class AvitoManager(Platform, Feed):
    KEY = "AVITO"
    DESCRIPTION_TEMPLATE = "avito.txt"

    def get_root(self):
        root = etree.Element("Ads")
        objectify.deannotate(root, cleanup_namespaces=True, xsi_nil=True)
        root.attrib["target"] = "Avito"
        root.attrib["formatVersion"] = "3"
        return root

    def get_offer(self, product):
        appt = objectify.Element("Ad")
        appt.Id = product.sku
        appt.Title = product.name
        appt.Category = self.feed_settings.AVITO_CATEGORY
        appt.ListingFee = "Package"
        appt.AdStatus = "Free"
        appt.ContactMethod = "По телефону и в сообщениях"
        appt.Condition = "Новое"
        appt.Description = product.description.render(self)
        appt.Delivery = "Свой курьер"
        appt.Address = self.feed_settings.ADDRESS
        appt.Price = product.price.now
        appt.ManagerName = self.feed_settings.MANAGER_NAME
        appt.ContactPhone = self.feed_settings.PHONE
        appt.Stock = product.quantity

        images = objectify.Element("Images")
        for image in product.images:
            i = objectify.Element("Image")
            i.attrib["url"] = self.get_media_url(image)
            images.append(i)

        appt.append(images)

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt

    def get_feed(self):
        for product in self.products:
            self.root.append(self.get_offer(product))

        return etree.tostring(
            self.root,
            pretty_print=True,
            encoding="utf-8",
            xml_declaration=True,
            standalone=True,
        )
