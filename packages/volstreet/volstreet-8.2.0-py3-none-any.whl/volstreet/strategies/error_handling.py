import functools
import traceback
from inspect import signature
from datetime import datetime
from time import sleep
from volstreet import config
from volstreet.utils import (
    notifier,
    current_time,
    log_error,
)
from volstreet.strategies.monitoring import exit_positions


@log_error(notify=True, raise_error=True)
def exit_strategy(strategy: callable, execution_time: datetime, *args, **kwargs):
    sig = signature(strategy)
    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    order_tag = bound.arguments.get("strategy_tag")
    index = bound.arguments.get("underlying").name
    exit_positions(execution_time, index, order_tag)
    user_prefix = config.ERROR_NOTIFICATION_SETTINGS.get("user")
    user_prefix = f"{user_prefix} - " if user_prefix else ""
    notifier(
        f"{user_prefix}Exited positions for strategy {strategy.__name__}",
        webhook_url=config.ERROR_NOTIFICATION_SETTINGS["url"],
        send_whatsapp=True,
    )


def exit_on_error(strategy):
    @functools.wraps(strategy)
    def wrapper(*args, **kwargs):
        execution_time = current_time()
        try:
            return strategy(*args, **kwargs)
        except Exception as e:
            user_prefix = config.ERROR_NOTIFICATION_SETTINGS.get("user")
            user_prefix = f"{user_prefix} - " if user_prefix else ""
            sleep(4)  # Sleep for 4 seconds to allow the orders to be filled
            notifier(
                f"{user_prefix}"
                f"Error in strategy {strategy.__name__}: {e}\nTraceback:{traceback.format_exc()}\n\n"
                f"Exiting existing positions...",
                webhook_url=config.ERROR_NOTIFICATION_SETTINGS["url"],
                level="ERROR",
                send_whatsapp=True,
            )
            exit_strategy(strategy, execution_time, *args, **kwargs)

    return wrapper
