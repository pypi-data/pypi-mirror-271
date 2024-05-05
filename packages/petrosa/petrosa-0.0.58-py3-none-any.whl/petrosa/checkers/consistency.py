import datetime
import pandas as pd
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)


def generate_benchmark_list(start: datetime.datetime, 
                            end: datetime.datetime, 
                            period: str):
    
    if period == '5m' or period == 'm5':
        minutes = 5
    elif period == '15m' or period == 'm15':
        minutes = 15
    elif period == '30m' or period == 'm30':
        minutes = 30
    elif period == '1h' or period == 'h1':
        minutes = 60
    else:
        minutes = 0

    datepointer = start        
    division_list = []
    
    while datepointer <= end:
        if(datepointer.minute % minutes == 0):
            division_list.append(datepointer.replace(second=0, microsecond=0))
        
        datepointer = datepointer + datetime.timedelta(minutes=1)
    
    division_list.pop(-1)
    
    return division_list


def check_consistency(start, 
                      end, 
                      actual , 
                      period: str) -> list:
    benchmark = generate_benchmark_list(start, end, period)
    
    lacking = []
    if isinstance(actual, pd.Series):
        actual = actual.to_list()
    
    for item in benchmark:
        if isinstance(item, pd.Timestamp):
            item = item.to_pydatetime()
        if item not in actual:
            lacking.append(item)
            
    return lacking
