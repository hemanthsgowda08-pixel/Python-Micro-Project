import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# 5. LIST & 7. DICTIONARY (List of Dictionaries for Movies)
MOVIES = [
    {"title": "Interstellar", "genre": "Sci-Fi", "poster": "#0D2B55", "stars": 5},
    {"title": "Mission Mangal", "genre": "Biography", "poster": "#B5451B", "stars": 4},
    {"title": "Rocketry", "genre": "Biography", "poster": "#7A3B00", "stars": 4},
    {"title": "Inception", "genre": "Sci-Fi", "poster": "#1A1A6E", "stars": 5},
    {"title": "Gravity", "genre": "Sci-Fi", "poster": "#006060", "stars": 4},
    {"title": "The Martian", "genre": "Sci-Fi", "poster": "#8B1A1A", "stars": 4}
]

# 5. LIST
SHOWTIMES = ["10:00 AM", "01:00 PM", "04:00 PM", "07:00 PM"]

# 8. NESTED DICTIONARY (Dictionaries inside a Dictionary)
SEAT_CATEGORIES = {
    "RECLINER": {"price": 600, "rows": ["A"], "cols": 8, "color": "#FFD700"},
    "PREMIUM":  {"price": 350, "rows": ["B", "C"], "cols": 10, "color": "#4FC3F7"},
    "STANDARD": {"price": 200, "rows": ["D", "E"], "cols": 10, "color": "#81C784"}
}

# 7. DICTIONARY (To store application state without using Classes)
state = {
    "movie": None, 
    "date": None, 
    "time": None,
    "seats": [], 
    "booked": {}, 
    "history": []
}

# 1. SETUP WINDOW
root = tk.Tk()
root.title("BSI CiniPass - Simplified")
root.geometry("900x650")
root.configure(bg="#0A0A0F")

sidebar = tk.Frame(root, bg="#12121A", width=200)
sidebar.pack(side="left", fill="y")

content_area = tk.Frame(root, bg="#0A0A0F")
content_area.pack(side="left", fill="both", expand=True)

def clear_view():
    # 3. LOOPING
    for widget in content_area.winfo_children():
        widget.destroy()

def nav_click(page):
    clear_view()
    # 2. DECISION MAKING
    if page == "home": build_home()
    elif page == "booking": build_booking(1)
    elif page == "history": build_history()

def build_home():
    tk.Label(content_area, text="NOW SHOWING", font=("Arial", 20, "bold"), bg="#0A0A0F", fg="#F5C518").pack(pady=20)
    grid = tk.Frame(content_area, bg="#0A0A0F")
    grid.pack()

    # 3. LOOPING & 4. PATTERN (Creating a 3-column Grid Pattern)
    row_idx, col_idx = 0, 0
    for movie in MOVIES:
        card = tk.Frame(grid, bg="#12121A", bd=2, relief="ridge", padx=15, pady=15)
        card.grid(row=row_idx, column=col_idx, padx=10, pady=10)

        tk.Frame(card, bg=movie["poster"], height=5, width=150).pack(fill="x")
        tk.Label(card, text=movie["title"], font=("Arial", 14, "bold"), bg="#12121A", fg="white").pack(pady=5)
        tk.Label(card, text=movie["genre"], bg="#12121A", fg="gray").pack()
        
        # 4. PATTERN (String Multiplication for stars) & 1. OPERATORS
        tk.Label(card, text="★" * movie["stars"], bg="#12121A", fg="gold").pack()

        def book_action(m=movie):
            state["movie"] = m
            nav_click("booking")

        tk.Button(card, text="BOOK TICKETS", bg="#E50914", fg="white", command=book_action).pack(pady=10)

        # 1. OPERATORS & 2. DECISION MAKING
        col_idx += 1
        if col_idx > 2:
            col_idx = 0
            row_idx += 1

