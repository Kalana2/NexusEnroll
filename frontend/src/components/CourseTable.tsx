import React from 'react'
import type { Course } from './../domain/models'


export function CourseTable({ courses, onAdd }: { courses: Course[]; onAdd: (c: Course) => void }) {
return (
<div className="overflow-auto border rounded-2xl shadow-sm">
<table className="w-full text-sm">
<thead className="bg-gray-50">
<tr>
<th className="p-2 text-left">ID</th>
<th className="p-2 text-left">Course Name</th>
<th className="p-2 text-left">Instructor</th>
<th className="p-2 text-left">Schedule</th>
<th className="p-2 text-left">Capacity</th>
<th className="p-2 text-left">Prerequisites</th>
<th className="p-2 text-left">Actions</th>
</tr>
</thead>
<tbody>
{courses.map(c => (
<tr key={c.id} className="odd:bg-white even:bg-gray-50">
<td className="p-2">{c.id}</td>
<td className="p-2">{c.name}</td>
<td className="p-2">{c.instructor}</td>
<td className="p-2">{c.schedule}</td>
<td className="p-2">{c.capacity.enrolled} / {c.capacity.total}</td>
<td className="p-2">{c.prerequisites || 'None'}</td>
<td className="p-2"><button className="btn" onClick={() => onAdd(c)}>Add to Cart</button></td>
</tr>
))}
</tbody>
</table>
</div>
)
}