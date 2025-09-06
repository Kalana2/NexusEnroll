import { api } from "./../../services/apiClient";
import type { Course } from "./../../domain/models";


// Repository interface
export interface ICourseRepository {
  list(): Promise<Course[]>;
  get(id: string): Promise<Course>;
  create(course: Course): Promise<Course>;
  update(id: string, partial: Partial<Course>): Promise<Course>;
  delete(id: string): Promise<void>;
}

// Implementation
export class CourseRepository implements ICourseRepository {
  async list() {
    return api.get<Course[]>("/courses");
  }

  async get(id: string) {
    return api.get<Course>(`/courses/${id}`);
  }

  async create(course: Course) {
    return api.post<Course>("/courses", course);
  }

  async update(id: string, partial: Partial<Course>) {
    return api.patch<Course>(`/courses/${id}`, partial);
  }

  async delete(id: string) {
    return api.delete<void>(`/courses/${id}`);
  }
}
