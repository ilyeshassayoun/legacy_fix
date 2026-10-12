# What I checked, and what the agent got wrong

## What the agent got wrong

The agent fixed the three most obvious crashes — division by zero in `fleet_summary`, division
by zero in `wear_percent`, and the unhandled `FileNotFoundError` in `load_settings` — but it
did not touch `analyze.py` at all. It left the file as a stub with the placeholder comment
"your analysis here" and a bare `print(df.head())`. I had to notice that `verify.py` was
checking both the length of `analyze.py` and the absence of that placeholder string before
the agent would have flagged it as incomplete.

## What I checked before I accepted its work

I ran `python verify.py` after every change to confirm the check count actually moved. For the
wear bug specifically, I traced through the arithmetic by hand: VOS-4471 has odometer 14900
and last_service_km 0, so km_since_service is 14900, and 14900 / 15000 * 100 = 99.3%. Before
the fix, `car_wear` returned 0 for any car whose `last_service_km` was falsy (including 0),
so that car was silently excluded from the average and never flagged — even though it was
almost due. I checked that the patched `car_wear` now returns 99.3% for that car and that
`fleet_summary` reports `due = 1` for the sample fleet.

## What the data actually said

I compared the group means of every numeric column between cars that broke down and those that
did not. Total odometer and age looked like the obvious culprits — they are the first things
a mechanic would check — but both had a group-mean ratio of almost exactly 1.00, meaning
broken-down cars and healthy cars had virtually identical mileage and age. The actual
predictors were `km_since_service` (ratio 1.61: cars that broke down had gone 61% further
since their last service on average) and `avg_daily_km` (ratio 1.22: they were also being
driven harder day-to-day). The risk score in `analyze.py` weights those two columns at 0.65
and 0.35 respectively and scales the result to 0–100.
