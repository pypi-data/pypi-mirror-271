import pandas as pd
import numpy as np
from odhpy import utils
from odhpy import stats


def mean_annual_flow(df: pd.DataFrame, wy_month=7):
    """
    MEAN ANNUAL FLOW
    This EFO INDICATOR is the mean flow in ML/y.

    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    ans = stats.annual_mean(df, wy_month).values[0]
    description = f"Mean annual flow (ML/y)"
    return {"Description": description, "Value": ans}


def days_in_no_flow_periods(df: pd.DataFrame, flow_threshold=2, duration_days=60, as_percentage=True):
    """
    DAYS IN NO-FLOW PERIODS (WATERHOLES)
    This EFO INDICATOR measures the occurance of undesirable periods when the flow effectivley 
    ceases (<=2ML/d) for longer than a given duration. The EFO says the percentage of days in 
    'no flow periods' cannot increase above some given value.
    
    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    col = df.columns[0]
    duration_days_excl = duration_days + 1
    current_spell = 0
    total_days = 0
    for idx, value in df[col].items():
        if value <= flow_threshold:
            current_spell += 1
            if current_spell < duration_days_excl:
                pass
            elif current_spell == duration_days_excl:
                #current_spell just became long enough to count
                total_days += current_spell
            else:
                #long run is continuing
                total_days += 1 
        else:
            current_spell = 0
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    description = f"Days when flow <={flow_threshold} ML/d for longer than {duration_days} days ({'%' if as_percentage else '# days'})"
    return {"Description": description, "Value": ans}


def days_in_ecological_low_flow_periods(df: pd.DataFrame, flow_threshold, duration_days, months=[1,2,3,4,5,6,7,8,9,10,11,12], as_percentage=True):
    """
    ECOLOGICAL LOW FLOW PERIODS
    This EFO INDICATOR measures the occurance of undesirable low-flow periods, in certain months.
    The EFO says the percentage of days in 'ecological asset low flow periods' in certain months 
    cannot increase above some given value. And it defines 'ecological asset low flow periods' as 
    periods longer than some duration_days, when the flow was less than some flow_threshold.

    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    col = df.columns[0]
    duration_days_excl = duration_days + 1
    total_days = 0
    current_spell = 0
    current_season_days = 0
    for idx, value in df[col].items():
        month_int = int(idx[5:7])
        if month_int in months:
            current_season_days += 1
        else:
            current_season_days = 0
        if value > flow_threshold:
            current_spell = 0
        else:
            current_spell += 1
            if current_spell < duration_days_excl:
                pass 
            elif current_spell == duration_days_excl:
                #current_spell just became long enough to count
                total_days += min(current_spell, current_season_days)
            else:
                if current_season_days > 0:
                    #long run is continuing
                    total_days += 1
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    description = f"Days when flow <={flow_threshold} ML/d for longer than {duration_days} days in this season={months} ({'%' if as_percentage else '# days'})"
    return {"Description": description, "Value": ans}


def days_in_riffle_periods(df: pd.DataFrame, lower_threshold, upper_threshold, as_percentage=True):
    """ 
    DAYS IN RIFFLE PERIODS
    This EFO INDICATOR is about maintaining the number of days in desirable flow range 
    beneficial to riffle habitat. There is an upper and lower threshold. There is no 
    duration requirement, or seasonal component.

    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    col = df.columns[0]
    total_days = ((df[col] >= lower_threshold) & (df[col] <= upper_threshold)).sum()
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    description = f"Days when {lower_threshold}<= flow <={upper_threshold} ML/d ({'%' if as_percentage else '# days'})"
    return {"Description": description, "Value": ans}


def days_in_riffle_drown_out_periods(df: pd.DataFrame, flow_threshold, as_percentage=True):
    """ 
    DAYS IN RIFFLE DROWN-OUT PERIODS
    This EFO INDICATOR measures the number of days in undesirable flow ranges above the 
    riffle-drown-out threshold, when the water level is above the rocks and airation is
    less effective. This is used instead of "days_in_riffle_periods" used in some 
    water plans.

    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    col = df.columns[0]
    total_days = (df[col] >= flow_threshold).sum()
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    description = f"Days when flow >={flow_threshold} ML/d ({'%' if as_percentage else '# days'})"
    return {"Description": description, "Value": ans}


def days_in_river_forming_periods(df: pd.DataFrame, flow_threshold, as_percentage=True):
    """
    DAYS IN RIVER FORMING PERIODS
    This EFO INDICATOR measures the number of days in high-flow periods necessary for 
    river forming processes. Note this is not exactly the same as 
    "days_in_riffle_drown_out_periods" because that compares using '>=' while this 
    compares using '>'.

    Returns:
        _type_: _description_
    """
    utils.assert_df_has_one_column(df)
    col = df.columns[0]
    total_days = (df[col] > flow_threshold).sum()
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    description = f"Days when flow >{flow_threshold} ML/d ({'%' if as_percentage else '# days'})"
    return {"Description": description, "Value": ans}


def days_in_riparian_low_flow_periods(df: pd.DataFrame, flow_threshold, duration_days=365, as_percentage=True):
    """
    DAYS IN RIPARIAN (OR FLOODPLAIN VEG) LOW FLOW PERIODS
    This EFO INDICATOR measures undesirable periods between the floods necessary for 
    riparian and floodplain health. The plan defines these undesirable periods as 
    periods longer than 1 year (duration_days=365) when the flow was less than some 
    flow_threshold. 
    
    Returns:
        _type_: _description_
    """
    ans = days_in_no_flow_periods(df, flow_threshold, duration_days, as_percentage)
    return ans
