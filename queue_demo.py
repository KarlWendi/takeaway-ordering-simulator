"""Compare station capacity using fictional orders; no database changes."""

from kitchen import simulate_queue


DEMO_ORDERS = [
    {"id": 1, "item_id": 1, "quantity": 2, "status": "queued"},
    {"id": 2, "item_id": 2, "quantity": 1, "status": "queued"},
    {"id": 3, "item_id": 3, "quantity": 1, "status": "queued"},
]


def main():
    print("Fictional orders: 2 burgers (6 min), fries (2 min), wrap (4 min)")
    print("All orders start waiting at simulation minute 0.")
    for stations in [1, 2, 3]:
        result = simulate_queue(DEMO_ORDERS, stations)
        print(f"\n{stations} station(s): average wait "
              f"{result['average_waiting_minutes']} min; "
              f"all ready after {result['all_ready_after_minutes']} min")
        for entry in result["schedule"]:
            print(f"Order #{entry['order_id']} -> station {entry['station']}: "
                  f"starts at {entry['waiting_minutes']} min, "
                  f"ready at {entry['ready_after_minutes']} min")


if __name__ == "__main__":
    main()
