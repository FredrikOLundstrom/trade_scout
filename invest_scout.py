"""
Date: 2020-05-15
Author: Fredrik Lundström

This is a micro console-app that simply automates looking for an arbitrage opportunity
in between Spago and Spago BTA. This is simply a fun tool that I built to observe a
share and its BTA neighbor without spending much time looking on it.
"""
# pylint: disable=invalid-name
import os
import time
import datetime
import atexit
import sys
import pandas as pd
import avanza

global FILE_NAME
global MUTE
global span_log

MUTE = False
FILE_NAME = 'span_log.csv'
ex = avanza.Ticker(393036)
properties = dir(ex)
properties_public = [x for x in properties if x[0] != '_']
cols = list(['todays_datetime'])
cols.extend(properties_public)

try:
    span_log = pd.read_csv(FILE_NAME)
except:
    span_log = pd.DataFrame(columns=cols)

def save_log():
    """Save to file, called on exit"""
    FILE_NAME = 'span_log.csv'
    print('Saving log...')
    span_log.to_csv(FILE_NAME, index=False, encoding='utf-8')

def exit_handler():
    """Graceful exit, save log"""
    save_log()
    print('Investerings spanaren stängs ner!')

def rules(delta_, spago_, spago_bta_):
    """Simple arbitrage rules or add new more complex"""
    switch = False
    #yesterday_high = span_log
    #yesterday_low = span_log
    if delta_ > 0.6:
        if MUTE:
            os.system('say "Undersök köp, högt arbitrage"')
        print("Högt arbitrage, {}>0.6".format(delta_))
        switch = True
    if spago_bta_.sell_price < 4.8:
        if MUTE:
            os.system('say "Undersök köp, lågt B T A pris"')
        print("Högt aktiepris, {}<4.8".format(spago_bta_.sell_price))
        switch = True
    if spago_.buy_price > 5.5:
        if MUTE:
            os.system('say "Undersök köp, högt aktiepris"')
        print("Högt aktiepris, {}>5.5".format(spago_.buy_price))
        switch = True
    if spago_.change_percent > 3 or spago_.change_percent < -3:
        print('Stor förändring i Spago\'s pris: {}%'.format(spago_.change_percent))
    if spago_bta_.change_percent > 3 or spago_bta_.change_percent < -3:
        print('Stor förändring i BTA pris: {}%'.format(spago_bta_.change_percent))
    #if spago_.highest_price == spago_.last_price:
    #    print('Nuvarande pris är dagshögsta (Spago)')
    #if spago_bta_.highest_price == spago_bta_.last_price:
    #    print('Nuvarande pris är dagshögsta (Spago BTA)')
    #if span_log[span_log[]]['highest_price']
    #if switch and True:
        #input('Tryck enter för att återgå') != "0":
        #print("")
    #IDÉ 1: Teknisk analys (EMA passerar annan EMA)
    #IDE 2:

i = 0
os.system('say "Startar investerings spanaren Spago"')
atexit.register(exit_handler)

while True:
    i += 1
    now = datetime.datetime.now()
    todays_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    curr_h = now.hour
    curr_m = now.minute
    market_hours = False
    if curr_h > 8 and curr_h < 18 and not(curr_h == 17 and curr_m > 30):
        market_hours = True
    market_day = now.weekday() < 5
    market_open = market_day and market_hours

    if not market_open:
        print("""{}, Iteration: {}
        Zzz... Marknaden sover""".format(todays_datetime, i))
        time.sleep(5*60)
    else:
        if i % 10 == 0:
            os.system('say "Iteration {}"'.format(i))

        shares = [avanza.Ticker(393036), avanza.Ticker(1086441)]

        spago = shares[0]
        spago_bta = shares[1]

        delta = round(spago.buy_price-spago_bta.sell_price, 4)
        print(
            """{}, Iteration: {}
        Bid: {}, Ask: {}, SPAGO
        Bid: {}, Ask: {}, SPAGO BTA
        DELTA: {}, (Spago Bid – BTA Ask)

        Vinst vid omsatta    500 aktier: {},
        Vinst vid omsatta  1,000 aktier: {},
        Vinst vid omsatta  2,000 aktier: {},
        Vinst vid omsatta  5,000 aktier: {},
        Vinst vid omsatta 10,000 aktier: {},

        Öka antalet från    500 till {}
        Öka antalet från  1,000 till {}
        Öka antalet från  2,000 till {}
        Öka antalet från  5,000 till {}
        Öka antalet från 10,000 till {}
        _____________________________________________
            """
            .format(
                now,
                i,
                spago.buy_price,
                spago.sell_price,
                spago_bta.buy_price,
                spago_bta.sell_price,
                delta,
                (delta*500)-60,
                (delta*1000)-60,
                (delta*2000)-60,
                (delta*5000)-130,
                (delta*10000)-280,
                round(((spago.buy_price*500)-30) / spago_bta.sell_price, 1) - 10,
                round(((spago.buy_price*1000)-30) / spago_bta.sell_price, 1) - 10,
                round(((spago.buy_price*2000)-30) / spago_bta.sell_price, 1) - 10,
                round(((spago.buy_price*5000)-65) / spago_bta.sell_price, 1) - 20,
                round(((spago.buy_price*10000)-140) / spago_bta.sell_price, 1) - 40,
            )
        )
        rules(delta, spago, spago_bta)

        time.sleep(1*20)

        shares = [avanza.Ticker(393036), avanza.Ticker(1086441)]
        for x in range(len(shares)):
            try:
                span_log.loc[len(span_log)] = [
                    now,
                    shares[x].buy_price,
                    shares[x].change,
                    shares[x].change_percent,
                    shares[x].country,
                    shares[x].currency,
                    shares[x].data,
                    shares[x].flag_code,
                    shares[x].get,
                    shares[x].highest_price,
                    shares[x].id,
                    shares[x].info,
                    shares[x].isin,
                    shares[x].last_price,
                    shares[x].last_price_updated,
                    shares[x].lowest_price,
                    shares[x].marketplace,
                    shares[x].name,
                    shares[x].quote_updated,
                    shares[x].sell_price,
                    shares[x].session,
                    shares[x].set,
                    shares[x].symbol
                ]
            except:
                print(shares, file=sys.stderr)
        if i % 20 == 0:
            save_log()
