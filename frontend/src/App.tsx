import { useState } from 'react'
import './App.scss'
import Student from './pages/Student.jsx'
import Login from './pages/Login.jsx';
import Admin from './pages/Admin.jsx';
import FacultyDashboard from './pages/FacultyDashboard.jsx';


function App() {
  const [role, setRole] = useState('');
  const [appState ,setAppState] = useState({
    courses:[
      {
      id: "CS101",
      name: "Introduction to Computer Science",
      instructor: "Dr. Jane Smith",
      semester:"1",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 15, total: 100 },
      prerequisites: ["ENG 101"],
    },
    {
      id: "CS201",
      semester:"2",
      name: "Data Structures and Algorithms",
      instructor: "Dr. John Doe",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 5, total: 80 },
      prerequisites: ["ENG 101"],
    },
    {
      id: "CS301",
      semester:"2",
      name: "Database Systems",
      instructor: "Dr. Alan Turing",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 15, total: 60 },
      prerequisites: ["ENG 101"],
    },
    {
      id: "MATH101",
      name: "Calculus I",
      semester:"1",
      instructor: "Dr. Robert Johnson",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 10, total: 120 },
      prerequisites: ["ENG 101"],
    },
    {
      id: "MATH201",
      name: "Linear Algebra",
      semester:"3",
      instructor: "Dr. Emily Chen",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 20, total: 90 },
      prerequisites: ["ENG 101"],
    },
    {
      id: "PHYS101",
      name: "Physics I",
      semester:"1",
      instructor: "Dr. Michael Brown",
      schedule: "Fri 09:00–11:30 (Hall E)",
      capacity: { enrolled: 15, total: 80 },
      prerequisites: ["ENG 101"],
    },

    ],
    users:[
      {
        id: 1,
        email:"admin@gmail.com",
        role:"admin",
        name:"chathura priyashan",
        password:"1234",
        contact: "0712345678"
      } ,
      {
        id: 2,
        email:"faculty@gmail.com",
        role:"faculty",
        name:"Dr.Jane Smith",
        password:"1234",
        contact: "0712345678",
      } ,
      {
        id: 3,
        contact: "0712345678",
        email:"faculty2@gmail.com",
        role:"faculty",
        name:"sahan gajanayake",
        password:"1234"

      } ,
      {
        id: 4,
        email:"student@gmail.com",
        role:"student",
        name:"kalana jinendra",
        password:"1234"

      } ,
    ],
    departments:[
      {
        id: 1,
        name:"Science",
      },
      {
        id:2,
        name:"Computer Science"
      },
      {
        id:2,
        name:"Art Department"
      }

    ],
    semesters:[1,2,3],
  })


  return (
    <>
    {
        (role == "student") ? <Student setRole={setRole} appState={appState} setAppState={setAppState}/> : 
        (role == "faculty") ? <FacultyDashboard setRole={setRole} appState={appState} setAppState={setAppState}/> :
        (role == "admin") ? <Admin setRole={setRole} setAppState={setAppState} appState={appState}/> : <Login setRole={setRole} appState={appState} setAppState={setAppState} />
    }
    </>
  )
}

export default App

