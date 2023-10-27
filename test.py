import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os

text = '3/9/2021  7:24:00 AM'
date = dt.datetime.strptime(text,'%m/%d/%Y %H:%M:%S %p')
print(date.date())