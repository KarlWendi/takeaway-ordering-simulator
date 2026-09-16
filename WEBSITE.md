# Stage 7: a website written in Python

Streamlit builds the browser interface from website.py. You do not write HTML. web_client.py sends HTTP requests to the existing FastAPI service; database.py remains responsible for transactions and stock.

## Start locally

Open two terminals in the repository folder, using the same Python environment:

```text
python -m pip install -r requirements.txt
```

Terminal one:

```text
python -m uvicorn api:app --reload
```

Terminal two:

```text
python -m streamlit run website.py --server.address 127.0.0.1
```

Open http://127.0.0.1:8501. Keep both terminals running. For the demonstration virtual environment on Windows, replace python with .\.venv\Scripts\python.exe. This is a local website; uploading code to GitHub does not publish a running service.

## Understand each part

1. st.title, st.columns and st.metric create the menu and price display.
2. GET /menu supplies real database stock. Sold-out items cannot be selected.
3. st.form collects the food and quantity. Only its submit button triggers POST /orders.
4. The API validates the request and uses the existing transaction. A stale stock display never bypasses the API's stock check.
5. A successful response becomes a confirmation in st.session_state. st.rerun refreshes stock and orders without submitting the form again.
6. The slider changes GET /queue?stations=..., which only calculates. It does not reduce stock.

Streamlit reruns the Python script after interactions. That is why POST belongs inside `if submitted`, and why it is never cached or automatically retried. A connection failure may happen after an order was saved: check the saved-order list before submitting again. Duplicate-request protection is still future work.

TAKEAWAY_API_URL optionally changes the service address on the Streamlit server. The browser itself does not call FastAPI; Streamlit's Python process does. Both processes must be able to reach the configured service.

## Demonstrate and check

Read the menu, submit one available item, check its confirmation and decreased stock, refresh without placing another order, and compare station counts. Try a quantity greater than remaining stock: the service rejects it and stock remains unchanged. Stop the API to see the friendly connection error, then restart it. Automated website tests use a temporary database and verify that refresh and station changes cannot create orders.

This stage supports one product type per order, retains the existing fictional timings and has no payment processing. Public hosting and authentication are separate future stages.

Framework references: [forms](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form), [running an app](https://docs.streamlit.io/develop/concepts/architecture/run-your-app).
