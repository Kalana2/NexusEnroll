import { api } from "./../../services/apiClient";
import type { Course } from "./../../domain/models";

export interface ICourseRepository {
  list(): Promise<Course[]>;
  get(id: string): Promise<Course>;
  update(id: string, partial: Partial<Course>): Promise<Course>;
}

export class CourseRepository implements ICourseRepository {
  async list() {
    return api.get<Course[]>("/courses");
  }
  async get(id: string) {
    return api.get<Course>(`/courses/${id}`);
  }
  async update(id: string, partial: Partial<Course>) {
    return api.patch<Course>(`/courses/${id}`, partial);
  }
}
