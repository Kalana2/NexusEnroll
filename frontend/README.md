# NexusEnroll (React + Design Patterns)


## Run
1. npm i
2. npm run api # starts json-server on http://localhost:3001
3. npm run dev # starts React app on http://localhost:5173


## Where patterns live
- Facade: src/patterns/facade/EnrollmentFacade.ts
- Repository: src/patterns/repository/CourseRepository.ts
- Strategy: src/patterns/strategy/validation.ts
- Command: src/patterns/command/commands.ts
- Observer: src/patterns/observer/EventBus.tsx
- Adapter: src/services/apiClient.ts (ApiError)
- Factory (example idea): could add a NotificationFactory to build Notification objects per type.