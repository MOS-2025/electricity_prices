import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


def calculate_statistics(df):
    """
    Calculate cheapest, most expensive, and average electricity price.
    """
    if df["Price perKwhour"].isnull().all():
        raise ValueError("No valid price data available.")

    cheapest = df.loc[df["Price perKwhour"].idxmin()]
    most_expensive = df.loc[df["Price perKwhour"].idxmax()]
    average = df["Price perKwhour"].mean()

    return cheapest, most_expensive, average


def find_price(df, selected_datetime):
    """
    Find electricity price for a specific date and time.
    """
    return df[df["Date and Time"] == selected_datetime]


def get_user_input():
    """
    Get user input and remove extra spaces.
    """
    return input(
        "Enter (dd/mm/yyyy hh:mm),Example 01/01/2026 17:00: "
    ).strip()


def main():
    # Displays welcome message
    print("Welcome to the electricity prices checker!")
    # Define the scope and credentials for Google Sheets API
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
    # Check if sheet is empty or missing data
    if not data or len(data) < 2:
        print("Error: The Google Sheet is empty or missing data.")
        exit()
    # Define required column names and check if they exist in the data
    required_columns = ["Week No", "Date and Time", "Price perKwhour"]

    for column in required_columns:
        if column not in data[0]:
            print(f"Error: Missing required column: {column}")
            exit()

    df = pd.DataFrame(data[1:], columns=data[0])
    # Convert price column to numeric, coercing errors to NaN
    df["Price perKwhour"] = pd.to_numeric(
        df["Price perKwhour"], errors="coerce"
    )
    # Convert date column to datetime, coercing errors to NaT
    df["Date and Time"] = pd.to_datetime(
        df["Date and Time"], dayfirst=True, errors="coerce"
    )

    # User input
    user_input = get_user_input()

    try:
        # Convert user input into datetime object
        selected_datetime = pd.to_datetime(user_input, format="%d/%m/%Y %H:%M")

        # Find matching row
        result = find_price(df, selected_datetime)

        if not result.empty:
            print("\nElectricity price for selected date and time:")
            print(result[["Week No", "Date and Time", "Price perKwhour"]])
        else:
            print("\nNo data found for that date and time.")

    except ValueError:
        # Handle incorrect date format
        print("\nInvalid format. Enter the date and time as dd/mm/yyyy hh:mm")

    try:
        cheapest, most_expensive, average = calculate_statistics(df)

    except ValueError as e:
        # Handle missing or invalid price data
        print(e)
        exit()
    # Ask user what result they want to see
    choice = input(
        "\nPress Enter for all, or type c (cheapest), "
        "m (most expensive), a (average): "
    ).strip().lower()
    # Shows all results if user presses Enter or types "all" (case-insensitive)
    if choice in ("", "all"):
        print("\nCheapest electricity price:")
        cheapest_cols = ["Week No", "Date and Time", "Price perKwhour"]
        print(cheapest[cheapest_cols].to_string())

        print("\nMost expensive electricity price:")
        most_expensive_cols = ["Week No", "Date and Time", "Price perKwhour"]
        print(most_expensive[most_expensive_cols].to_string())

        print("\nAverage electricity price:")
        print(average)
    # Shows only the cheapest price if user selects "c"
    elif choice == "c":
        print("\nCheapest electricity price:")
        cheapest_cols = ["Week No", "Date and Time", "Price perKwhour"]
        print(cheapest[cheapest_cols].to_string())
    # Shows only the most expensive price if user selects "m"
    elif choice == "m":
        print("\nMost expensive electricity price:")
        most_expensive_cols = ["Week No", "Date and Time", "Price perKwhour"]
        print(most_expensive[most_expensive_cols].to_string())
    # Shows only average price if user selects "a"
    elif choice == "a":
        print("\nAverage electricity price:")
        print(average)

    # Send selected result back to Google Sheet
    cheapest_datetime = (
        cheapest["Date and Time"].strftime("%d/%m/%Y %H:%M")
        if pd.notnull(cheapest["Date and Time"]) else ""
    )
    most_expensive_datetime = (
        most_expensive["Date and Time"].strftime("%d/%m/%Y %H:%M")
        if pd.notnull(most_expensive["Date and Time"]) else ""
    )
    # Prepare results for Google Sheet
    results = [["Metric", "Week No", "Date and Time", "Price perKwhour"]]

    if choice in ("", "all"):
        results.append([
            "Cheapest",
            cheapest["Week No"],
            cheapest_datetime,
            cheapest["Price perKwhour"]
        ])
        results.append([
            "Most Expensive",
            most_expensive["Week No"],
            most_expensive_datetime,
            most_expensive["Price perKwhour"]
        ])
        results.append(["Average", "", "", average])

    elif choice == "c":
        results.append([
            "Cheapest",
            cheapest["Week No"],
            cheapest_datetime,
            cheapest["Price perKwhour"]
        ])

    elif choice == "m":
        results.append([
            "Most Expensive",
            most_expensive["Week No"],
            most_expensive_datetime,
            most_expensive["Price perKwhour"]
        ])

    elif choice == "a":
        results.append(["Average", "", "", average])

    else:
        # if invalid input, stop before writing to Google Sheet
        print("\nInvalid choice. Nothing written to Google Sheet.")
        return

    # Clear old results first so stale rows don't remain
    Sheet1.batch_clear(["F2:I5"])

    end_row = len(results) + 1
    # Write results to Google Sheet
    Sheet1.update(range_name=f"F2:I{end_row}", values=results)

    print("\nSelected result has been written back to the Google Sheet.")


if __name__ == "__main__":
    main()
