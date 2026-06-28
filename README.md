# Carpool Management System

A command-line application written in Python to manage college/office carpooling from start to finish, covering ride scheduling, passenger booking, driver ratings, and receipt generation.

Built as a first year summer project to practise core Python concepts.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)
- [Planned Improvements](#planned-improvements)

---

## About

Organizing carpools by hand means juggling group chats, spreadsheets, and manually keeping track of who paid, who showed up, and how the ride went. This project replaces all of that with a simple menu-driven system that keeps everything in one place.

There are two separate portals: one for the admin who manages rides, and one for passengers who book seats and collect their receipts. Data is saved to local text files so nothing is lost between sessions.

---

## Features

### Admin Panel

**Ride Management**
- Add rides with pickup/drop location, driver name, contact, vehicle, date, time, available seats, and fare
- View all rides with current seat counts and status
- Update status: Scheduled, Active, Completed, or Cancelled
- Delete a ride from the system

**Passenger Management**
- View all booked passengers with payment and booking status
- Search passengers by name, phone, email, route, or pickup point (partial and case-insensitive matching)
- Update payment status: Paid, Pending, or Waived
- Cancel a booking, which frees up the seat for someone else

**Ratings**
- Add or update a 1-5 star rating for every confirmed passenger on a Completed ride
- Rating is auto-categorized: Excellent, Good, Average, Poor, or Very Poor
- Optional written feedback per passenger
- Two chart options using Matplotlib: pie chart (category-wise) and bar chart (star-wise)

**Receipts**
- Generate receipts for all rated passengers on a ride
- Each receipt gets a unique ID (e.g. RCPT-001-0001)
- View all issued receipts in one list

**Reports**
- Summary dashboard with totals, ride status breakdown, passenger payment stats, and rating averages including highest, lowest, and category breakdown
- Save all data to text files

### Passenger Portal

- Browse available rides with seat availability and fare
- Book a ride (checks for duplicate booking and seat limits)
- Print a formatted receipt to the terminal
- Verify any receipt by its ID

---

## Tech Stack

- **Python 3**
- **Matplotlib** for rating distribution pie and bar charts
- **NumPy** for rating statistics
- Built-in file I/O for data persistence

No database or external setup required.

---

## Getting Started

### Requirements

Python 3 must be installed. Install the two dependencies with:

```bash
pip install matplotlib numpy
```

### Running the App

```bash
python carpool_management.py
```

The program loads any existing data automatically on startup and saves on exit.

---

## How to Use

When you run the program, you choose between the Admin Panel and Passenger Portal.

```
==============================
  CARPOOL MANAGEMENT SYSTEM   
==============================
  1. Admin Panel
  2. Passenger Portal
  3. Exit
==============================
```

**Admin flow:**
Add a ride, let passengers book seats, mark the ride Completed once it's done, add ratings for each passenger, and generate receipts. Use the search feature to quickly look up any passenger by name, phone, email, route, or pickup point.

**Passenger flow:**
View available rides, book one, and once the admin has generated receipts, use the receipt ID to print or verify it.

---

## Project Structure

```
carpool-management-system/
|
|-- carpool_management.py   # All application logic
|-- rides.txt                # Auto-generated on save
|-- passengers.txt           # Auto-generated on save
|-- ratings.txt              # Auto-generated on save
|-- receipts.txt              # Auto-generated on save
|-- README.md
```

## Sample Output

**Receipt printed in terminal:**

```
******************************************
*                                        *
*        CARPOOL BOOKING RECEIPT         *
*                                        *
******************************************
*  PASSENGER                             *
*  Name    : Jane Doe
*  Phone   : 9876543210
******************************************
*  JOURNEY                               *
*  From    : Delhi
*  To      : Gurugram
*  Date    : 10/07/2026
*  Time    : 08:00
*  Pickup  : Hauz Khas Metro
******************************************
*  DRIVER                                *
*  Name    : Rajesh Kumar
*  Contact : 9876543210
*  Vehicle : Honda City DL01AB1234
******************************************
*  Fare    : Free
*  Payment : Paid
*  Rating  : ***** (Excellent)
*  Rcpt ID : RCPT-001-0001
*                                        *
******************************************
```

---

## Planned Improvements

- GUI using Tkinter
- SQLite database instead of text files
- SMS/email notification on booking and receipt issue
- PDF export for receipts
- Password-protected admin login
- Live ride tracking / ETA support

---

## Author

**JEET MAKHIJA**

---

## License

This project is open source under the [MIT License](LICENSE).
