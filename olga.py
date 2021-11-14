import re

import pandas as pd
import pendulum


def parse_duration(duration):
    """Parse duration in string format MM:SS or HH:MM:SS as pendulum duration."""
    
    minutes = re.compile("\d{1,2}\:\d{1,2}")
    hours = re.compile("\d{1,2}\:\d{1,2}\:\d{1,2}")
    if hours.match(duration):
        return pendulum.parse(duration, exact=True) - pendulum.Time(0,0,0)
    elif minutes.match(duration):
        return pendulum.parse(":".join(["00", duration]), exact=True) - pendulum.Time(0,0,0)
    else:
        print("Please enter a valid duration in minutes (MM:SS) or hours (HH:MM:SS)")
        return None


vdot_table = pd.read_csv("vdot.csv", index_col=0, converters={i: parse_duration for i in range(1,10)})


def olga_bondarenko_interval(vdot):
    def pp(timedelta):
        """Pretty print timedelta rounded to seconds."""
        return timedelta.round(freq="s").__str__()[-8:]


    racetimes = vdot_table.loc[vdot,:]
    paces = {
        "recovery": racetimes.marathon / 42.190,
        "400m": racetimes._5k / 5,
        "300m": racetimes._1500m / 1.5,
        "200m": racetimes._1500m / 1.5 - pd.Timedelta("00:00:10"),
    }
    doc = f"""
    Your Olga Bondarenko interval training paces and times are:
      - recovery: {pp(paces['recovery'])} 
      - 400m:     {pp(paces['400m'])} ({pp((0.4 * paces['400m']))})
      - 300m:     {pp(paces['300m'])} ({pp((0.3 * paces['300m']))})
      - 200m:     {pp(paces['200m'])} ({pp((0.2 * paces['200m']))})
      - 100m:     sprint  
    """
    print(doc)
