# pyGarminConnect
Library for communicating with and retrieving activty data from Garmin Connect

Usage
-----
```python
from GarminConnect import GarminConnect

gc = GarminConnect('<garmin_account_username>', '<garmin_account_password>')
gc.getActivities(start=0, count=10)
```
