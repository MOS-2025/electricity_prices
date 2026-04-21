import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt


print("Welcome to the electricity prices checker!")


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

# User input
user_input = input("Enter (dd/mm/yyyy hh:mm),Example 01/01/2026 17:00: ")

try:
    selected_datetime = pd.to_datetime(user_input, format="%d/%m/%Y %H:%M")

    # Find matching row
    result = df[df["Date and Time"] == selected_datetime]

    if not result.empty:
        print("\nElectricity price for selected date and time:")
        print(result[["Week No", "Date and Time", "Price perKwhour"]])
    else:
        print("\nNo data found for that date and time.")

except ValueError:
    print("\nInvalid format. Enter the date and time as dd/mm/yyyy hh:mm")


# Cheapest and most expensive and average price
cheapest = df.loc[df["Price perKwhour"].idxmin()]
most_expensive = df.loc[df["Price perKwhour"].idxmax()]
average = df["Price perKwhour"].mean()

print("\nCheapest electricity price:")
print(cheapest[["Week No", "Date and Time", "Price perKwhour"]].to_string())

print("\nMost expensive electricity price:")
print(most_expensive[["Week No", "Date and Time", "Price perKwhour"]].to_string())

print("\nAverage electricity price:")
print(average)


# Send result back to Google Sheet
results = [
    ["Metric", "Week No", "Date and Time", "Price perKwhour"],
    [
        "Cheapest",
        cheapest["Week No"],
        cheapest["Date and Time"].strftime("%d/%m/%Y %H:%M") if pd.notnull(cheapest["Date and Time"]) else "",
        cheapest["Price perKwhour"]
    ],
    [
        "Most Expensive",
        most_expensive["Week No"],
        most_expensive["Date and Time"].strftime("%d/%m/%Y %H:%M") if pd.notnull(most_expensive["Date and Time"]) else "",
        most_expensive["Price perKwhour"]
    ],
    ["Average", "", "", average]
]
Sheet1.update(range_name="F2:I5", values=results)

print("\nResults have been written back to the Google Sheet.")
