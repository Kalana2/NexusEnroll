import React, { useState } from 'react'
import { useBus } from './../patterns/observer/EventBus'


export default function FacultyPage() {
const bus = useBus()
const [grade, setGrade] = useState('A-')
return (
<div className="grid gap-4 max-w-xl">
<h2 className="text-lg font-semibold">Faculty — Submit Grades</h2>
<label className="text-sm">Grade</label>
<input value={grade} onChange={e => setGrade(e.target.value)} className="border rounded p-2" />
<button className="btn" onClick={() => bus.emit('NOTIFY', `Grades submitted: ${grade}`)}>Submit</button>
</div>
)
}