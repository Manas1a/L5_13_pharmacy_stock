"""Track pharmacy inventory, patient allergies, and prescriptions."""

import json
import sqlite3
from datetime import datetime


conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create a small in-memory database of patients."""
    with conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS patients "
            "(id TEXT, name TEXT, allergy TEXT)"
        )
        conn.executemany(
            "INSERT INTO patients VALUES (?, ?, ?)",
            [
                ("P1", "Kavya", "penicillin"),
                ("P2", "Arjun", "none"),
                ("P3", "Meena", "ibuprofen"),
            ],
        )


def find_patient(name):
    """Look up a patient without interpolating input into SQL."""
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add a nonnegative quantity of medicine to the inventory."""
    if batch_log is None:
        batch_log = []
    if not isinstance(units, int) or units < 0:
        print(f"Invalid stock quantity for {drug}: {units}")
        return len(batch_log)
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid expiry date for {drug}: {expiry}")
        return len(batch_log)
    if expiry_date < datetime.now().date():
        print(f"Warning: {drug} is already expired")
    current = stock.get(drug, {}).get("units", 0)
    stock[drug] = {"units": current + units, "expiry": expiry}
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense available, unexpired medicine to an eligible patient."""
    patients = find_patient(patient_name)
    if not patients:
        print(f"Patient not found: {patient_name}")
        return False
    if not isinstance(units, int) or units <= 0:
        print("Dispensing quantity must be a positive integer")
        return False
    patient_id, allergy = patients[0]
    if allergy.lower() == drug.lower():
        print(f"Allergy warning for {patient_name}")
        return False
    item = stock.get(drug)
    if item is None:
        print(f"Medicine not in stock: {drug}")
        return False
    if item["units"] < units:
        print(f"Insufficient stock for {drug}")
        return False
    try:
        expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid expiry date for {drug}")
        return False
    if expiry < datetime.now().date():
        print(f"Cannot dispense expired medicine: {drug}")
        return False
    item["units"] -= units
    prescriptions.append(
        {
            "patient": patient_id,
            "drug": drug,
            "units": units,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )
    return True


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    today = datetime.now().date()
    soon = []
    for drug, item in stock.items():
        try:
            expiry = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
        except ValueError:
            print(f"Invalid expiry date for {drug}")
            continue
        if (expiry - today).days < days:
            soon.append(drug)
    return soon


def export_prescriptions(file="prescriptions.json"):
    """Write the prescriptions list to a UTF-8 JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=4)


def load_stock(file="stock.json"):
    """Load stock from JSON if the file exists and is valid."""
    try:
        with open(file, "r", encoding="utf-8") as stock_file:
            loaded = json.load(stock_file)
    except FileNotFoundError:
        print("Stock file not found. Starting with empty stock.")
        return
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Unable to load stock: {error}")
        return
    if not isinstance(loaded, dict):
        print("Invalid stock format: expected a dictionary")
        return
    for drug, item in loaded.items():
        if (
            isinstance(drug, str)
            and isinstance(item, dict)
            and isinstance(item.get("units"), int)
            and item["units"] >= 0
            and isinstance(item.get("expiry"), str)
        ):
            try:
                datetime.strptime(item["expiry"], "%Y-%m-%d")
            except ValueError:
                print(f"Skipping invalid expiry date for {drug}")
                continue
            stock[drug] = {
                "units": item["units"],
                "expiry": item["expiry"],
            }
        else:
            print(f"Skipping invalid stock entry: {drug}")


def print_stock():
    """Display current medicine quantities and expiry dates."""
    print("Pharmacy Stock")
    for drug, item in stock.items():
        print(drug, "->", item["units"], "units, expires", item["expiry"])


def main():
    """Run the sample pharmacy workflow and interactive patient lookup."""
    setup_database()
    load_stock()
    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", -15, "2026-11-30")
    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))
    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
