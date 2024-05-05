from . import __version__
from ._shift import shift_data
from click import argument, command, option
from functools import wraps
from datetime import time, tzinfo
from pathlib import Path
import click
import dateutil  # type: ignore


def cli_type(func):
    @classmethod
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            raise click.BadParameter(str(e))

    return wrapped


class CliTypes:
    @cli_type
    def time(cls, value: str) -> time:
        return time.fromisoformat(value)

    @cli_type
    def timezone(cls, value: str) -> tzinfo:
        return get_timezone(value)


def get_timezone(timezone: str | tzinfo) -> tzinfo:
    if isinstance(timezone, tzinfo):
        return timezone

    tz = dateutil.tz.gettz(timezone)

    if tz is None:
        raise ValueError(f'invalid timezone {timezone!r}')

    return tz


@command(context_settings={
    'show_default': True,
    'help_option_names': ['-h', '--help'],
})
@click.version_option(__version__)
@option('-c', '--close', 'closing_time', required=True, type=CliTypes.time, help='Daily closing time')
@option('-z', '--timezone', default='America/New_York', type=CliTypes.timezone, help='Closing time timezone')
@option('--include-weekends', is_flag=True, default=False, help='Do not remove Saturday and Sunday data')
@argument('input_file', type=Path)
@argument('output_file', type=Path)
def cli(closing_time, timezone, include_weekends, input_file, output_file):
    '''
    Shift data time so that daily candle closes with price at CLOSING_TIME.

    INPUT_FILE is Forex Tester exported data with defaut settings,
    OUTPUT_FILE has the same format and can be imported back into
    Forex Tester with default settings.

    Example:

    \b
      shiftdata -c 18:00 XAUUSD.csv XAUUSD2.csv
      shiftdata -c 17:00 EURUSD.csv EURUSD2.csv

    In XAUUSD2.csv, 18:00 will be shifted to 00:00 so that after importing
    into Forex Tester, daily candle closing price becomes that of 17:59:59
    but the closing time becomes 23:59:59.
    Similarly for EURUSD2.csv but with different closing time.
    '''
    shift_data(
        input_file, output_file,
        closing_time=closing_time,
        tzinfo=timezone,
        include_weekends=include_weekends)
