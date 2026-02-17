# Bounded Context Structure (Template)

## Overview
The `<bounded_context_name>` bounded context is organized into **modules** to preserve the Single Responsibility Principle (SRP) and clear architectural boundaries.

## Bounded Context Location
Bounded contexts are located **directly in `/src/`**.

The structure is:
- `/src/` contains bounded contexts (e.g., `src/<bounded_context_name>/`)
- Each bounded context contains modules (e.g., `src/<bounded_context_name>/<module_a>/`)
- Future bounded contexts are added as siblings (e.g., `src/<another_context>/`, `src/<another_context_2>/`)

---

## Module Structure

Within the `<bounded_context_name>` bounded context, define modules by business capability.

### 1. `<module_a>/` Module
**Responsibility**: `<business capability / workflow>`

**Domain**:
- `<PrimaryEntityA>` entity
- `<DomainEventA>` domain event
- `<ValueObjectA>` value object
- Core business rules for `<module_a>`

**Application**:
- `<ModuleAService>`
- Commands/queries for `<module_a>` use cases

**Infrastructure**:
- Repository implementations
- Event publisher/subscriber adapters
- External provider adapters (if needed)

**Features**:
- Feature A.1: `<feature description>`
- Feature A.2: `<feature description>`

---

### 2. `<module_b>/` Module
**Responsibility**: `<business capability / workflow>`

**Domain**:
- `<PrimaryEntityB>` entity
- `<DomainEventB>` domain event
- `<ValueObjectB>` value object
- Core business rules for `<module_b>`

**Application**:
- `<ModuleBService>`
- Commands/queries for `<module_b>` use cases

**Infrastructure**:
- Repository implementations
- Provider adapters (e.g., messaging, AI, APIs)
- Subscriber handlers

**Features**:
- Feature B.1: `<feature description>`
- Feature B.2: `<feature description>`

---

### 3. `<module_c>/` Module
**Responsibility**: `<business capability / workflow>`

**Domain**:
- `<PrimaryEntityC>` entity
- `<DomainEventC>` domain event
- `<ValueObjectC>` value object
- Core business rules for `<module_c>`

**Application**:
- `<ModuleCService>`
- Commands/queries for `<module_c>` use cases

**Infrastructure**:
- Repository implementations
- External service adapters
- Event subscribers

**Features**:
- Feature C.1: `<feature description>`
- Feature C.2: `<feature description>`

---

## Module Communication

Modules communicate through:

1. **Domain Events** (preferred for loose coupling)
   - `<DomainEventA>` (`module_a`) → triggers `<action>`
   - `<DomainEventB>` (`module_b`) → triggers `<action>`
   - `<DomainEventC>` (`module_c`) → triggers `<action>`

2. **Shared Domain Concepts**
   - Concepts used across multiple bounded contexts go in `src/shared/domain/`
   - Concepts only used within this bounded context stay local to its modules

3. **Application Orchestration**
   - Application services may coordinate module interactions when explicit orchestration is required

---

## Shared Code

### Global Shared Code (`src/shared/`)
Code reused across **multiple bounded contexts**:

- **`shared/domain/`**:
  - Common value objects (e.g., `Email`, `UserId`, `Timestamp`)
  - Shared domain types and enums
  - Base domain exceptions

- **`shared/application/`**:
  - Base service classes
  - Cross-context DTOs
  - Shared validation utilities

- **`shared/infrastructure/`**:
  - Base adapter classes
  - Common infrastructure utilities (logging, retries, observability)
  - Shared configuration helpers

**Guideline**: Add code to `src/shared/` only when reused across multiple bounded contexts.

### Context-Level Shared Code (`src/<bounded_context_name>/shared/`)
Optional folder for code shared across modules **within one bounded context**.

- **`<bounded_context_name>/shared/domain/`**:
  - Context-specific value objects used by multiple modules
  - Shared domain types/exceptions inside this context

- **`<bounded_context_name>/shared/application/`**:
  - Shared DTOs/services/validators for this context

- **`<bounded_context_name>/shared/infrastructure/`**:
  - Shared adapters/utilities used by multiple modules

**Guidelines**:
- Optional: create only if there is meaningful reuse
- If code is used by one module only, keep it in that module
- If likely reused by other contexts, move to `src/shared/`

---

## SOLID Principles in Module Structure

### Single Responsibility Principle (SRP)
- Each module should have one clear business responsibility

### Dependency Inversion Principle (DIP)
- Modules depend on abstractions (ports), not concrete implementations
- Communication favors domain events and contracts over direct coupling
- Adapters remain swappable

### Open/Closed Principle (OCP)
- Add new modules/handlers without modifying stable existing modules

---

## Application / Framework Boundary

- **`src/`** contains business logic only (bounded contexts, domain, application, shared code, wiring)
- **Framework/app entrypoints** (e.g., `apps/backend/`, `apps/api/`, `apps/web/`) contain:
  - Routes/controllers
  - Request/response schemas
  - Framework bootstrap files
- The app layer depends on `src`, never the opposite

---

## Directory Structure (Template)

The codebase can use a **flat per-layer layout** within each module (e.g., `entities.py`, `events.py`, `value_objects.py`) instead of one file per entity.

```text
src/<bounded_context_name>/
├── <module_a>/
│   ├── domain/
│   │   ├── entities.py
│   │   ├── events.py
│   │   ├── value_objects.py
│   │   └── ports/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   └── infrastructure/
│       ├── adapters/
│       └── subscribers/
├── <module_b>/
│   ├── domain/
│   │   ├── entities.py
│   │   ├── events.py
│   │   ├── value_objects.py
│   │   └── ports/
│   ├── application/
│   │   └── services/
│   └── infrastructure/
│       ├── adapters/
│       └── subscribers/
├── <module_c>/
│   ├── domain/
│   │   ├── entities.py
│   │   ├── events.py
│   │   ├── value_objects.py
│   │   └── ports/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   └── infrastructure/
│       └── adapters/
├── persistence/
│   └── models.py
└── shared/
    ├── domain/
    ├── application/
    └── infrastructure/
```
