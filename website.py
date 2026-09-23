"""Stage 7: python -m streamlit run website.py (start the API first)."""
import os
import streamlit as st
from menu import format_price
from web_client import APIError, request_api

st.set_page_config(page_title="Takeaway Kitchen", page_icon="🍔", layout="wide")
st.title("🍔 Takeaway Kitchen")
st.caption("A fictional ordering simulation · no payments or real deliveries")
if os.environ.get("TAKEAWAY_TEMPORARY_DEMO") == "1":
    st.info("Public demo: stock and orders are shared by visitors and reset when the service restarts. The free service may take a little time to wake up.")

notice = st.session_state.pop("order_notice", None)
if notice:
    st.success(notice)

st.button("Refresh menu and orders")
try:
    menu = request_api("GET", "/menu")
except APIError as error:
    st.error(str(error))
    st.info("Start the FastAPI server, then refresh this page.")
    st.stop()

st.subheader("Today's menu")
for row_start in range(0, len(menu), 3):
    for column, item in zip(st.columns(3), menu[row_start:row_start + 3]):
        with column:
            st.subheader(item["name"])
            st.metric("Price", format_price(item["price_pence"]))
            st.caption(f"{item['stock']} available" if item["stock"] else "Sold out")

if "trolley" not in st.session_state:
    st.session_state["trolley"] = {}

available = [item for item in menu if item["stock"] > 0]
st.subheader("Build your order")
if available:
    by_id = {item["id"]: item for item in available}
    with st.form("trolley_form", clear_on_submit=False):
        item_id = st.selectbox("Choose food", list(by_id), format_func=lambda value: by_id[value]["name"])
        quantity = st.number_input("Quantity", min_value=1, max_value=50, value=1, step=1)
        submitted = st.form_submit_button("Add to trolley", type="primary")
    if submitted:
        current_quantity = st.session_state["trolley"].get(item_id, 0)
        new_quantity = current_quantity + quantity
        if new_quantity > by_id[item_id]["stock"]:
            st.error(f"Only {by_id[item_id]['stock']} × {by_id[item_id]['name']} are currently available.")
        elif new_quantity > 50:
            st.error("A trolley can contain at most 50 of one product.")
        else:
            st.session_state["trolley"][item_id] = new_quantity
            st.rerun()
    st.caption("Adding an item does not reserve stock. Stock is checked when you check out.")
else:
    st.info("Everything is currently sold out.")

st.subheader("Your trolley")
trolley = st.session_state["trolley"]
menu_by_id = {item["id"]: item for item in menu}
if trolley:
    trolley_rows = []
    trolley_total = 0
    for trolley_item_id, trolley_quantity in trolley.items():
        item = menu_by_id[trolley_item_id]
        line_total = item["price_pence"] * trolley_quantity
        trolley_total += line_total
        trolley_rows.append({
            "Food": item["name"],
            "Quantity": trolley_quantity,
            "Line total": format_price(line_total),
        })
    st.dataframe(trolley_rows, hide_index=True, width="stretch")
    st.metric("Trolley total", format_price(trolley_total))

    remove_columns = st.columns(min(len(trolley), 4))
    for index, trolley_item_id in enumerate(list(trolley)):
        item = menu_by_id[trolley_item_id]
        with remove_columns[index % len(remove_columns)]:
            if st.button(
                f"Remove {item['name']}",
                key=f"remove-{trolley_item_id}",
            ):
                del st.session_state["trolley"][trolley_item_id]
                st.rerun()

    if st.button("Checkout", type="primary"):
        checkout_items = [
            {"item_id": trolley_item_id, "quantity": trolley_quantity}
            for trolley_item_id, trolley_quantity in trolley.items()
        ]
        try:
            order = request_api(
                "POST",
                "/checkout",
                json={"items": checkout_items},
            )
        except APIError as error:
            st.error(str(error))
        else:
            st.session_state["trolley"] = {}
            st.session_state["order_notice"] = (
                f"Order #{order['order_id']} placed with "
                f"{len(order['items'])} item type(s) — "
                f"{format_price(order['total_pence'])}."
            )
            st.rerun()
else:
    st.info("Your trolley is empty. Add something from the menu above.")

st.divider()
orders_tab, queue_tab = st.tabs(["Saved orders", "Kitchen estimates"])
with orders_tab:
    try:
        orders = request_api("GET", "/orders")
        if orders:
            st.dataframe([{"Order": order["id"], "Food": order["name"], "Quantity": order["quantity"], "Total": format_price(order["total_pence"]), "Status": order["status"]} for order in orders], hide_index=True, width="stretch")

            st.subheader("Staff order controls")
            st.caption("Advance each order through the kitchen one stage at a time.")
            next_status = {
                "queued": "preparing",
                "preparing": "ready",
                "ready": "collected",
            }
            active_orders = [order for order in orders if order["status"] in next_status]
            for order in active_orders:
                target_status = next_status[order["status"]]
                label = f"Order #{order['id']}: mark as {target_status}"
                if st.button(label, key=f"status-{order['id']}-{target_status}"):
                    try:
                        request_api(
                            "PATCH",
                            f"/orders/{order['id']}/status",
                            json={"status": target_status},
                        )
                    except APIError as error:
                        st.error(str(error))
                    else:
                        st.session_state["order_notice"] = (
                            f"Order #{order['id']} is now {target_status}."
                        )
                        st.rerun()

            if not active_orders:
                st.caption("There are no active orders to update.")
        else:
            st.info("No saved orders yet.")
    except APIError as error:
        st.error(str(error))
with queue_tab:
    stations = st.slider("Kitchen stations", min_value=1, max_value=10, value=2)
    st.caption("Recalculated from minute zero for all queued orders; these are invented estimates, not a live countdown.")
    try:
        queue = request_api("GET", "/queue", params={"stations": stations})
        left, middle, right = st.columns(3)
        left.metric("Average wait", f"{queue['average_waiting_minutes']} min")
        middle.metric("Longest wait", f"{queue['maximum_waiting_minutes']} min")
        right.metric("All ready after", f"{queue['all_ready_after_minutes']} min")
        if queue["schedule"]:
            st.dataframe(queue["schedule"], hide_index=True, width="stretch")
        else:
            st.info("No queued orders to simulate.")
    except APIError as error:
        st.error(str(error))
