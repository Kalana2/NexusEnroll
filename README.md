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
    Backend/
        +--- common/   # shared libs 
            __init__.py 
        +--- Db/
            __init__.py
            Singleton.
        +--- Auth/
            __init__.py
        +--- User-Service
        +--- Course-Service
        +--- Entrollment-Service
        +--- Notification-Service
        +--- Schedule-Service
        +--- Reporting-Service
        +--- Grade-Service
        +--- Api-Gateway
        


      bus.py            # simple publisher/subscriber wrapper
      schemas.py        # Pydantic event payloads

       +-- User-Service/
                +--- app.py #

```



---

## 🧩 Layers

1. **Adapters (I/O)**  
   - `http.py`: FastAPI routes → map HTTP requests to domain services.  

2. **Domain (Core Business)**  
   - `models.py`: Classes like `Enrollment`, `ClassOffering`.  
   - `transaction.py`: Implements **Proxy** → ensures commit/rollback semantics.  
   - `service.py`: Orchestrates enrollment logic (calls repo, emits events).  

3. **Infrastructure**  
   - `db.py`: SQLAlchemy persistence.  
   - `repo.py`: Encapsulates DB queries so domain logic doesn’t depend on SQL.  

---

## 🛠 Design Patterns Used

- **Proxy Pattern**  
  `TransactionProxy` wraps `EnrollmentTransaction`. Ensures that dropping/adding a course is all-or-nothing.  

- **Observer Pattern (via Event Bus)**  
  Publishes `SeatOpened` event when a student drops a course → `notification-service` consumes event.  

---

## 🔄 Enrollment Flow (Drop Course Example)

1. API Gateway → `POST /classes/{id}/drop`
2. FastAPI router → `EnrollmentService.drop_student(student_id, class_id)`
3. `TransactionProxy` begins DB transaction
4. Domain logic:
   - Remove student from class  
   - Increment available seats  
   - Publish `SeatOpened` event  
5. If any step fails → transaction rollback  
6. Commit transaction, response returned  

