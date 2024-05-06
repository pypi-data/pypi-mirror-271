import copy
import datetime

import pandas as pd
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)


def remove_weird_chars(results):
    # results_json = json.loads(json.dumps(results.to_dict(), default=str))
    results_json = results

    new_res = {}

    for key in results_json.keys():
        old_key = key
        new_key = old_key.replace('.', '_')
        new_key = new_key.replace(' ', '_')
        new_key = new_key.replace('%', 'pcent')
        new_key = new_key.replace('[', '')
        new_key = new_key.replace(']', '')
        new_key = new_key.replace('(', '')
        new_key = new_key.replace(')', '')
        new_key = new_key.replace('$', '')
        new_key = new_key.replace('&', 'and')
        new_key = new_key.replace('#', 'n')
        new_key = new_key.replace('__', '_')
        new_key = new_key.lower()

        new_res[new_key] = results_json[old_key]

    return new_res

def dict_time_convert(stats):
    ret_res = {}
    
    for key in stats.keys():
        if isinstance(stats[key], pd.Timedelta):
            ret_res[key] = stats[key].total_seconds()
        elif isinstance(stats[key], pd.Timestamp):
            ret_res[key] = stats[key].to_pydatetime()
        else:
            ret_res[key] = stats[key]

    return ret_res

def result_maker(bt_stats, bt_params, bt_test_params, test_type):
    bt_stats = copy.deepcopy(bt_stats)
    bt_params = copy.deepcopy(bt_params)
    bt_test_params = copy.deepcopy(bt_test_params)
    test_type = copy.deepcopy(test_type)
                
    if '_trades' in bt_stats:
        del(bt_stats['_trades'])
    if '_strategy' in bt_stats:
        del(bt_stats['_strategy'])
    if '_equity_curve' in bt_stats:
        del(bt_stats['_equity_curve'])
        
    if '_id' in bt_test_params:
        del(bt_test_params["_id"])

    bt_stats = remove_weird_chars(bt_stats)
    bt_params = remove_weird_chars(bt_params)

    bt_stats = dict_time_convert(bt_stats)
    
    ret = {**bt_test_params, **bt_stats, **bt_params}
    ret['test_type'] = test_type
    ret['insert_timestamp'] = datetime.datetime.now()
        
    return ret


def list_maker(stats, test_params):
    list_doc = {}
    list_doc['insert_timestamp'] = datetime.datetime.now()
    list_doc['n_trades'] = stats['# Trades']
    list_doc['strategy'] = test_params['strategy']
    list_doc['period'] = test_params['period']
    list_doc['symbol'] = test_params['symbol']
    list_doc['trades_list'] = stats._trades.to_dict('records')
    
    td_list = []
    
    for item in list_doc['trades_list']:
        td_list.append(dict_time_convert(item))

    list_doc['trades_list'] = td_list
    ret = {**list_doc, **test_params}
    
    return ret
