"""Console script for fhs_enyaq_data."""
import sys

import typer
from pprint import pprint
main = typer.Typer()

@main.command()
def list_car_types():
    from .abrp_list_cars import list_cars
    result = list_cars()
    for k in result:
        print(f"{k:40}  {result[k]}")


@main.command()
def get_data(
        vehicle_vin: str = typer.Option("", help="Extra help")
):
    from .fhs_enyaq_data import get_vehicle_data
    get_vehicle_data()

    return 0


@main.command()
def get_instruments(
):
    from .fhs_enyaq_data import print_instruments
    from .config import get_config
    config = get_config()
    print_instruments(config)

    return 0

@main.command()
def send_data(
        vehicle_vin: str = typer.Option("", help="Extra help"),
):
    from .fhs_enyaq_data import get_instruments
    from .config import get_config
    from .abrp_send import send_abrp
    config = get_config()
    instruments = get_instruments(config)
    pprint(instruments)
    send_abrp(config, instruments)

    return 0

@main.command()
def send_data_loop(
        idle_wait: int = typer.Option(10,  help="delay in idle wait"),
        drive_wait: int = typer.Option(5,  help="delay in drivemode wait"),
        charge_wait: int = typer.Option(5,  help="delay in charge wait"),
):
    from .loop import data_loop
    from .output import console_str
    data_loop(idle_wait, drive_wait, charge_wait, output=console_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
