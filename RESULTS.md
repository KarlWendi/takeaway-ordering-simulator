# Queue experiment and interpretation

## Question

How does increasing preparation capacity change waiting and completion times for a fixed workload?

## Reproducible workload

Run `python queue_demo.py`. It does not use your database. Three orders are considered in this order: two burgers (6 preparation minutes), one fries (2 minutes), one wrap (4 minutes).

| Stations | Average waiting minutes | Maximum waiting minutes | All ready after minutes |
| --- | --- | --- | --- |
| 1 | 4.67 | 8 | 12 |
| 2 | 0.67 | 2 | 6 |
| 3 | 0 | 0 | 6 |

With two stations, order 1 starts on station 1 at minute zero and finishes at six. Order 2 starts on station 2 at zero and finishes at two. Order 3 then starts on station 2 at two and finishes at six. Average wait = (0 + 0 + 2) / 3 = 0.67 minutes, rounded.

## Observed saved-order snapshot

During the local demonstration on 16 September 2026, the queued workload was four wraps (16 minutes), eleven wraps (44 minutes), then two burgers (6 minutes). GET /queue was executed separately for one, two and three stations; all three requests returned 200.

| Stations | Average waiting minutes | Maximum waiting minutes | All ready after minutes |
| --- | --- | --- | --- |
| 1 | 25.33 | 60 | 66 |
| 2 | 5.33 | 16 | 44 |
| 3 | 0 | 0 | 44 |

For one station, starts are 0, 16 and 60, giving (0 + 16 + 60) / 3 = 25.33 minutes. For two stations, starts are 0, 0 and 16, giving 5.33 minutes. For three stations, all orders start at zero. These values describe this snapshot; later orders will change the result. The local restaurant.db is intentionally not uploaded.

## Finding

Extra capacity reduces waiting for these workloads. The third station removes waiting, but it cannot shorten the largest order's own duration. In the saved-order example, the 44-minute order determines the completion time for both two and three stations.

## Assumptions

- Every queued order is available at simulation minute zero; historic timestamps are ignored.
- Stations start free, are identical and handle one whole order at a time.
- ID order approximates arrival order; each next order uses the earliest-free station.
- Invented per-unit preparation times multiply by quantity. There is no batching or shared equipment.
- Simulation does not change order status, deduct stock, or track real elapsed time.

## Limits and future work

This is a scheduling simulation, not evidence of actual McDonald's waiting times or an optimal restaurant staffing level. A more realistic version could model arrivals, specialised equipment, batching and completed orders. A further experiment could compare ID order with shortest-job-first, measuring both average waiting and the longest wait to discuss efficiency and fairness.
