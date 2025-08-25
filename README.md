# 🎓 Nexus Enroll



## 📐 1. Backend Architecture Overview

### Microservices (bounded contexts)
- **user-service** – Users, roles, user states (Active/Suspended/Pending)
- **course-service** – Courses, Classes, Prerequisites
- **enrollment-service** – Add/Drop + atomic transactions (Proxy)
- **notification-service** – Sends notifications (Observer)
- **schedule-service** – Calendar-like views (Decorator)
- **reporting-service** – Report export (Adapter)
- **grades-service** – Batch grade processing (Command)
- **api-gateway** *(optional)* – Routing / auth / aggregation

### File Structure

```
/NexusEnroll/
│
├── api-gateway/                        # Optional edge gateway
│   ├── src/
│   │   ├── routes/                     # Route definitions & aggregations
│   │   ├── middleware/                 # Auth, logging, rate-limiting
│   │   ├── services/                   # Calls to backend services
│   │   ├── __init__.py (or main.go, etc.)
│   │
│   ├── Dockerfile
│   └── package.json (or go.mod, etc.)
│
├── user-service/
│   ├── src/
│   │   ├── controllers/                # REST/GraphQL endpoints
│   │   ├── models/                     # User, Role, UserState
│   │   ├── services/                   # Business logic
│   │   ├── repositories/               # DB access
│   │   ├── events/                     # Publish user events (created, suspended)
│   │   ├── __init__.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
│
├── course-service/
│   ├── src/
│   │   ├── controllers/                # Manage courses, classes
│   │   ├── models/                     # Course, Class, Prerequisites
│   │   ├── services/                   # Capacity mgmt, validation
│   │   ├── repositories/
│   │   ├── events/                     # Publish updates for enrollment-service
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── enrollment-service/
│   ├── src/
│   │   ├── controllers/                # Add/Drop endpoints
│   │   ├── services/                   # Atomic transaction logic
│   │   ├── models/                     # Enrollment, Waitlist
│   │   ├── repositories/
│   │   ├── events/                     # Notify capacity/waitlist changes
│   │   ├── sagas/                      # Orchestrate cross-service transactions
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── notification-service/
│   ├── src/
│   │   ├── subscribers/                # Listen to pub/sub topics
│   │   ├── channels/                   # Email, SMS, WebPush adapters
│   │   ├── services/                   # Observer logic
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── schedule-service/
│   ├── src/
│   │   ├── controllers/
│   │   ├── decorators/                 # Flexible calendar decorators
│   │   ├── services/                   # Calendar building logic
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── reporting-service/
│   ├── src/
│   │   ├── controllers/                # Endpoints to export reports
│   │   ├── adapters/                   # CSV, XLSX, PDF exporters
│   │   ├── services/                   # Data aggregation
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── grades-service/
│   ├── src/
│   │   ├── commands/                   # Batch grade commands
│   │   ├── handlers/                   # Command pattern handlers
│   │   ├── models/                     # Grade, Assignment, BatchJob
│   │   ├── services/
│   │   ├── __init__.py
│   │
│   ├── Dockerfile
│   └── package.json
│
├── common-libs/                        # Shared libraries (optional)
│   ├── auth/                           # JWT, OAuth utils
│   ├── events/                         # Event bus/pubsub abstraction
│   ├── db/                             # Common DB clients/config
│   └── logger/                         # Shared logging
│
├── docker-compose.yml     
│
└── README.md


```
