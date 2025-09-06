import type { Course } from "./../../domain/models";
import {
  CompositeValidation,
  CapacityStrategy,
  PrereqStrategy,
  TimeConflictStrategy,
} from "./../../patterns/strategy/validation";
import { EnrollCommand } from "./../../patterns/command/commands";
import { useBus } from "./../../patterns/observer/EventBus";

export function useEnrollmentFacade() {
  const bus = useBus();
  const validator = new CompositeValidation([
    new PrereqStrategy(),
    new CapacityStrategy(),
    new TimeConflictStrategy(),
  ]);

  async function tryEnroll(
    course: Course,
    ctx: {
      completed: string[];
      schedule: Array<{ time: string; courseId: string }>;
      studentId: number;
    }
  ) {
    const err = validator.validate(course, {
      completedCourses: ctx.completed,
      currentSchedule: ctx.schedule,
    });
    if (err) {
      bus.emit("ERROR", err);
      return { ok: false, message: err };
    }
    const cmd = new EnrollCommand(course, ctx.studentId);
    await cmd.execute();
    bus.emit("ENROLLED", { courseId: course.id });
    bus.emit("NOTIFY", `${course.name} added to enrollment`);
    return { ok: true };
  }

  return { tryEnroll };
}
