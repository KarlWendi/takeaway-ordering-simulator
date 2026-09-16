# Stage 8: publish a public demo

The website and API need running Python servers. GitHub Pages only serves static files and cannot run these servers. The public website link belongs in the README after it has been deployed and checked.

## Two services, one visitor link

- Website: Streamlit runs website.py and presents the public interface.
- API: Uvicorn runs api:app and stores accepted orders in SQLite.
- TAKEAWAY_API_URL: an environment variable on the website tells it where the hosted API lives. localhost on a hosting server means that server, not your home computer.
- TAKEAWAY_DATABASE_PATH: optionally points the API at a database on persistent storage. When omitted, it uses restaurant.db beside database.py, as before.

## Hosting decision

A free disposable demo can recreate its fictional database after server restarts. It must say clearly that data is temporary. A persistent version needs durable database storage. Render's persistent disks require a paid service; do not create paid resources without reviewing and accepting the cost.

Existing local restaurant.db is never uploaded. The public demo begins with fictional initial stock. All visitors would share this demo inventory unless a later stage adds separate visitor sessions.

## Render setup

Create two Python web services from this GitHub repository. For both, use the build command `pip install -r requirements.txt` and a supported Python version matching the tested workflow.

API start command:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Set the API health-check path to `/`. Once the API is running, copy its HTTPS service address.

Website start command:

```text
streamlit run website.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false
```

Set TAKEAWAY_API_URL on the website to the API's HTTPS address, without a trailing slash. Set its health-check path to `/_stcore/health`. Do not enter the local 127.0.0.1 address. Keep Streamlit's default browser security protections enabled.

For durable SQLite, attach a persistent disk to the API only and point TAKEAWAY_DATABASE_PATH at a file under its mount path, such as /var/data/restaurant.db. Keep a single API instance with this SQLite database.

## Before adding the live link

Open the website's public HTTPS address in a separate browser session. Confirm the menu loads, submit one fictional order, check the confirmation and stock, then refresh and change station counts without creating another order. Check unavailable stock rejection. Verify restart behaviour agrees with the chosen storage model. Only then add a `Try the live demo` link to README.md and the GitHub repository's Website field.

Signing up, authorising GitHub access and accepting hosting costs require the account owner. No public URL is available until the provider has successfully deployed both services.

References: [Render web services](https://render.com/docs/web-services), [persistent disks](https://render.com/docs/disks).
