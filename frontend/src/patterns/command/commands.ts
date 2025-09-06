import type { Course, Enrollment } from "./../../domain/models";
import { api } from "./../../services/apiClient";

export interface Command {
  execute(): Promise<void>;
  undo(): Promise<void>;
}

export class EnrollCommand implements Command {
  private createdId: number | null = null;
  constructor(private course: Course, private studentId: number) {}
  async execute() {
    const e = await api.post<Enrollment>("/enrollments", {
      courseId: this.course.id,
      studentId: this.studentId,
      status: "ready",
    });
    this.createdId = e.id!;
    await api.patch(`/courses/${this.course.id}`, {
      capacity: {
        ...this.course.capacity,
        enrolled: this.course.capacity.enrolled + 1,
      },
    });
  }
  async undo() {
    if (this.createdId != null)
      await api.delete(`/enrollments/${this.createdId}`);
    await api.patch(`/courses/${this.course.id}`, {
      capacity: {
        ...this.course.capacity,
        enrolled: Math.max(0, this.course.capacity.enrolled - 1),
      },
    });
  }
}

export class DropCommand implements Command {
  constructor(private enrollmentId: number, private course: Course) {}
  async execute() {
    await api.delete(`/enrollments/${this.enrollmentId}`);
    await api.patch(`/courses/${this.course.id}`, {
      capacity: {
        ...this.course.capacity,
        enrolled: Math.max(0, this.course.capacity.enrolled - 1),
      },
    });
  }
  async undo() {
    /* intentionally left simple for demo */
  }
}
