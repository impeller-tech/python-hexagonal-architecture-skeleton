# Messaging Rule (DDD + Hexagonal)

## Purpose

Define a consistent messaging topology for projects using **Domain-Driven Design (DDD)** and **Hexagonal Architecture**, avoiding rigid patterns that reduce scalability and operability.

---

## Core Rule

Do **not** adopt a fixed rule such as:

- `1 queue = 1 bounded context`

Instead, design messaging around:

- integration boundaries
- consumer isolation
- operational needs (SLA, retries, DLQ, scaling)

---

## Recommended Pattern

1. **Exchange per domain or bounded context** (depending on required isolation).
2. **Queues per consumer/use case** (not per entire bounded context).
3. **Routing keys per event/command type**.

---

## Why avoid `1 queue = 1 BC` as a standard

A single queue per bounded context often causes:

- mixed criticality workloads in the same queue
- poor retry and DLQ control granularity
- noisy message types blocking important flows
- inefficient scaling (all-or-nothing scaling)

---

## Template Topology

### 1) Integration Events

Each bounded context publishes **integration events** (not internal domain internals).

- Exchange: `<bc_or_domain>.events`
- Routing keys:
  - `<aggregate>.<entity>.<event_past_tense>`
  - `<aggregate>.<entity>.<event_past_tense>`
  - `<aggregate>.<entity>.<event_past_tense>`

Example:
- Exchange: `loans.events`
- Keys:
  - `loan.application.created`
  - `loan.application.validated`
  - `loan.application.approved`

### 2) Queues per Consumer / Use Case

Each consumer owns a dedicated queue and binding set.

- `<consumer_or_service>.<event_or_purpose>.q`
- `<consumer_or_service>.<event_or_purpose>.dlq`

Examples:
- `risk-assessment.loan-created.q`
- `notifications.loan-approved.q`
- `analytics.loan-*.q`

Per-queue policy checklist:
- [ ] prefetch/concurrency
- [ ] retry strategy
- [ ] DLQ binding
- [ ] message TTL
- [ ] max length / overflow policy
- [ ] priority (if needed)

### 3) Async Commands

Use queues per **capability/handler** (or command channel), not per full BC.

- `<capability>.commands.q`
- `<capability>.commands.dlq`

Examples:
- `loan-underwriting.commands.q`
- `disbursement.commands.q`

---

## Naming Convention Placeholders

- **Exchange (events)**: `<domain_or_bc>.events`
- **Exchange (commands)**: `<domain_or_bc>.commands`
- **Queue**: `<consumer_or_capability>.<purpose>.q`
- **DLQ**: `<same_queue_name>.dlq`
- **Routing key**: `<aggregate>.<entity>.<event_or_command>`

---

## Bounded Context Mapping

### `<bounded_context_name>`

**Publishes**
- `<event_name_1>`
- `<event_name_2>`

**Consumes**
- `<event_or_command_name_1>` via `<queue_name_1>`
- `<event_or_command_name_2>` via `<queue_name_2>`

**Adapters (Infra)**
- Publisher adapter: `<publisher_adapter_name>`
- Consumer adapter: `<consumer_adapter_name>`

---

## Hexagonal Placement

- **Domain**: unaware of broker (RabbitMQ/Kafka/etc.).
- **Application**: defines ports (`PublishEventPort`, `CommandHandlerPort`, etc.).
- **Infrastructure**: implements broker adapters (exchange/queue/binding/retry/DLQ).
- **Anti-Corruption Layer (ACL)**: translates contracts between bounded contexts.

---

## Bounded Context Structure Alignment

- Keep the messaging bounded context directly under `src/` (for example `src/messaging/`).
- Define messaging modules by business capability; each module keeps `domain/`, `application/`, and `infrastructure/`.
- Prefer module communication through domain events and contracts; orchestrate directly only when required.
- Put cross-context reusable code in `src/shared/`; keep messaging-only reusable code in `src/messaging/shared/`.
- Keep framework entrypoints outside `src/` (for example `apps/backend/`, `apps/webhooks/`).

---

## Reliability & Delivery Checklist

- [ ] At-least-once delivery assumptions documented
- [ ] Consumer idempotency strategy defined
- [ ] Outbox pattern considered for reliable publish
- [ ] Retry with backoff configured
- [ ] Poison-message handling to DLQ
- [ ] Observability: metrics, traces, structured logs
- [ ] Contract versioning strategy (`v1`, `v2`, …)

---

## MVP Exception (Allowed Temporarily)

Using `1 queue = 1 BC` can be accepted **only** if all are true:

- [ ] single async flow
- [ ] low traffic
- [ ] few consumers
- [ ] explicit plan to split queues later

Create a follow-up task:
- **Refactor trigger**: `<throughput_or_error_threshold>`
- **Owner**: `<team_or_role>`
- **Target date**: `<yyyy-mm-dd>`

---

## Executive Summary

> For DDD + Hexagonal systems:
> **Exchange per domain/context, queue per consumer/use case, routing key per event/command type**.
> Avoid “one queue per bounded context” as a default architecture rule.
