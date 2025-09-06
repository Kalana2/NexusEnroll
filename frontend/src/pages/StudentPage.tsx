import React from 'react'
import { useEnrollment } from './../state/EnrollmentContext'
import { useEnrollmentFacade } from './../patterns/facade/EnrollmentFacade'
import { CourseTable } from './../components/CourseTable'


export default function StudentPage() {
const { courses, refresh } = useEnrollment()
const { tryEnroll } = useEnrollmentFacade()


async function handleAdd(course: any) {
const res = await tryEnroll(course, {
completed: ['ENG 101'],
schedule: [{ time: '09:00–11:30', courseId: 'ENG 102' }],
studentId: 1
})
if (res.ok) await refresh()
}


return (
<div className="grid gap-4">
<h2 className="text-lg font-semibold">Student — Course Catalogue</h2>
<CourseTable courses={courses} onAdd={handleAdd} />
</div>
)
}