import matplotlib.pyplot as plt
import numpy as np

rides      = []
passengers = []
ratings    = []
receipts   = []


# -----------------------------------------------
#  RIDE FUNCTIONS
# -----------------------------------------------

def add_ride():
    print("")
    print("------------------------------")
    print("         ADD NEW RIDE         ")
    print("------------------------------")
    from_loc = input("From (pickup location) : ")
    to_loc   = input("To   (drop location)   : ")
    driver   = input("Driver name            : ")
    contact  = input("Driver contact number  : ")
    vehicle  = input("Vehicle model & number : ")
    date     = input("Date (DD/MM/YYYY)      : ")
    time     = input("Time (HH:MM)           : ")

    while True:
        try:
            seats = int(input("Available seats        : "))
            if seats > 0:
                break
            print("Seats must be at least 1.")
        except ValueError:
            print("Please enter a whole number.")

    while True:
        try:
            fare = float(input("Fare per seat (0=Free) : "))
            if fare >= 0:
                break
            print("Fare cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")

    rides.append({
        "id"       : len(rides) + 1,
        "from_loc" : from_loc,
        "to_loc"   : to_loc,
        "driver"   : driver,
        "contact"  : contact,
        "vehicle"  : vehicle,
        "date"     : date,
        "time"     : time,
        "seats"    : seats,
        "fare"     : fare,
        "booked"   : 0,
        "status"   : "Scheduled"
    })
    print("Ride added: " + from_loc + " --> " + to_loc)


def view_rides():
    print("")
    print("------------------------------")
    print("           ALL RIDES          ")
    print("------------------------------")
    if len(rides) == 0:
        print("No rides found.")
        return
    for r in rides:
        if r["fare"] == 0:
            fare_str = "Free"
        else:
            fare_str = "Rs." + str(r["fare"]) + "/seat"
        seats_left = r["seats"] - r["booked"]
        print("ID       : " + str(r["id"]))
        print("Route    : " + r["from_loc"] + " --> " + r["to_loc"])
        print("Driver   : " + r["driver"] + " | Contact: " + r["contact"])
        print("Vehicle  : " + r["vehicle"])
        print("Schedule : " + r["date"] + " at " + r["time"])
        print("Seats    : " + str(seats_left) + " left out of " + str(r["seats"]))
        print("Fare     : " + fare_str)
        print("Status   : " + r["status"])
        print("------------------------------")


