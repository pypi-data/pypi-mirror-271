# EPİAŞ Transparency Platform 2.0 Python Library

This library enables users to get data from EPİAŞ's Transparency Platform by using simple python functions.

Please note that this is not an official release, and the accuracy or reliability of the data retrieved through this library cannot be guaranteed. Users are advised to exercise caution and verify the data independently before making any decisions based on it. 

The author(s) of this library shall not be held responsible for any inaccuracies or damages resulting from the use of the data.

Data input formats should be such as: "YYYY-MM-DD". An example would be : "2024-05-29"

All the functions returns a pandas dataframe.

## Currently few selected datasets are available, which are:


epias_mcp(start_date,end_date): Function that returns the MCP for a given interval

epias_kgup(start_date,end_date): Function that returns the DPP's (KGUP) based on resources for a given interval

epias_plant_kgup(start_date,end_date,pl_id,o_id): Function that returns the DPP's (KGUP) based on resources for a given interval (org_id: Organization ID, pl_id: Plant ID) Organization IDs can be obtained via epias_org function Plant IDs can be obtained via  epias_uevcb function

epias_org(start_date,end_date): Function that returns the organizations for a given interval

epias_uevcb(start_date,end_date,o_id): Function that returns the UEVCB data for a given interval (o_id: Organization ID)

epias_demand(start_date,end_date): Function that returns the real time electricity consumption for a given interval

epias_idmp(start_date,end_date): Function that returns the intraday markey prices for a given interval

epias_idma(start_date,end_date): Function that returns the trade amount at intraday market for a given interval 

epias_smp(start_date,end_date): Function that returns the System Marginal Price for a given interval 

epias_yal(start_date,end_date): Function that returns the amount of load orders (YAL) for a given interval 

epias_yat(start_date,end_date): Function that returns the amount of deload orders (YAT) for a given interval

epias_sfc(start_date,end_date): Function that returns the SFC prices for a given interval

epias_pfc(start_date,end_date): Function that returns the PFC prices for a given interval



#### Example 1
```python
from seffaflik2 import epias_mcp

day_ahead_prices = epias_mcp("2024-01-15","2024-03-16")

print(day_ahead_prices)
```

#### Example 2
```python
import seffaflik2 as sf

day_ahead_prices = sf.epias_mcp("2024-01-15","2024-03-16")

print(day_ahead_prices)
```


