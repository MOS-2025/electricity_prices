print("Welcome to the electricity prices checker, Data for January to April 2026 can be viewed to determine the cheapest and most expensive electricity prices !")
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import os
import json


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Electricity_Prices')

Sheet1 = SHEET.worksheet('Sheet1')

data = Sheet1.get_all_values()


df = pd.DataFrame(data[1:], columns=data[0])



df["Price perKwhour"] = pd.to_numeric(df["Price perKwhour"], errors="coerce")
df["Date and Time"] = pd.to_datetime(df["Date and Time"], dayfirst=True, errors="coerce")

#print(df)

cheapest = df.loc[df["Price perKwhour"].idxmin()]
print(cheapest)

expensive = df.loc[df["Price perKwhour"].idxmax()]
print(expensive)

#print(df["Price perKwhour"].max())

#df["Date and Time"] = pd.to_datetime(df["Date and Time"])

#jan1 = df[df["Date and Time"].dt.date == pd.to_datetime("2026-01-01").date()]

#print(jan1)