def update_ride_status():
    print("")
    print("------------------------------")
    print("      UPDATE RIDE STATUS      ")
    print("------------------------------")
    if len(rides) == 0:
        print("No rides found.")
        return
    view_rides()
    try:
        rid = int(input("Enter Ride ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    ride = None
    for r in rides:
        if r["id"] == rid:
            ride = r
            break
    if ride == None:
        print("Ride not found.")
        return

    print("Current Status: " + ride["status"])
    print("1. Scheduled")
    print("2. Active")
    print("3. Completed")
    print("4. Cancelled")
    choice = input("Choose new status: ")

    if choice == "1":
        ride["status"] = "Scheduled"
    elif choice == "2":
        ride["status"] = "Active"
    elif choice == "3":
        ride["status"] = "Completed"
    elif choice == "4":
        ride["status"] = "Cancelled"
    else:
        print("Invalid choice.")
        return
    print("Status updated to: " + ride["status"])


def delete_ride():
    print("")
    print("------------------------------")
    print("         DELETE RIDE          ")
    print("------------------------------")
    if len(rides) == 0:
        print("No rides found.")
        return
    view_rides()
    try:
        rid = int(input("Enter Ride ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    for i in range(len(rides)):
        if rides[i]["id"] == rid:
            confirm = input("Are you sure you want to delete this ride? (yes/no): ")
            if confirm.lower() == "yes":
                rides.pop(i)
                print("Ride deleted.")
            else:
                print("Deletion cancelled.")
            return
    print("Ride not found.")


# -----------------------------------------------
#  PASSENGER FUNCTIONS
# -----------------------------------------------

def book_ride():
    print("")
    print("------------------------------")
    print("          BOOK A RIDE         ")
    print("------------------------------")
    if len(rides) == 0:
        print("No rides available.")
        return

    name   = input("Your full name    : ")
    email  = input("Email address     : ")
    phone  = input("Phone number      : ")
    pickup = input("Your pickup point : ")

    print("")
    print("-- Available Rides --")
    found_any = False
    for r in rides:
        if r["status"] == "Scheduled" or r["status"] == "Active":
            if r["booked"] < r["seats"]:
                if r["fare"] == 0:
                    fare_str = "Free"
                else:
                    fare_str = "Rs." + str(r["fare"]) + "/seat"
                seats_left = r["seats"] - r["booked"]
                print(str(r["id"]) + ". " + r["from_loc"] + " --> " + r["to_loc"] +
                      " | " + r["date"] + " " + r["time"] +
                      " | Seats left: " + str(seats_left) +
                      " | " + fare_str)
                found_any = True

    if found_any == False:
        print("No seats available right now.")
        return

    try:
        rid = int(input("Enter Ride ID to book: "))
    except ValueError:
        print("Invalid ID.")
        return

    selected = None
    for r in rides:
        if r["id"] == rid:
            selected = r
            break

    if selected == None:
        print("Ride not found.")
        return
    if selected["booked"] >= selected["seats"]:
        print("Sorry, this ride is full!")
        return
    if selected["status"] != "Scheduled" and selected["status"] != "Active":
        print("Booking is closed for this ride.")
        return

    for p in passengers:
        if p["email"] == email and p["ride_id"] == rid:
            print("You have already booked this ride!")
            return

    passengers.append({
        "id"      : len(passengers) + 1,
        "name"    : name,
        "email"   : email,
        "phone"   : phone,
        "pickup"  : pickup,
        "ride_id" : rid,
        "route"   : selected["from_loc"] + " --> " + selected["to_loc"],
        "payment" : "Pending",
        "status"  : "Confirmed"
    })
    selected["booked"] += 1
    print("")
    print("Booking Confirmed!")
    print(name + " booked: " + selected["from_loc"] + " --> " + selected["to_loc"])
    if selected["fare"] > 0:
        print("Fare due: Rs." + str(selected["fare"]) + " | Payment: Pending")


def view_passengers():
    print("")
    print("------------------------------")
    print("        ALL PASSENGERS        ")
    print("------------------------------")
    if len(passengers) == 0:
        print("No passengers found.")
        return
    for p in passengers:
        print("ID      : " + str(p["id"]))
        print("Name    : " + p["name"])
        print("Phone   : " + p["phone"])
        print("Route   : " + p["route"])
        print("Pickup  : " + p["pickup"])
        print("Payment : " + p["payment"])
        print("Status  : " + p["status"])
        print("------------------------------")


def search_passenger():
    print("")
    print("------------------------------")
    print("       SEARCH PASSENGER       ")
    print("------------------------------")
    if len(passengers) == 0:
        print("No passengers found.")
        return

    print("Search by:")
    print("1. Name")
    print("2. Phone")
    print("3. Email")
    print("4. Route")
    print("5. Pickup Point")
    choice = input("Choose: ")

    results = []

    if choice == "1":
        keyword = input("Enter name: ").lower()
        for p in passengers:
            if keyword in p["name"].lower():
                results.append(p)
    elif choice == "2":
        keyword = input("Enter phone: ").lower()
        for p in passengers:
            if keyword in p["phone"].lower():
                results.append(p)
    elif choice == "3":
        keyword = input("Enter email: ").lower()
        for p in passengers:
            if keyword in p["email"].lower():
                results.append(p)
    elif choice == "4":
        keyword = input("Enter route: ").lower()
        for p in passengers:
            if keyword in p["route"].lower():
                results.append(p)
    elif choice == "5":
        keyword = input("Enter pickup point: ").lower()
        for p in passengers:
            if keyword in p["pickup"].lower():
                results.append(p)
    else:
        print("Invalid choice.")
        return

    if len(results) == 0:
        print("No passengers found.")
        return

    print(str(len(results)) + " result(s) found:")
    print("------------------------------")
    for p in results:
        print("ID      : " + str(p["id"]))
        print("Name    : " + p["name"])
        print("Email   : " + p["email"])
        print("Phone   : " + p["phone"])
        print("Route   : " + p["route"])
        print("Pickup  : " + p["pickup"])
        print("Payment : " + p["payment"])
        print("Status  : " + p["status"])
        print("------------------------------")


def update_payment():
    print("")
    print("------------------------------")
    print("     UPDATE PAYMENT STATUS    ")
    print("------------------------------")
    if len(passengers) == 0:
        print("No passengers found.")
        return
    view_passengers()
    try:
        pid = int(input("Enter Passenger ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    passenger = None
    for p in passengers:
        if p["id"] == pid:
            passenger = p
            break
    if passenger == None:
        print("Passenger not found.")
        return

    print("Current payment: " + passenger["payment"])
    print("1. Paid")
    print("2. Pending")
    print("3. Waived")
    choice = input("Choose: ")

    if choice == "1":
        passenger["payment"] = "Paid"
    elif choice == "2":
        passenger["payment"] = "Pending"
    elif choice == "3":
        passenger["payment"] = "Waived"
    else:
        print("Invalid choice.")
        return
    print("Payment updated to: " + passenger["payment"])


def cancel_booking():
    print("")
    print("------------------------------")
    print("        CANCEL BOOKING        ")
    print("------------------------------")
    if len(passengers) == 0:
        print("No passengers found.")
        return
    view_passengers()
    try:
        pid = int(input("Enter Passenger ID to cancel: "))
    except ValueError:
        print("Invalid ID.")
        return

    passenger = None
    for p in passengers:
        if p["id"] == pid:
            passenger = p
            break
    if passenger == None:
        print("Passenger not found.")
        return
    if passenger["status"] == "Cancelled":
        print("This booking is already cancelled.")
        return

    confirm = input("Cancel booking for " + passenger["name"] + "? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancellation aborted.")
        return

    passenger["status"] = "Cancelled"
    for r in rides:
        if r["id"] == passenger["ride_id"]:
            if r["booked"] > 0:
                r["booked"] -= 1
            break
    print("Booking cancelled for: " + passenger["name"])


# -----------------------------------------------
#  RATING FUNCTIONS
# -----------------------------------------------

def add_ratings():
    print("")
    print("------------------------------")
    print("      ADD / UPDATE RATINGS    ")
    print("------------------------------")
    if len(passengers) == 0:
        print("No passengers found.")
        return
    view_rides()
    try:
        rid = int(input("Enter Ride ID to rate: "))
    except ValueError:
        print("Invalid ID.")
        return

    ride = None
    for r in rides:
        if r["id"] == rid:
            ride = r
            break
    if ride == None:
        print("Ride not found.")
        return
    if ride["status"] != "Completed":
        print("Ratings can only be added for Completed rides.")
        return

    confirmed_list = []
    for p in passengers:
        if p["ride_id"] == rid and p["status"] == "Confirmed":
            confirmed_list.append(p)

    if len(confirmed_list) == 0:
        print("No confirmed passengers for this ride.")
        return

    for p in confirmed_list:
        print("")
        print("Passenger: " + p["name"] + " (" + p["phone"] + ")")
        while True:
            try:
                score = int(input("Rating (1-5 stars): "))
                if 1 <= score <= 5:
                    break
                print("Enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input.")

        feedback = input("Feedback (press Enter to skip): ")

        if score == 5:
            category = "Excellent"
        elif score == 4:
            category = "Good"
        elif score == 3:
            category = "Average"
        elif score == 2:
            category = "Poor"
        else:
            category = "Very Poor"

        existing = None
        for rt in ratings:
            if rt["passenger_id"] == p["id"] and rt["ride_id"] == rid:
                existing = rt
                break

        if existing != None:
            existing["rating"]   = score
            existing["feedback"] = feedback
            existing["category"] = category
            print("Updated: " + str(score) + " stars (" + category + ")")
        else:
            ratings.append({
                "id"             : len(ratings) + 1,
                "passenger_id"   : p["id"],
                "passenger_name" : p["name"],
                "phone"          : p["phone"],
                "ride_id"        : rid,
                "route"          : ride["from_loc"] + " --> " + ride["to_loc"],
                "driver"         : ride["driver"],
                "rating"         : score,
                "feedback"       : feedback,
                "category"       : category
            })
            print("Saved: " + str(score) + " stars (" + category + ")")


def view_ratings():
    print("")
    print("------------------------------")
    print("          ALL RATINGS         ")
    print("------------------------------")
    if len(ratings) == 0:
        print("No ratings recorded yet.")
        return
    for rt in ratings:
        print("Passenger : " + rt["passenger_name"])
        print("Route     : " + rt["route"])
        print("Driver    : " + rt["driver"])
        print("Rating    : " + str(rt["rating"]) + " stars (" + rt["category"] + ")")
        if rt["feedback"] == "":
            print("Feedback  : None")
        else:
            print("Feedback  : " + rt["feedback"])
        print("------------------------------")


def rating_charts():
    print("")
    print("------------------------------")
    print("         RATING CHARTS        ")
    print("------------------------------")
    if len(ratings) == 0:
        print("No ratings found.")
        return

    view_rides()
    try:
        rid = int(input("Ride ID (0 = all rides): "))
    except ValueError:
        print("Invalid ID.")
        return

    if rid == 0:
        subset = ratings
        title  = "All Rides"
    else:
        ride = None
        for r in rides:
            if r["id"] == rid:
                ride = r
                break
        if ride == None:
            print("Ride not found.")
            return
        subset = []
        for rt in ratings:
            if rt["ride_id"] == rid:
                subset.append(rt)
        title = ride["from_loc"] + " --> " + ride["to_loc"]

    if len(subset) == 0:
        print("No ratings found for this selection.")
        return

    print("Choose chart type:")
    print("1. Pie Chart  (category wise)")
    print("2. Bar Chart  (star wise)")
    chart_choice = input("Choose: ")

    cat_list  = []
    star_list = []
    for rt in subset:
        cat_list.append(rt["category"])
        star_list.append(rt["rating"])

    if chart_choice == "1":
        unique, counts = np.unique(np.array(cat_list), return_counts=True)
        colors = ["#4caf50", "#8bc34a", "#ffc107", "#ff5722", "#f44336"]
        plt.figure(figsize=(6, 5))
        plt.pie(counts, labels=unique, autopct="%1.1f%%", startangle=140,
                colors=colors[:len(unique)])
        plt.title("Rating Distribution - " + title)
        plt.tight_layout()
        plt.show()

    elif chart_choice == "2":
        star_counts = []
        for s in [1, 2, 3, 4, 5]:
            star_counts.append(star_list.count(s))
        bar_colors = ["#f44336", "#ff5722", "#ffc107", "#8bc34a", "#4caf50"]
        plt.figure(figsize=(6, 5))
        plt.bar(["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
                star_counts, color=bar_colors)
        plt.title("Star-wise Ratings - " + title)
        plt.xlabel("Stars")
        plt.ylabel("Number of Ratings")
        plt.tight_layout()
        plt.show()

    else:
        print("Invalid choice.")


# -----------------------------------------------
#  RECEIPT FUNCTIONS
# -----------------------------------------------

def generate_receipts():
    print("")
    print("------------------------------")
    print("       GENERATE RECEIPTS      ")
    print("------------------------------")
    if len(ratings) == 0:
        print("Please add ratings before generating receipts.")
        return
    view_rides()
    try:
        rid = int(input("Enter Ride ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    ride = None
    for r in rides:
        if r["id"] == rid:
            ride = r
            break
    if ride == None:
        print("Ride not found.")
        return

    count = 0
    for rt in ratings:
        if rt["ride_id"] != rid:
            continue

        already_issued = False
        for rc in receipts:
            if rc["passenger_id"] == rt["passenger_id"] and rc["ride_id"] == rid:
                already_issued = True
                break
        if already_issued:
            continue

        passenger = None
        for p in passengers:
            if p["id"] == rt["passenger_id"]:
                passenger = p
                break
        if passenger == None:
            continue

        rid_str = str(rid)
        pid_str = str(rt["passenger_id"])
        while len(rid_str) < 3:
            rid_str = "0" + rid_str
        while len(pid_str) < 4:
            pid_str = "0" + pid_str
        receipt_id = "RCPT-" + rid_str + "-" + pid_str

        receipts.append({
            "receipt_id"     : receipt_id,
            "passenger_id"   : rt["passenger_id"],
            "passenger_name" : rt["passenger_name"],
            "phone"          : passenger["phone"],
            "pickup"         : passenger["pickup"],
            "ride_id"        : rid,
            "from_loc"       : ride["from_loc"],
            "to_loc"         : ride["to_loc"],
            "driver"         : ride["driver"],
            "contact"        : ride["contact"],
            "vehicle"        : ride["vehicle"],
            "date"           : ride["date"],
            "time"           : ride["time"],
            "fare"           : ride["fare"],
            "payment"        : passenger["payment"],
            "rating"         : rt["rating"],
            "category"       : rt["category"]
        })
        count += 1

    print(str(count) + " receipt(s) generated for: " +
          ride["from_loc"] + " --> " + ride["to_loc"])


def view_receipts():
    print("")
    print("------------------------------")
    print("         ALL RECEIPTS         ")
    print("------------------------------")
    if len(receipts) == 0:
        print("No receipts issued yet.")
        return
    for rc in receipts:
        if rc["fare"] == 0:
            fare_str = "Free"
        else:
            fare_str = "Rs." + str(rc["fare"])
        print("Receipt ID : " + rc["receipt_id"])
        print("Passenger  : " + rc["passenger_name"])
        print("Route      : " + rc["from_loc"] + " --> " + rc["to_loc"])
        print("Date       : " + rc["date"] + " at " + rc["time"])
        print("Fare       : " + fare_str + " | Payment: " + rc["payment"])
        print("Rating     : " + str(rc["rating"]) + " stars (" + rc["category"] + ")")
        print("------------------------------")


def print_receipt():
    print("")
    print("------------------------------")
    print("         PRINT RECEIPT        ")
    print("------------------------------")
    receipt_id = input("Enter Receipt ID: ")

    rc = None
    for r in receipts:
        if r["receipt_id"] == receipt_id:
            rc = r
            break
    if rc == None:
        print("Receipt not found.")
        return

    if rc["fare"] == 0:
        fare_str = "Free"
    else:
        fare_str = "Rs." + str(rc["fare"])

    stars = ""
    for i in range(rc["rating"]):
        stars = stars + "*"

    print("")
    print("******************************************")
    print("*                                        *")
    print("*        CARPOOL BOOKING RECEIPT         *")
    print("*                                        *")
    print("******************************************")
    print("*  PASSENGER                             *")
    print("*  Name    : " + rc["passenger_name"])
    print("*  Phone   : " + rc["phone"])
    print("******************************************")
    print("*  JOURNEY                               *")
    print("*  From    : " + rc["from_loc"])
    print("*  To      : " + rc["to_loc"])
    print("*  Date    : " + rc["date"])
    print("*  Time    : " + rc["time"])
    print("*  Pickup  : " + rc["pickup"])
    print("******************************************")
    print("*  DRIVER                                *")
    print("*  Name    : " + rc["driver"])
    print("*  Contact : " + rc["contact"])
    print("*  Vehicle : " + rc["vehicle"])
    print("******************************************")
    print("*  Fare    : " + fare_str)
    print("*  Payment : " + rc["payment"])
    print("*  Rating  : " + stars + " (" + rc["category"] + ")")
    print("*  Rcpt ID : " + rc["receipt_id"])
    print("*                                        *")
    print("******************************************")


def verify_receipt():
    print("")
    print("------------------------------")
    print("        VERIFY RECEIPT        ")
    print("------------------------------")
    receipt_id = input("Enter Receipt ID: ")

    rc = None
    for r in receipts:
        if r["receipt_id"] == receipt_id:
            rc = r
            break

    if rc != None:
        print("")
        print("VALID RECEIPT!")
        print("Issued to : " + rc["passenger_name"])
        print("Route     : " + rc["from_loc"] + " --> " + rc["to_loc"])
        print("Date      : " + rc["date"])
        print("Payment   : " + rc["payment"])
    else:
        print("")
        print("INVALID - Receipt not found.")


# -----------------------------------------------
#  SUMMARY
# -----------------------------------------------

def show_summary():
    print("")
    print("------------------------------")
    print("        SYSTEM SUMMARY        ")
    print("------------------------------")
    print("Total Rides      : " + str(len(rides)))
    print("Total Passengers : " + str(len(passengers)))
    print("Total Ratings    : " + str(len(ratings)))
    print("Total Receipts   : " + str(len(receipts)))

    if len(rides) > 0:
        print("")
        print("-- Ride Status --")
        scheduled = 0
        active    = 0
        completed = 0
        cancelled = 0
        for r in rides:
            if r["status"] == "Scheduled":
                scheduled += 1
            elif r["status"] == "Active":
                active += 1
            elif r["status"] == "Completed":
                completed += 1
            elif r["status"] == "Cancelled":
                cancelled += 1
        print("Scheduled : " + str(scheduled))
        print("Active    : " + str(active))
        print("Completed : " + str(completed))
        print("Cancelled : " + str(cancelled))

    if len(passengers) > 0:
        print("")
        print("-- Passenger Status --")
        confirmed = 0
        cancelled = 0
        paid      = 0
        pending   = 0
        for p in passengers:
            if p["status"] == "Confirmed":
                confirmed += 1
            elif p["status"] == "Cancelled":
                cancelled += 1
            if p["payment"] == "Paid":
                paid += 1
            elif p["payment"] == "Pending":
                pending += 1
        print("Confirmed : " + str(confirmed))
        print("Cancelled : " + str(cancelled))
        print("Paid      : " + str(paid))
        print("Pending   : " + str(pending))

    if len(ratings) > 0:
        print("")
        print("-- Rating Stats --")
        scores = np.array([rt["rating"] for rt in ratings])
        print("Average : " + str(round(float(np.mean(scores)), 2)) + " stars")
        print("Highest : " + str(int(np.max(scores))) + " stars")
        print("Lowest  : " + str(int(np.min(scores))) + " stars")
        print("")
        print("-- Category Breakdown --")
        excellent = 0
        good      = 0
        average   = 0
        poor      = 0
        very_poor = 0
        for rt in ratings:
            if rt["category"] == "Excellent":
                excellent += 1
            elif rt["category"] == "Good":
                good += 1
            elif rt["category"] == "Average":
                average += 1
            elif rt["category"] == "Poor":
                poor += 1
            elif rt["category"] == "Very Poor":
                very_poor += 1
        print("Excellent : " + str(excellent))
        print("Good      : " + str(good))
        print("Average   : " + str(average))
        print("Poor      : " + str(poor))
        print("Very Poor : " + str(very_poor))

    print("------------------------------")


# -----------------------------------------------
#  FILE SAVE / LOAD
# -----------------------------------------------

def save_to_file():
    with open("rides.txt", "w") as f:
        for r in rides:
            line = (str(r["id"]) + "|" + r["from_loc"] + "|" + r["to_loc"] + "|" +
                    r["driver"] + "|" + r["contact"] + "|" + r["vehicle"] + "|" +
                    r["date"] + "|" + r["time"] + "|" + str(r["seats"]) + "|" +
                    str(r["fare"]) + "|" + str(r["booked"]) + "|" + r["status"])
            f.write(line + "\n")

    with open("passengers.txt", "w") as f:
        for p in passengers:
            line = (str(p["id"]) + "|" + p["name"] + "|" + p["email"] + "|" +
                    p["phone"] + "|" + p["pickup"] + "|" + str(p["ride_id"]) + "|" +
                    p["route"] + "|" + p["payment"] + "|" + p["status"])
            f.write(line + "\n")

    with open("ratings.txt", "w") as f:
        for rt in ratings:
            line = (str(rt["id"]) + "|" + str(rt["passenger_id"]) + "|" +
                    rt["passenger_name"] + "|" + rt["phone"] + "|" +
                    str(rt["ride_id"]) + "|" + rt["route"] + "|" + rt["driver"] + "|" +
                    str(rt["rating"]) + "|" + rt["feedback"] + "|" + rt["category"])
            f.write(line + "\n")

    with open("receipts.txt", "w") as f:
        for rc in receipts:
            line = (rc["receipt_id"] + "|" + str(rc["passenger_id"]) + "|" +
                    rc["passenger_name"] + "|" + rc["phone"] + "|" + rc["pickup"] + "|" +
                    str(rc["ride_id"]) + "|" + rc["from_loc"] + "|" + rc["to_loc"] + "|" +
                    rc["driver"] + "|" + rc["contact"] + "|" + rc["vehicle"] + "|" +
                    rc["date"] + "|" + rc["time"] + "|" + str(rc["fare"]) + "|" +
                    rc["payment"] + "|" + str(rc["rating"]) + "|" + rc["category"])
            f.write(line + "\n")

    print("Data saved successfully.")


def load_from_file():
    rides.clear()
    passengers.clear()
    ratings.clear()
    receipts.clear()

    try:
        with open("rides.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 12:
                    rides.append({
                        "id"       : int(p[0]),
                        "from_loc" : p[1],
                        "to_loc"   : p[2],
                        "driver"   : p[3],
                        "contact"  : p[4],
                        "vehicle"  : p[5],
                        "date"     : p[6],
                        "time"     : p[7],
                        "seats"    : int(p[8]),
                        "fare"     : float(p[9]),
                        "booked"   : int(p[10]),
                        "status"   : p[11]
                    })
        print("Rides loaded     : " + str(len(rides)))
    except FileNotFoundError:
        print("Starting fresh (no saved rides found).")

    try:
        with open("passengers.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 9:
                    passengers.append({
                        "id"      : int(p[0]),
                        "name"    : p[1],
                        "email"   : p[2],
                        "phone"   : p[3],
                        "pickup"  : p[4],
                        "ride_id" : int(p[5]),
                        "route"   : p[6],
                        "payment" : p[7],
                        "status"  : p[8]
                    })
        print("Passengers loaded: " + str(len(passengers)))
    except FileNotFoundError:
        pass

    try:
        with open("ratings.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 10:
                    ratings.append({
                        "id"             : int(p[0]),
                        "passenger_id"   : int(p[1]),
                        "passenger_name" : p[2],
                        "phone"          : p[3],
                        "ride_id"        : int(p[4]),
                        "route"          : p[5],
                        "driver"         : p[6],
                        "rating"         : int(p[7]),
                        "feedback"       : p[8],
                        "category"       : p[9]
                    })
        print("Ratings loaded   : " + str(len(ratings)))
    except FileNotFoundError:
        pass

    try:
        with open("receipts.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 17:
                    receipts.append({
                        "receipt_id"     : p[0],
                        "passenger_id"   : int(p[1]),
                        "passenger_name" : p[2],
                        "phone"          : p[3],
                        "pickup"         : p[4],
                        "ride_id"        : int(p[5]),
                        "from_loc"       : p[6],
                        "to_loc"         : p[7],
                        "driver"         : p[8],
                        "contact"        : p[9],
                        "vehicle"        : p[10],
                        "date"           : p[11],
                        "time"           : p[12],
                        "fare"           : float(p[13]),
                        "payment"        : p[14],
                        "rating"         : int(p[15]),
                        "category"       : p[16]
                    })
        print("Receipts loaded  : " + str(len(receipts)))
    except FileNotFoundError:
        pass


# -----------------------------------------------
#  MENUS
# -----------------------------------------------

def admin_menu():
    while True:
        print("")
        print("==============================")
        print("         ADMIN PANEL          ")
        print("==============================")
        print("  -- RIDES --")
        print("  1.  Add Ride")
        print("  2.  View All Rides")
        print("  3.  Update Ride Status")
        print("  4.  Delete Ride")
        print("------------------------------")
        print("  -- PASSENGERS --")
        print("  5.  View All Passengers")
        print("  6.  Search Passenger")
        print("  7.  Update Payment Status")
        print("  8.  Cancel a Booking")
        print("------------------------------")
        print("  -- RATINGS --")
        print("  9.  Add / Update Ratings")
        print("  10. View All Ratings")
        print("  11. Rating Charts")
        print("------------------------------")
        print("  -- RECEIPTS --")
        print("  12. Generate Receipts")
        print("  13. View All Receipts")
        print("------------------------------")
        print("  14. Summary")
        print("  15. Save Data")
        print("  0.  Back to Main Menu")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            add_ride()
        elif choice == "2":
            view_rides()
        elif choice == "3":
            update_ride_status()
        elif choice == "4":
            delete_ride()
        elif choice == "5":
            view_passengers()
        elif choice == "6":
            search_passenger()
        elif choice == "7":
            update_payment()
        elif choice == "8":
            cancel_booking()
        elif choice == "9":
            add_ratings()
        elif choice == "10":
            view_ratings()
        elif choice == "11":
            rating_charts()
        elif choice == "12":
            generate_receipts()
        elif choice == "13":
            view_receipts()
        elif choice == "14":
            show_summary()
        elif choice == "15":
            save_to_file()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def passenger_menu():
    while True:
        print("")
        print("==============================")
        print("       PASSENGER PORTAL       ")
        print("==============================")
        print("  1. View Available Rides")
        print("  2. Book a Ride")
        print("  3. Print My Receipt")
        print("  4. Verify a Receipt")
        print("  0. Back to Main Menu")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            view_rides()
        elif choice == "2":
            book_ride()
        elif choice == "3":
            print_receipt()
        elif choice == "4":
            verify_receipt()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    print("Loading saved data...")
    load_from_file()

    while True:
        print("")
        print("==============================")
        print("  CARPOOL MANAGEMENT SYSTEM   ")
        print("==============================")
        print("  1. Admin Panel")
        print("  2. Passenger Portal")
        print("  3. Exit")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            passenger_menu()
        elif choice == "3":
            save_to_file()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()