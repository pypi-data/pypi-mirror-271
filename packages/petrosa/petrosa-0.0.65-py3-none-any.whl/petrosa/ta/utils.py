import datetime
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)



def strategy_output(
    ticker,
    timeframe,
    pet_datetime,
    entry_value,
    disruption_value,
    stop_loss,
    take_profit,
    direction
) -> dict:

    if (timeframe == 'm15'):
        minutes = 15
    elif (timeframe == 'm30'):
        minutes = 30
    elif (timeframe == 'h1'):
        minutes = 60
    elif (timeframe == 'd1'):
        minutes = 1440
    else:
        raise

    valid_until = pet_datetime + datetime.timedelta(minutes=minutes)

    ret = {}
    ret['ticker'] = ticker
    ret['datetime'] = pet_datetime
    ret['entry_value'] = entry_value
    ret['disruption_value'] = disruption_value
    ret['stop_loss'] = stop_loss
    ret['take_profit'] = take_profit
    ret['direction'] = direction
    ret['timeframe'] = timeframe
    ret['valid_until'] = valid_until

    return ret
