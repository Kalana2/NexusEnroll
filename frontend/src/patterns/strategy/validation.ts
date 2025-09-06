import type { Course } from "./../../domain/models";

export interface ValidationContext {
  completedCourses: string[];
  currentSchedule: Array<{ time: string; courseId: string }>;
}

export interface ValidationStrategy {
  validate(course: Course, ctx: ValidationContext): string | null; // return error message or null
}

export class PrereqStrategy implements ValidationStrategy {
  validate(course: Course, ctx: ValidationContext) {
    if (!course.prerequisites || course.prerequisites === "None") return null;
    return ctx.completedCourses.includes(course.prerequisites)
      ? null
      : `Missing prerequisite: ${course.prerequisites}`;
  }
}

export class CapacityStrategy implements ValidationStrategy {
  validate(course: Course) {
    return course.capacity.enrolled < course.capacity.total
      ? null
      : "Course is full";
  }
}

export class TimeConflictStrategy implements ValidationStrategy {
  validate(course: Course, ctx: ValidationContext) {
    const time = course.schedule.split(" ")[1]; // naive parse e.g., 09:00–11:30
    const conflict = ctx.currentSchedule.find((s) => s.time === time);
    return conflict ? `Time conflict with ${conflict.courseId}` : null;
  }
}

export class CompositeValidation implements ValidationStrategy {
  constructor(private strategies: ValidationStrategy[]) {}
  validate(course: Course, ctx: ValidationContext) {
    for (const s of this.strategies) {
      const e = s.validate(course, ctx);
      if (e) return e;
    }
    return null;
  }
}
