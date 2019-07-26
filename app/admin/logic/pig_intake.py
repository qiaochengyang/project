# coding: utf8
from app.common.config.define_name import define_name, define_name_pigbase, define_name_pig_daily_assess
from app.common.util.input_checker import param_err, check_len, is_none


def intake_trend_action(params):
    pid = params.get('pid')
    start_time = params.get('startTime')
    end_time = params.get('endTime')

    if is_none(pid):
        return param_err('种猪id')

    if is_none(start_time):
        return param_err(define_name_pig_daily_assess['start_time'])

    if is_none(end_time):
        return param_err(define_name_pig_daily_assess['end_time'])

    return dict(type=True)



def total_perstation_action(params):
    stationid = params.get('stationId')
    time = params.get('time')

    if is_none(stationid) or not check_len(stationid, 12, 'le'):
        return param_err(define_name['stationid'])

    if is_none(time):
        return param_err('时间')

    return dict(type=True)
