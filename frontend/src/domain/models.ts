export type Course = {
id: string
name: string
instructor: string
schedule: string
capacity: { enrolled: number; total: number }
prerequisites: string
}


export type Enrollment = {
id?: number
courseId: string
studentId: number
status: 'ready' | 'pending' | 'conflict'
}


export type User = { id: number; email: string; password?: string; role: 'student' | 'faculty' | 'admin'; name: string }


export type Notification = { id?: number; message: string; type: 'System' | 'Update' | 'Assignment'; time: string; unread?: boolean }