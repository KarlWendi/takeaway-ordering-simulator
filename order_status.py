STATUS_TRANSITIONS = {
    "queued": "preparing",
    "preparing": "ready",
    "ready": "collected",
}

# A function that validates the status change.
def validate_status_change(current_status, new_status):
    expected_status = STATUS_TRANSITIONS.get(current_status)

    if new_status != expected_status:
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )