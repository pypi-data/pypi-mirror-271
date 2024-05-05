from pathlib import Path
from datetime import datetime, time, timedelta, timezone, tzinfo
import csv


def shift_data(input_file: Path, output_file: Path, /,
               closing_time: time,
               tzinfo: tzinfo,
               include_weekends: bool):
    count = 0

    with input_file.open() as in_stream, output_file.open('w') as out:
        reader = csv.reader(in_stream)
        next(reader)  # skip header
        out.write('<TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>\n')
        ct = closing_time

        for row in reader:
            # if count >= 10: break  # for testing
            r1 = row[1]
            r2 = row[2]
            dt = datetime.fromisoformat(f'{r1[0:4]}-{r1[4:6]}-{r1[6:8]}T{r2[0:2]}:{r2[2:4]}')
            dt = dt.replace(tzinfo=timezone.utc).astimezone(tzinfo)

            if not include_weekends:
                wd = dt.isoweekday()
                t = dt.time()

                if (wd == 5 and ct <= t) or (wd == 6) or (wd == 7 and t < ct):
                    continue  # skip

            out.write(row[0])
            out.write(',')
            dt = dt - timedelta(hours=ct.hour, minutes=ct.minute) + timedelta(days=1)
            out.write(dt.strftime('%Y%m%d'))
            out.write(',')
            out.write(dt.strftime('%H%M'))
            out.write(',')
            out.write(row[3])
            out.write(',')
            out.write(row[4])
            out.write(',')
            out.write(row[5])
            out.write(',')
            out.write(row[6])
            out.write(',')
            out.write(row[7])
            out.write('\n')
            count += 1
