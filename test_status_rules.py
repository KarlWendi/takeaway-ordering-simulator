import unittest

from order_status import validate_status_change


class OrderStatusRuleTests(unittest.TestCase):
    def test_valid_changes(self):
        validate_status_change("queued", "preparing")
        validate_status_change("preparing", "ready")
        validate_status_change("ready", "collected")

    def test_skipping_a_status_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_status_change("queued", "ready")

    def test_backwards_change_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_status_change("ready", "preparing")

    def test_collected_order_cannot_restart(self):
        with self.assertRaises(ValueError):
            validate_status_change("collected", "queued")


if __name__ == "__main__":
    unittest.main()