def build_booking(step):
    clear_view()
    tk.Label(content_area, text=f"Step {step} of 4", font=("Arial", 16), bg="#0A0A0F", fg="white").pack(pady=10)

    # 2. DECISION MAKING (Handling multi-step process)
    if step == 1:
        tk.Label(content_area, text="Select Movie", font=("Arial", 14), bg="#0A0A0F", fg="gold").pack()
        for m in MOVIES:
            color = "#E50914" if state["movie"] == m else "#1A1A28"
            tk.Button(content_area, text=m["title"], bg=color, fg="white", width=40,
                      command=lambda m_=m: [state.update({"movie": m_}), build_booking(1)]).pack(pady=5)

        tk.Button(content_area, text="NEXT", bg="white", command=lambda: build_booking(2) if state["movie"] else messagebox.showerror("Error", "Select a movie!")).pack(pady=20)

    elif step == 2:
        dates = [(datetime.today() + timedelta(days=i)).strftime("%d %b") for i in range(5)]
        if not state["date"]: state["date"] = dates[0]

        tk.Label(content_area, text="Select Date", font=("Arial", 14), bg="#0A0A0F", fg="gold").pack(pady=10)
        df = tk.Frame(content_area, bg="#0A0A0F")
        df.pack()
        for d in dates:
            color = "#E50914" if state["date"] == d else "#1A1A28"
            tk.Button(df, text=d, bg=color, fg="white", width=10, command=lambda d_=d: [state.update({"date": d_}), build_booking(2)]).pack(side="left", padx=5)

        tk.Label(content_area, text="Select Time", font=("Arial", 14), bg="#0A0A0F", fg="gold").pack(pady=20)
        tf = tk.Frame(content_area, bg="#0A0A0F")
        tf.pack()
        for t in SHOWTIMES:
            color = "#E50914" if state["time"] == t else "#1A1A28"
            tk.Button(tf, text=t, bg=color, fg="white", width=10, command=lambda t_=t: [state.update({"time": t_}), build_booking(2)]).pack(side="left", padx=5)

        nav = tk.Frame(content_area, bg="#0A0A0F")
        nav.pack(pady=30)
        tk.Button(nav, text="BACK", command=lambda: build_booking(1)).pack(side="left", padx=20)
        tk.Button(nav, text="NEXT", command=lambda: build_booking(3) if state["time"] else messagebox.showerror("Error", "Select time!")).pack(side="left", padx=20)

    elif step == 3:
        show_key = f"{state['movie']['title']}_{state['date']}_{state['time']}"
        if show_key not in state["booked"]:
            state["booked"][show_key] = []

        tk.Label(content_area, text="SCREEN", bg="gray", fg="white", width=50).pack(pady=20)

        # 3. LOOPING over 8. NESTED DICTIONARY
        for cat, info in SEAT_CATEGORIES.items():
            tk.Label(content_area, text=f"{cat} - ₹{info['price']}", bg="#0A0A0F", fg=info["color"]).pack()
            for r in info["rows"]:
                row_frame = tk.Frame(content_area, bg="#0A0A0F")
                row_frame.pack(pady=2)
                tk.Label(row_frame, text=r, bg="#0A0A0F", fg="white", width=2).pack(side="left")

                for c in range(1, info["cols"] + 1):
                    seat_id = f"{r}{c}"
                    # 2. DECISION MAKING
                    if seat_id in state["booked"][show_key]: color, stat = "gray", "disabled"
                    elif seat_id in state["seats"]: color, stat = "#E50914", "normal"
                    else: color, stat = "#1A1A28", "normal"

                    def toggle_seat(s=seat_id):
                        if s in state["seats"]: state["seats"].remove(s)
                        else: state["seats"].append(s)
                        build_booking(3)

                    tk.Button(row_frame, text=str(c), bg=color, fg="white", width=3, state=stat, command=toggle_seat).pack(side="left", padx=2)

        tk.Label(content_area, text=f"Selected: {', '.join(state['seats'])}", bg="#0A0A0F", fg="white").pack(pady=10)

        nav = tk.Frame(content_area, bg="#0A0A0F")
        nav.pack(pady=10)
        tk.Button(nav, text="BACK", command=lambda: build_booking(2)).pack(side="left", padx=20)
        tk.Button(nav, text="NEXT", command=lambda: build_booking(4) if state["seats"] else messagebox.showerror("Error", "Select seats!")).pack(side="left", padx=20)

    elif step == 4:
        # 1. OPERATORS (Math for total calculation)
        total = 0
        for s in state["seats"]:
            for cat, info in SEAT_CATEGORIES.items():
                if s[0] in info["rows"]:
                    total += info["price"]
        tax = int(total * 0.18)
        grand = total + tax

        tk.Label(content_area, text="Bill Summary", font=("Arial", 16, "bold"), bg="#0A0A0F", fg="gold").pack(pady=10)
        tk.Label(content_area, text=f"Movie: {state['movie']['title']}\nDate & Time: {state['date']} | {state['time']}\nSeats: {', '.join(state['seats'])}", bg="#0A0A0F", fg="white").pack(pady=10)
        tk.Label(content_area, text=f"Subtotal: ₹{total}\nTax (18%): ₹{tax}", bg="#0A0A0F", fg="white").pack()
        tk.Label(content_area, text=f"Grand Total: ₹{grand}", font=("Arial", 14, "bold"), bg="#0A0A0F", fg="#00C853").pack(pady=10)

        def confirm():
            # 7. DICTIONARY (Creating a history record)
            booking = {"movie": state["movie"]["title"], "date": state["date"], "time": state["time"], "seats": list(state["seats"]), "total": grand}
            state["history"].append(booking)
            
            show_key = f"{state['movie']['title']}_{state['date']}_{state['time']}"
            state["booked"][show_key].extend(state["seats"])

            state["seats"].clear()
            state["movie"] = None 

            messagebox.showinfo("Success", "Tickets Booked Successfully!")
            nav_click("history")

        nav = tk.Frame(content_area, bg="#0A0A0F")
        nav.pack(pady=20)
        tk.Button(nav, text="BACK", command=lambda: build_booking(3)).pack(side="left", padx=20)
        tk.Button(nav, text="PAY & CONFIRM", bg="#00C853", fg="black", font=("Arial", 12, "bold"), command=confirm).pack(side="left", padx=20)

