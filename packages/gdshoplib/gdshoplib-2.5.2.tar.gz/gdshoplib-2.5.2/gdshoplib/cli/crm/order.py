import time
from typing import Optional

import typer

from gdshoplib.apps.crm.orders import Order

app = typer.Typer()


@app.command()
def on_request_update():
    # Взять все заказы, в нужном статусе
    # Обновить позиции на заказ
    for order in Order.query(params=Order.list_filter()):
        order.on_request.update()


@app.command()
def update(
    loop_iteration: Optional[int] = typer.Option(None),
    order_id: Optional[str] = typer.Option(None),
):
    # Обновить расчеты заказов
    if order_id:
        Order.update_one(order_id)
        return

    while True:
        Order.update()
        if loop_iteration:
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def set_commission():
    ...


@app.command()
def update_decline(loop_iteration: Optional[int] = typer.Option(None)):
    # Обновить расчеты заказов
    while True:
        Order.update_decline()
        if loop_iteration:
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def notify():
    # Разослать уведомление для менеджеров из CRM
    ...


if __name__ == "__main__":
    app()
