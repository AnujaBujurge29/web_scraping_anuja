import sqlite3
import sys

DB_PATH = "db/mlb_history.db"


def print_table(rows, columns):
    if not rows:
        print("No results found.")
        return
    print("-" * 80)
    print(" | ".join(columns))
    print("-" * 80)
    for row in rows:
        print(" | ".join(str(item) for item in row))
    print("-" * 80)


def main():
    print("MLB History Query CLI")
    print("Type `exit` to quit.\n")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        try:
            query = input("SQL> ").strip()
            if query.lower() in ["exit", "quit"]:
                break
            if not query:
                continue
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            print_table(rows, columns)
        except Exception as e:
            print(f"Error: {e}")

    conn.close()
    print("Exiting!")


if __name__ == "__main__":
    main()
