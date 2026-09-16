"""Stage 7: python -m streamlit run website.py (start the API first)."""
import streamlit as st
from menu import format_price
from web_client import APIError, request_api

st.set_page_config(page_title="Takeaway Kitchen", page_icon="🍔", layout="wide")
st.title("🍔 Takeaway Kitchen")
st.caption("A fictional ordering simulation · no payments or real deliveries")

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
for column, item in zip(st.columns(max(1, len(menu))), menu):
    with column:
        st.subheader(item["name"])
        st.metric("Price", format_price(item["price_pence"]))
        st.caption(f"{item['stock']} available" if item["stock"] else "Sold out")

available = [item for item in menu if item["stock"] > 0]
st.subheader("Place an order")
if available:
    by_id = {item["id"]: item for item in available}
    # Only a submitted form sends POST. Other reruns only read data.
    with st.form("order_form", clear_on_submit=False):
        item_id = st.selectbox("Choose food", list(by_id), format_func=lambda value: by_id[value]["name"])
        quantity = st.number_input("Quantity", min_value=1, max_value=50, value=1, step=1)
        submitted = st.form_submit_button("Place simulated order", type="primary")
    if submitted:
        try:
            order = request_api("POST", "/orders", json={"item_id": item_id, "quantity": quantity})
        except APIError as error:
            st.error(str(error))
        else:
            st.session_state["order_notice"] = f"Order #{order['order_id']} saved: {order['quantity']} × {order['name']} — {format_price(order['total_pence'])}."
            st.rerun()
    st.caption("One food type per order. Each successful submission creates a new order. Availability is checked by the API.")
else:
    st.info("Everything is currently sold out.")

st.divider()
orders_tab, queue_tab = st.tabs(["Saved orders", "Kitchen estimates"])
with orders_tab:
    try:
        orders = request_api("GET", "/orders")
        if orders:
            st.dataframe([{"Order": order["id"], "Food": order["name"], "Quantity": order["quantity"], "Total": format_price(order["total_pence"]), "Status": order["status"]} for order in orders], hide_index=True, width="stretch")
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
