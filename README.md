# ⚡ Electricity Prices Checker

A Python-based command-line application that connects to a Google Sheet to analyze electricity prices.
It allows users to query electricity prices for a specific date and time, and calculates key insights such as the cheapest, most expensive, and average prices.
The data is collected every 30 minutes starting on 01/01/2026 00:30 until 01/07/2026 23:30.


<img width="462" height="612" alt="image" src="https://github.com/user-attachments/assets/0155c057-7c48-439a-bcc6-5672b4688b61" />


---

## 📌 Features

* Connects to Google Sheets using a **service account**
* Reads and processes data using **pandas**
* User input to check electricity price at a specific date/time
* Automatically calculates:

  * Cheapest price
  * Most expensive price
  * Average price
* Selected statistics displayed on linked Google sheet

---

## 🔗 Live Project

* **Live Site:** https://mos-2025.github.io/
* **Repository:** https://github.com/MOS-2025/

* <img width="1402" height="837" alt="image" src="https://github.com/user-attachments/assets/447f965c-da04-467e-8b9c-e56c048f2138" />


---


## 🔗 Flow Chart


<img width="632" height="902" alt="image" src="https://github.com/user-attachments/assets/47fcd6f8-e7bc-41b6-8b50-4f46e92712b8" />



---

## 🔑 Google Sheets Setup

1. Go to Google Cloud Console
2. Create a new project
3. Enable:

   * Google Sheets API
   * Google Drive API
4. Create a **Service Account**
5. Download the credentials file and rename it to:

```bash
creds.json
```

6. Share your Google Sheet with the service account email

---

## 📊 Expected Google Sheet Format

**Sheet name:** `Sheet1`

**Columns required:**

* Week No
* Date and Time (format: `dd/mm/yyyy hh:mm`)
* Price per KWh

---

## ▶️ How to Run

```bash
python run.py
```

Enter a date and time when prompted:

```
Enter (dd/mm/yyyy hh:mm), Example: 01/01/2026 17:00
```

---

## ⚙️ What the Script Does

* Loads electricity price data from Google Sheets
* Converts:

  * Prices → numeric values
  * Dates → datetime format
* Searches for a matching date/time
* Displays:

  * Selected price (if found)
  * Cheapest price
  * Most expensive price
  * Average price
* Writes results back to the Google Sheet

---

## 📤 Output

The script prints results in the terminal and updates the Google Sheet:

* **Range:** `F2:I5`

**Includes:**

* Cheapest price
* Most expensive price
* Average price

---

## ⚠️ Error Handling

* Invalid date format → prompts user to re-enter
* Missing or invalid data handled using pandas
* Non-numeric values safely converted

<img width="1693" height="598" alt="image" src="https://github.com/user-attachments/assets/c005cf30-23ed-4aa1-90d4-6b347a7c8ce4" />


---

## 🚀 Future Enhancements

* Add charts using miniplot for data visualization
* Build a web interface
* Filter by date ranges or weeks
* Integrate live electricity price APIs
* Upload CSV file with data for entire calendar year (currently 1 week's data recorded)
* Compare cheapest prices against peak wind generation

---

## 🛠️ Technologies Used

* Python
* pandas
* Google Sheets API

---

## 🧪 Testing & Validation

* Passed through PEP8 Linter with no issues
* <img width="1886" height="843" alt="image" src="https://github.com/user-attachments/assets/6571c741-c2b2-44c5-aeab-30fa7dc6a959" />
* Tested locally in terminal
* Verified Google Sheets integration

---

## 📂 Credits

* MDN Web Docs
* Traversy Media
* W3Schools