def build_history():
    tk.Label(content_area, text="Booking History", font=("Arial", 18, "bold"), bg="#0A0A0F", fg="white").pack(pady=20)
    if not state["history"]:
        tk.Label(content_area, text="No bookings yet.", bg="#0A0A0F", fg="gray").pack()
    
    for b in state["history"]:
        card = tk.Frame(content_area, bg="#12121A", bd=1, relief="solid", padx=20, pady=10)
        card.pack(fill="x", padx=50, pady=5)
        tk.Label(card, text=f"Movie: {b['movie']} | Date: {b['date']} | Time: {b['time']}", bg="#12121A", fg="white").pack(anchor="w")
        tk.Label(card, text=f"Seats: {', '.join(b['seats'])} | Paid: ₹{b['total']}", bg="#12121A", fg="gold").pack(anchor="w")

# 6. TUPLE (Used for configuring the navigation menu buttons)
menu_items = (
    ("Home", "home"), 
    ("Book Ticket", "booking"), 
    ("My Bookings", "history")
)

tk.Label(sidebar, text="🚀 BSI CiniPass", font=("Arial", 16, "bold"), bg="#12121A", fg="#E50914").pack(pady=20)

for text, key in menu_items:
    tk.Button(sidebar, text=text, bg="#1A1A28", fg="white", font=("Arial", 12), width=15,
              command=lambda k=key: nav_click(k)).pack(pady=10)

# Start application
nav_click("home")
root.mainloop()