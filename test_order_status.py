import tempfile
import unittest
import sqlite3
from pathlib import Path

from database import (
    get_menu,
    get_orders,
    initialise_database,
    place_order,
    update_order_status,
)


class StatusDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "test.db"

        initialise_database(self.path)
        order = place_order(1, 2, self.path)
        self.order_id = order["order_id"]

    def test_status_is_saved_without_changing_stock(self):
        stock_before = get_menu(self.path)

        update_order_status(self.order_id, "preparing", self.path)

        self.assertEqual(get_orders(self.path)[0]["status"], "preparing")
        self.assertEqual(get_menu(self.path), stock_before)

    def test_invalid_change_leaves_order_unchanged(self):
        with self.assertRaises(ValueError):
            update_order_status(self.order_id, "collected", self.path)

        self.assertEqual(get_orders(self.path)[0]["status"], "queued")
        self.assertEqual(get_menu(self.path)[0]["stock"], 18)

    def test_missing_order_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Order not found"):
            update_order_status(999, "preparing", self.path)

        self.assertEqual(len(get_orders(self.path)), 1)

    def test_preparing_order_has_an_estimated_ready_time(self):
        update_order_status(self.order_id, "preparing", self.path)

        order = get_orders(self.path)[0]
        self.assertIsNotNone(order["preparation_started_at"])
        self.assertIsNotNone(order["estimated_ready_at"])
        self.assertGreater(order["estimated_ready_at"], order["preparation_started_at"])

    def test_elapsed_preparation_becomes_ready_automatically(self):
        update_order_status(self.order_id, "preparing", self.path)
        connection = sqlite3.connect(self.path)
        with connection:
            connection.execute(
                "UPDATE orders SET estimated_ready_at = '2000-01-01 00:00:00' "
                "WHERE id = ?",
                (self.order_id,),
            )
        connection.close()

        self.assertEqual(get_orders(self.path)[0]["status"], "ready")


if __name__ == "__main__":
    unittest.main()
