// import { Link, Route, Routes, Navigate } from "react-router-dom";
// import StudentPage from "./pages/StudentPage";
// import FacultyPage from "./pages/FacultyPage";
// import AdminPage from "./pages/AdminPage";
// import NotificationsPanel from "./components/NotificationsPanel";

// export default function App() {
//   return (
//     <div className="min-h-screen grid grid-rows-[auto,1fr]">
//       <header className="flex items-center gap-4 p-4 shadow-sm sticky top-0 bg-white z-10">
//         <h1 className="text-xl font-bold">NexusEnroll</h1>
//         <nav className="flex gap-3 text-sm">
//           <Link to="/student">Student</Link>
//           <Link to="/faculty">Faculty</Link>
//           <Link to="/admin">Admin</Link>
//         </nav>
//         <div className="ml-auto">
//           <NotificationsPanel />
//         </div>
//       </header>
//       <main className="p-4">
//         <Routes>
//           <Route path="/" element={<Navigate to="/student" replace />} />
//           <Route path="/student" element={<StudentPage />} />
//           <Route path="/faculty" element={<FacultyPage />} />
//           <Route path="/admin" element={<AdminPage />} />
//         </Routes>
//       </main>
//     </div>
//   );
// }


import { useState } from 'react'
import './App.scss'
import Student from './pages/Student.jsx'
import Login from './pages/Login.jsx';
import Admin from './pages/Admin.jsx';
import FacultyDashboard from './pages/FacultyDashboard.jsx';




function App() {
  const [role, setRole] = useState('');


  return (
    <>
    {
        (role == "student") ? <Student setRole={setRole}/> : 
        (role == "faculty") ? <FacultyDashboard setRole={setRole} /> :
        (role == "admin") ? <Admin setRole={setRole}/> : <Login setRole={setRole} />
    }
    </>
  )
}

export default App

