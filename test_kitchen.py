import copy
import unittest

from kitchen import simulate_queue
from queue_demo import DEMO_ORDERS


class KitchenTests(unittest.TestCase):
    def test_two_station_schedule(self):
        result = simulate_queue(DEMO_ORDERS, 2)
        self.assertEqual(result["schedule"], [
            {"order_id": 1, "station": 1, "prep_minutes": 6,
             "waiting_minutes": 0, "ready_after_minutes": 6},
            {"order_id": 2, "station": 2, "prep_minutes": 2,
             "waiting_minutes": 0, "ready_after_minutes": 2},
            {"order_id": 3, "station": 2, "prep_minutes": 4,
             "waiting_minutes": 2, "ready_after_minutes": 6},
        ])
        self.assertEqual(result["average_waiting_minutes"], 0.67)
        self.assertEqual(result["maximum_waiting_minutes"], 2)
        self.assertEqual(result["all_ready_after_minutes"], 6)

    def test_one_station_runs_sequentially(self):
        result = simulate_queue(DEMO_ORDERS, 1)
        self.assertEqual([row["waiting_minutes"] for row in result["schedule"]], [0, 6, 8])
        self.assertEqual(result["average_waiting_minutes"], 4.67)
        self.assertEqual(result["all_ready_after_minutes"], 12)

    def test_three_stations_remove_wait_for_three_orders(self):
        result = simulate_queue(DEMO_ORDERS, 3)
        self.assertEqual(result["average_waiting_minutes"], 0)
        self.assertEqual(result["all_ready_after_minutes"], 6)

    def test_empty_queue_returns_zero_summary(self):
        result = simulate_queue([], 2)
        self.assertEqual(result["schedule"], [])
        self.assertEqual(result["order_count"], 0)
        self.assertEqual(result["average_waiting_minutes"], 0)
        self.assertEqual(result["all_ready_after_minutes"], 0)

    def test_id_order_and_completed_orders(self):
        orders = copy.deepcopy(list(reversed(DEMO_ORDERS)))
        orders[1]["status"] = "completed"
        result = simulate_queue(orders, 1)
        self.assertEqual([row["order_id"] for row in result["schedule"]], [1, 3])
        self.assertEqual(result["all_ready_after_minutes"], 10)

    def test_invalid_station_counts_are_rejected(self):
        for stations in [0, -1, 11, True, 1.5, "2"]:
            with self.subTest(stations=stations):
                with self.assertRaises(ValueError):
                    simulate_queue(DEMO_ORDERS, stations)

    def test_unknown_product_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "No preparation time"):
            simulate_queue([{"id": 1, "item_id": 999, "quantity": 1, "status": "queued"}])

    def test_simulation_does_not_mutate_orders(self):
        orders = copy.deepcopy(DEMO_ORDERS)
        before = copy.deepcopy(orders)
        simulate_queue(orders, 2)
        self.assertEqual(orders, before)


if __name__ == "__main__":
    unittest.main()
