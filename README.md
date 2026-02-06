# Cloud ELT – Synthetic Healthcare Data

## Overview
This project is a **ELT portfolio build** that simulates realistic UK hospital operational data and processes it through a modern data‑engineering stack. It is designed to demonstrate **data engineering concepts**: event‑driven source data, immutable raw storage, columnar analytics, and warehouse modelling.

The system generates synthetic but *realistic* inpatient activity (admissions, discharges, bed pressure, waiting lists, and operational snapshots), lands the data in object storage, and transforms it downstream for analytics and visualisation.

---

## Key Goals

- Simulate realistic hospital pressure dynamics (finite beds, queues, long stays)
- Capture event‑level and snapshot‑level data as would occur in real systems
- Follow ELT best practice (raw → staging → curated → marts)
- Development and testing are performed on a VPS to validate ELT logic before scaling to cloud-managed services
- Use cloud‑native patterns (object storage, columnar analytics)

---

## Architecture – Development & Validation

```
Synthetic Source Generator (Python)
↓
Amazon S3 (Raw / Immutable JSON Events)
↓
Staging Layer (PyArrow Normalisation → Parquet on S3)
↓
ClickHouse (Curated Warehouse – Star Schema)
↓
Analytics / BI (Power BI)
```

## Architecture – Post-Migration

```
Synthetic Source Generator (Python)
↓
Amazon S3 (Raw / Immutable JSON Events)
↓
Staging Layer (Parquet on S3)
↓
Amazon Redshift (Curated Warehouse – Star Schema)
↓
Analytics / BI (Power BI)
```

### Migration stages

- Source generator: Local filesystem (VPS) → Amazon S3
- Staging: PyArrow-based normalisation → Parquet on S3
- Curated warehouse: ClickHouse → Amazon Redshift

---

## Data Domains

### Admissions
- Patient admission requests
- Department assignment subject to bed availability
- Admission timestamps

### Discharges
- Variable length of stay
- Long‑stay and bed‑blocking scenarios
- Natural pressure relief over time

### Waiting List
- First In First Out (FIFO) waiting list when no beds are available
- Captures:
  - patient_id
  - request_date
  - wait_duration
- Daily snapshots allow queue‑length and delay analysis

### Operational Snapshots
- **Start‑of‑day (SOD)** and **End‑of‑day (EOD)** snapshots
- Departments:
  - beds
  - occupied beds
  - capacity
- Waiting list size

---

## Source Data Generation

- Finite beds per department
- Patients cannot be admitted twice on same day or before they have been discharged
- Admissions follow a **Poisson derived daily rate** based on maximum stay per department
- Seasonal pressure simulated using monthly multiplier
- Generation of long-stay patients to simulate bed-blocking (1%) and delayed discharge (5%)

All source outputs are emitted as **individual JSON events**.

---

## Raw Layer (S3)

- Immutable JSON objects
- One event per file
- Partitioned by event type and event date (daily)
- Append only

Example:

```
/admission/event_date=2024-03-15/admission_<uuid>.json
/discharge/event_date=2024-03-15/discharge_<uuid>.json
/wait_snapshot/event_date=2024-03-15/wait_snapshot_<uuid>.json
/dep_snapshot/event_date=2024-03-15/dep_snapshot_<uuid>.json
```
---

## Staging Layer (S3)

- Immutable Parquet files
- Events grouped by month
- Partitioned by event type and month (monthly)
- Schema enforced at write time using PyArrow

Example:

```
/admission/event_date=2024-03/admission.parquet
/discharge/event_date=2024-03/discharge.parquet
/wait_snapshot/event_date=2024-03/wait_snapshot.parquet
/dep_snapshot/event_date=2024-03/dep_snapshot.parquet
```
---

## ELT Philosophy

- Minimal transformation upstream
- No business logic in the source generator
- Raw data is always preserved
- All modelling happens downstream in SQL
- Mirror real‑world cloud data platforms

---

## Warehouse Modelling

### Curated Layer

Kimball‑style star schema:

- **Fact tables**
  - fact_admissions
  - fact_discharges
  - fact_waiting_list
  - fact_department_occupancy

- **Dimension tables**
  - dim_patient
  - dim_department
  - dim_date

### Analytics & Marts

- Waiting time percentiles (P90 / P95)
- Bed utilisation trends
- Queue growth vs discharge rate
- Pressure simulation validation

Percentiles and aggregations are calculated **in the warehouse**, not upstream.

---

## Columnar Analytics

The platform is designed around **columnar execution**:

- Typical analysis:
  - wait times by department
  - occupancy by date
  - percentile‑based KPIs

---

## Engineering Decisions (Intentional)

| Decision | Reason |
|--------|-------|
| Event‑level JSON | Matches real source systems |
| Snapshots + events | Enables operational analytics |
| UUID‑based object keys | Avoids collisions & retries |
| No early aggregation | Preserves analytical flexibility |

---

## What This Project Is and Is Not

**This is:**
- A realistic data‑engineering simulation
- A cloud‑first ELT design
- A portfolio project showing judgement and trade‑offs

**This is not:**
- A clinical system
- A patient‑level analytics product

---

## How to Run (High Level)

1. Create and activate Python virtual environment
2. Run source generator to emit events
3. Events are written to S3
4. Query raw data via Athena or load into Redshift
5. Build curated models via SQL

(Exact commands documented in `/src`)

---

## Future Enhancements

- dbt models for curated layer
- Data quality checks (row counts, nulls, late events)
- Power BI dashboards
- Incremental warehouse loading

---

