import sqlite3
from datetime import datetime

DB_NAME = "assignments.db"

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- VALIDATE DATE ----------------
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ---------------- PRIORITY LOGIC ----------------
def get_priority(deadline):
    d = datetime.strptime(deadline, "%Y-%m-%d")
    diff = (d - datetime.now()).days

    if diff < 0:
        return "Overdue ⚠️"
    elif diff <= 1:
        return "High 🔴"
    elif diff <= 3:
        return "Medium 🟠"
    else:
        return "Low 🟢"


# ---------------- ADD ASSIGNMENT ----------------
def add_assignment():
    title = input("Enter assignment title: ").strip()

    if not title:
        print("❌ Title cannot be empty!\n")
        return

    deadline = input("Enter deadline (YYYY-MM-DD): ")

    if not validate_date(deadline):
        print("❌ Invalid date format! Use YYYY-MM-DD\n")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO assignments (title, deadline, status) VALUES (?, ?, ?)",
        (title, deadline, "Pending")
    )

    conn.commit()
    conn.close()

    print("✅ Assignment added successfully!\n")


# ---------------- VIEW ASSIGNMENTS ----------------
def view_assignments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assignments")
    tasks = cursor.fetchall()

    conn.close()

    if not tasks:
        print("📭 No assignments found.\n")
        return

    print("\n📋 Your Assignments:\n")

    for task in tasks:
        id, title, deadline, status = task
        priority = get_priority(deadline)

        print(f"ID: {id}")
        print(f"Title: {title}")
        print(f"Deadline: {deadline}")
        print(f"Priority: {priority}")
        print(f"Status: {status}")
        print("-" * 30)


# ---------------- MARK COMPLETE ----------------
def mark_complete():
    id = input("Enter assignment ID to mark as complete: ")

    if not id.isdigit():
        print("❌ Invalid ID!\n")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assignments WHERE id=?", (id,))
    task = cursor.fetchone()

    if not task:
        print("❌ Assignment not found!\n")
    else:
        cursor.execute("UPDATE assignments SET status='Done' WHERE id=?", (id,))
        conn.commit()
        print("✅ Marked as completed!\n")

    conn.close()


# ---------------- DELETE ASSIGNMENT ----------------
def delete_assignment():
    id = input("Enter assignment ID to delete: ")

    if not id.isdigit():
        print("❌ Invalid ID!\n")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assignments WHERE id=?", (id,))
    task = cursor.fetchone()

    if not task:
        print("❌ Assignment not found!\n")
    else:
        cursor.execute("DELETE FROM assignments WHERE id=?", (id,))
        conn.commit()
        print("🗑️ Assignment deleted!\n")

    conn.close()


# ---------------- MAIN MENU ----------------
def main():
    init_db()

    while True:
        print("\n🎯 Smart Assignment Manager")
        print("1. Add Assignment")
        print("2. View Assignments")
        print("3. Mark as Complete")
        print("4. Delete Assignment")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_assignment()
        elif choice == "2":
            view_assignments()
        elif choice == "3":
            mark_complete()
        elif choice == "4":
            delete_assignment()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.\n")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()