import typer

from gdshoplib.cli.crm.application import app as crm
from gdshoplib.cli.finance.application import app as finance
from gdshoplib.cli.product.application import app as product
from gdshoplib.cli.service.application import app as service
from gdshoplib.cli.stock.application import app as stock
from gdshoplib.cli.temporal.application import app as temporal

app = typer.Typer()

app.add_typer(crm, name="crm")
app.add_typer(temporal, name="temporal")
app.add_typer(finance, name="finance")
app.add_typer(product, name="product")
app.add_typer(service, name="service")
app.add_typer(stock, name="stock")

if __name__ == "__main__":
    app()
