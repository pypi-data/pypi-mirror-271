import datetime
import time
from typing import Optional

from pydantic import BaseModel

from gdshoplib.apps.crm.cart import Cart
from gdshoplib.apps.crm.on_request import (OnRequestTable,
                                           OnRequestTableInvalidRow)
from gdshoplib.apps.products.price import Price
from gdshoplib.apps.products.product import Product
from gdshoplib.core.settings import CRMSettings
from gdshoplib.services.gdshop.gdshop import DB
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.notion import Notion
from gdshoplib.services.notion.page import Page


class Order(Page):
    SETTINGS = CRMSettings()

    def __init__(self, *args, **kwargs):
        self._on_request = None
        self._products = None

        super(Order, self).__init__(*args, **kwargs)

    def __len__(self):
        return len(self.products) + sum([row.quantity for row in self.on_request])

    @staticmethod
    def list_filter(filter_type="raw"):
        if filter_type == "raw":
            return {
                "filter": {
                    "or": [
                        {"property": "Status", "status": {"equals": "Расчет"}},
                    ]
                }
            }
        elif filter_type == "complited_shop":
            return {
                "filter": {
                    "and": [
                        {"property": "Status", "status": {"equals": "Доставлено"}},
                        {"property": "Тип заказа", "select": {"equals": "Магазин"}},
                    ]
                }
            }
        elif filter_type == "complited_agent":
            return {
                "filter": {
                    "and": [
                        {"property": "Status", "status": {"equals": "Доставлено"}},
                        {"property": "Тип заказа", "select": {"equals": "Agent"}},
                    ]
                }
            }
        elif filter_type == "complited":
            return {
                "filter": {
                    "or": [
                        {
                            "property": "Status",
                            "status": {"does_not_equal": "Доставлено"},
                        },
                        {"property": "Status", "status": {"does_not_equal": "Отказ"}},
                        {
                            "property": "Status",
                            "status": {"does_not_equal": "Оформление"},
                        },
                        {"property": "Status", "status": {"does_not_equal": "Оплата"}},
                    ]
                }
            }
        elif filter_type == "actual":
            return {
                "filter": {
                    "or": [
                        {
                            "property": "Status",
                            "status": {"does_not_equal": "Комплектация"},
                        },
                        {
                            "property": "Status",
                            "status": {"does_not_equal": "Неразобранное"},
                        },
                        {"property": "Status", "status": {"does_not_equal": "Отказ"}},
                    ]
                }
            }
        elif filter_type == "waiting":
            return {
                "filter": {
                    "or": [
                        {"property": "Status", "status": {"equals": "Оплата"}},
                        {"property": "Status", "status": {"equals": "Комплектация"}},
                    ]
                }
            }
        elif filter_type == "new":
            return {
                "filter": {"property": "Status", "status": {"equals": "Неразобранное"}}
            }

    @classmethod
    def get(cls, id):
        page = [
            page
            for page in Database(cls.SETTINGS.CRM_DB).pages(
                params={
                    "filter": {
                        "property": "ID заказа",
                        "rich_text": {
                            "equals": id,
                        },
                    }
                }
            )
        ]
        if not page:
            return
        if len(page) > 1:
            raise OrderIDDuplicate

        page = page[0]

        return cls(page["id"], notion=page.notion, parent=page.parent)

    @classmethod
    def query(cls, filter=None, params=None, notion=None):
        for page in Database(cls.SETTINGS.CRM_DB, notion=notion).pages(
            filter=filter, params=params
        ):
            yield cls(page["id"], notion=page.notion, parent=page.parent)

    @property
    def on_request(self):
        if not self._on_request:
            self._on_request = OnRequestTable(
                [block for block in self.blocks(filter={"type": "table_row"})],
                notion=self.notion,
                parent=self,
            )

        return self._on_request

    @property
    def products(self):
        if not self._products:
            self._products = [Product(page.id) for page in self.products_field]
        return self._products

    def requested_price(self, product):
        return product.price.profit - product.price.profit * (self.discount * 0.01)

    @property
    def delivery(self):
        return

    @property
    def pay(self):
        return

    @property
    def discount_sum(self):
        return round(self.full_price - self.price, 2)

    @property
    def max_discount(self):
        # Расчет максимальной скидки
        if self.order_type != "Магазин":
            return 0

        now = self.on_request.price()
        for product in self.products:
            now += product.price.now
        lowest = self.on_request.price()
        for product in self.products:
            lowest += product.price.neitral

        result = now - lowest
        if not result:
            return 0
        return round((result) / (now * 0.01))

    def get_promocode(self):
        if not self.promocodes or self.order_type != "Магазин":
            return None
        self.promocodes.sort(key=lambda x: x.discount)
        return self.promocodes[0]

    @property
    def price(self):
        result = self.on_request.price()
        for product in self.products:
            result += product.price.now
        return result
        result = self.on_request.price()
        for product in self.products:
            if self.order_type == "Агент":
                result += product.price.neitral
            else:
                promocode = self.get_promocode()
                if promocode and product.price.current_discount < promocode.discount:
                    _price = (
                        product.price.profit
                        if product.price.profit > product.price.now
                        else product.price.now
                    )
                    result += _price - _price * (promocode.discount * 0.01)
                else:
                    result += product.price.now

        return round(result - result * (self.discount * 0.01))

    @property
    def full_price(self):
        result = self.on_request.price()
        for product in self.products:
            result += (
                product.price.profit
                if product.price.profit > product.price.now
                else product.price.now
            )

        return result

    @property
    def profit(self):
        profit = self.on_request.price("profit")
        for product in self.products:
            profit += product.price.profit
        return profit

    @property
    def commission(self):
        commission = self.on_request.price("profit") * 0.3
        for product in self.products:
            commission += product.price.profit * 0.15
        return round(commission)

    def generate_id(self):
        return f"{self.platform.key.lower()}.{int(time.time())}"

    def description_on_request_product(self, row):
        quantity = f"({row.quantity} шт.)"
        return f"{row.name} {quantity if row.quantity > 1 else ''}: {Price(row)['neitral'] * row.quantity} ₽"

    def description_basic_product(self, product):
        _price = (
            product.price.profit
            if product.price.profit > product.price.now
            else product.price.now
        )
        return f"{product.name}: {_price} ₽"

    @property
    def description(self):
        result = ["Ваш заказ\n"]
        counter = 1

        for row in self.on_request:
            if isinstance(row, OnRequestTableInvalidRow):
                continue
            result.append(f"{counter}. {self.description_on_request_product(row)}")
            counter += 1

        for product in self.products:
            result.append(f"{counter}. {self.description_basic_product(product)}")
            counter += 1

        if self.delivery or self.discount_sum:
            result.append(f"\nТовары ({len(self)}): {self.full_price}")

        if self.get_promocode():
            promocode = self.get_promocode()
            result.append(f"Промокод: {promocode.title} (-{promocode.discount}%)")

        if self.discount_sum:
            result.append(f"Скидка: {self.discount_sum}")

        if self.delivery:
            result.append(f"Стоимость доставки: {self.delivery.price}")

        result.append(f"\nОбщая стоимость: {self.price}")

        return "\n".join(result)

    def set_id(self):
        # Установить ID
        if not self.platform:
            return

        self.notion.update_prop(
            self.id,
            params={
                "properties": {"ID заказа": [{"text": {"content": self.generate_id()}}]}
            },
        )

    def set_max_discount(self):
        # Установка максимальной скидки
        self.notion.update_prop(
            self.id,
            params={"properties": {"max Скидка": {"number": self.max_discount or 0}}},
        )

    def set_price_description(self):
        # Установка описания расчетов цены
        self.notion.update_prop(
            self.id,
            params={
                "properties": {
                    "Расчеты": [{"text": {"content": self.description or ""}}]
                }
            },
        )

    def set_price(self):
        # Установка итоговой цены
        self.notion.update_prop(
            self.id,
            params={"properties": {"Итого": {"number": self.price}}},
        )

    def set_profit(self):
        # Установка итоговой цены
        self.notion.update_prop(
            self.id,
            params={"properties": {"Прибыль": {"number": self.profit}}},
        )

    def set_commission(self):
        # Установка комиссии менеджера
        self.notion.update_prop(
            self.id,
            params={"properties": {"Комиссия": {"number": self.commission}}},
        )

    def update_status(self, status):
        # Установка итоговой цены
        self.notion.update_prop(
            self.id,
            params={"properties": {"Status": {"status": {"name": status}}}},
        )

    def load_tasks(self):
        # Загрузка задач в CRM из источников
        ...

    def get_cart(self):
        # Получить список строк из базы
        return Cart.get(self.id)

    def update_cart(self):
        # Получить список всех товаров в карточке
        # Получить таблицу в расчетами
        cart = self.get_cart()
        for product in self.products:
            if product not in cart:
                cart.extend(product)
        # Добавить элементы карточки в таблицу
        # Обновить таблицу целиком
        ...

    @classmethod
    def update(cls):
        # Обновление карточки Order
        for order in cls.query(
            notion=Notion(caching=True), params=cls.list_filter(filter_type="raw")
        ):
            order.set_profit()
            order.set_price()
            order.set_commission()

            order.update_status("Комплектация")
            if not order.pk:
                order.set_id()

    @classmethod
    def update_one(cls, id):
        order = Order.get(id)
        order.set_profit()
        order.set_price()
        order.set_commission()

        order.update_status("Комплектация")

    @classmethod
    def update_decline(cls):
        date = datetime.date.today() - datetime.timedelta(days=7)
        for order in cls.query(
            notion=Notion(caching=True), params=cls.list_filter(filter_type="waiting")
        ):
            if order.edited_time.date() < date:
                order.update_status("Отказ")

    def notification(self):
        # Отправка уведомлений
        ...


class OrderIDDuplicate(Exception):
    ...
