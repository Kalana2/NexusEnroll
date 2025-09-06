import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { Course } from './../domain/models'
import { CourseRepository } from './../patterns/repository/CourseRepository';


const EnrollmentCtx = createContext<null | {
courses: Course[]
refresh: () => Promise<void>
}>(null)


export const EnrollmentProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
const repo = useMemo(() => new CourseRepository(), [])
const [courses, setCourses] = useState<Course[]>([])
async function refresh() { setCourses(await repo.list()) }
useEffect(() => { refresh() }, [])
return <EnrollmentCtx.Provider value={{ courses, refresh }}>{children}</EnrollmentCtx.Provider>
}


export const useEnrollment = () => {
const ctx = useContext(EnrollmentCtx)
if (!ctx) throw new Error('useEnrollment must be inside provider')
return ctx
}