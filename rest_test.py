# -*- encoding: utf-8 -*-
from requests import get
import pandas as pd
from datetime import datetime, timedelta, timezone
from json import loads
from os import system

URL = 'http://worldclockapi.com/api/json/est/now'
JSON_DATETIME = 'currentDateTime'
JSON_UTC = 'utcOffset'
TIMEOUT = 1  # таймаут в минутах


def main():
    i = 60
    while True:
        try:
            local_time = datetime.now(timezone.utc).astimezone()
            response = get(URL)
            if response.status_code != 200 or -TIMEOUT < local_time.minute - i < TIMEOUT:
                continue

            i = local_time.minute
            json_dt = loads(response.text)[JSON_DATETIME][:16]
            dt_stamp = datetime.strptime(json_dt, "%Y-%m-%dT%H:%M").timestamp()  # Unix timestamp, т.к. нужна поправка на часовой пояс
            json_utc = loads(response.text)[JSON_UTC]
            utc_sign = -1 if json_utc[0] == '-' else 1
            utc_stamp = pd.Timedelta(json_utc[1:9]) // timedelta(seconds=1)
            system_utc_offset = local_time.utcoffset() // timedelta(seconds=1)
            delta = system_utc_offset - utc_sign * utc_stamp

            result_stamp = dt_stamp + delta
            result = datetime.fromtimestamp(result_stamp).strftime('%Y-%m-%d %H:%M')
            system("cls")
            print(result)
            print("Сейчас раз в %dмин. выводится дата и время в формате yyyy-mm-dd hh:mm. Для завершения нажмите CTRL+C" % TIMEOUT)

        except KeyboardInterrupt:
            print("Вы нажали CTRL+C")
            break


main()




