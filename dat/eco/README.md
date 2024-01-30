# Eco Counter Data
Data should be loaded using the dedicated [Eco Counter Data Loader](../../src/LoadEcoCounterData.py)

The csv files in this folder contain the following columns and can be read using `pandas` or any other tool.
| # |  Column
|---|  ------
| 0 |  timestamp
| 1 |  iso_timestamp
| 2 |  zählstand
| 3 |  channel_name
| 4 |  channel_id
| 5 |  counter_site
| 6 |  counter_site_id

Channels denote the direction the counter is passed.
