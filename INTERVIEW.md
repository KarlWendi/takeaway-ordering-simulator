# Explain the project in your own words

Use these prompts to practise. They are examples to adapt, not claims you must memorise. This project was developed with AI assistance; describe that honestly and be ready to explain, test and modify the code yourself.

## A short introduction

“I worked on a Python takeaway simulation to understand how orders, stock and kitchen capacity connect. It accepts orders through a local API, saves them in SQLite and estimates kitchen queue timings. I compared different station counts and documented what the simplified model assumes.”

## Questions and answer checkpoints

| Question | What your explanation should cover |
| --- | --- |
| What happens when an order arrives? | Validate fields, reserve stock, calculate the total, save the order, commit and return JSON. |
| How do you avoid losing stock if saving fails? | The stock update and order insert are in one transaction; a failure rolls back both. |
| Why store prices as integer pence? | Exact whole-number calculations; format pounds only for display. |
| What is an API endpoint? | A method and path identifying an operation; GET /orders reads, POST /orders creates. |
| What does the database add? | Persistent structured data, constraints and transactions. |
| How does the scheduler choose a station? | For each next order, find the station with the earliest available time. |
| Why do three stations still take 44 minutes in the snapshot? | The largest order itself needs 44 minutes under the invented rules. |
| How did you check correctness? | Automated tests plus live requests, stock checks and a restart test; explain one concrete failure case. |
| What does GitHub contribute? | Source, explanations, real stage commits and automatic tests. It does not host a running API here. |
| What would you improve? | Choose one limitation and describe a small next step, such as ingredient stock or status changes. |

## Connect it to restaurant work

- Accurate input checks help avoid mistakes in orders.
- Consistent inventory changes help explain availability.
- Queue comparisons show why preparation capacity affects customers' waits.
- Documenting assumptions shows that simulated results need checking against real working conditions.
- Describe a real troubleshooting example: matching the editor and terminal to the same Python installation, or updating an imported file when a required function was missing.

## Exercises that show understanding

1. Explain the transaction without looking at your code.
2. Predict a schedule for preparation durations 6, 2 and 4 with two stations.
3. Change a fictional price and update your expected test result. Remember existing database prices are not overwritten on startup.
4. Point to the code that rejects zero quantity and the test that checks rejection.
5. Explain why a successful repeated POST creates a second order, whereas repeated GET /queue does not.

A finished portfolio demonstrates the implementation. Your own understanding is demonstrated by answering these questions and making a small change you can explain.
