// src/pages/FacultyDashboard.jsx
import React, { useState } from "react";
import "./faculty.scss";

const FacultyDashboard = () => {
  const [students, setStudents] = useState([
    { id: "STU-1042", name: "Jamie Lee", email: "jamie.lee@example.edu", contact: "0712345678" },
    { id: "STU-1089", name: "Chris Paul", email: "chris.paul@example.edu", contact: "0787654321" },
    { id: "STU-1110", name: "Ava Smith", email: "ava.smith@example.edu", contact: "07712345678" },
  ]);

  const [grades, setGrades] = useState([
    { id: "STU-1042", name: "Jamie Lee", grade: "A-", status: "Pending" },
    { id: "STU-1089", name: "Chris Paul", grade: "B+", status: "Submitted" },
    { id: "STU-1110", name: "Ava Smith", grade: "K", status: "Invalid grade" },
  ]);

  const [course, setCourse] = useState({
    name: "Intro to Data Science",
    id: "DSC-201",
    instructor: "Alex Morgan",
    schedule: "Mon & Wed, 10:00-11:30",
    capacity: 30,
    credits: 3,
    description:
      "Foundational course covering data wrangling, visualization, and model evaluation.",
  });

  const handleGradeChange = (id, value) => {
    setGrades((prev) =>
      prev.map((g) => (g.id === id ? { ...g, grade: value } : g))
    );
  };

  const saveGrades = () => {
    console.log("Saving grades:", grades);
    alert("Grades saved!");
  };

  const saveCourse = () => {
    console.log("Saving course:", course);
    alert("Course changes submitted for approval!");
  };

  return (
    <div className="container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <img src="/static/img/logo.png" alt="logo" />
          <h1 className="sidebar-brand">NexusEnroll</h1>
        </div>

        <nav className="sidebar-nav">
          <div className="sidebar-section-title">STAFF MEMBER</div>
          <ul>
            <li className="nav-item">
              <img src="/static/img/course.png" alt="courses" />
              Courses
            </li>
            <li className="nav-item">
              <img src="/static/img/grade.png" alt="grades" />
              Grades
            </li>
            <li className="nav-item">
              <img src="/static/img/report.png" alt="reports" />
              Reports
            </li>
          </ul>
        </nav>

        <div className="sidebar-profile">
          <img
            src="https://i.pravatar.cc/40?img=23"
            alt="Alex Morgan"
            className="profile-pic"
          />
          <div className="profile-details">
            <span className="profile-name">Alex Morgan</span>
            <span className="profile-role">Staff Member</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="main-content">
        {/* Notifications */}
        <header className="top-bar">
          <div className="card">
            <div className="notification btn-light expand">
              <img src="/static/img/bell.png" alt="bell" /> Notifications
            </div>
            <div className="notif-bar" style={{ marginTop: "1rem" }}>
              New student enrolled to SA
            </div>
          </div>
        </header>

        {/* Enrolled Students */}
        <section className="enrolled-students-section card">
          <div className="section-header">
            <h2>Enrolled Students by Course</h2>
          </div>
          <input
            type="search"
            placeholder="Search Course Name or ID"
            className="section-search"
          />
          <button className="btn btn-primary">Search</button>
          <table className="table striped">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Student Name</th>
                <th>Email</th>
                <th>Contact NO</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>{s.id}</td>
                  <td>{s.name}</td>
                  <td>{s.email}</td>
                  <td>{s.contact}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Grades */}
        <section className="enter-grades-section card">
          <div className="section-header">
            <h2>Enter Grades by Course</h2>
          </div>
          <input
            type="search"
            placeholder="Search Course Name or ID"
            className="section-search"
          />
          <button className="btn btn-primary">Search</button>
          <table className="table striped">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Student Name</th>
                <th>Current Grade</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {grades.map((g) => (
                <tr key={g.id}>
                  <td>{g.id}</td>
                  <td>{g.name}</td>
                  <td>
                    <input
                      type="text"
                      value={g.grade}
                      className="grade-input"
                      onChange={(e) =>
                        handleGradeChange(g.id, e.target.value)
                      }
                    />
                  </td>
                  <td>
                    <span
                      className={`grade ${
                        g.status.toLowerCase().replace(" ", "-")
                      }`}
                    >
                      {g.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button className="btn btn-primary btn-save-all" onClick={saveGrades}>
            Save All Grades
          </button>
        </section>

        {/* Course Details */}
        <section className="course-details-section card">
          <div className="section-header">
            <h2>Course Details</h2>
          </div>
          <input
            type="search"
            placeholder="Search Course Name or ID"
            className="section-search"
          />
          <button className="btn btn-primary">Search</button>

          <form className="course-form" autoComplete="off" noValidate>
            <label htmlFor="course-name">Course Name</label>
            <input
              id="course-name"
              type="text"
              value={course.name}
              onChange={(e) =>
                setCourse((c) => ({ ...c, name: e.target.value }))
              }
            />

            <label htmlFor="course-id">Course ID</label>
            <input id="course-id" type="text" value={course.id} readOnly />

            <label htmlFor="instructor">Instructor</label>
            <input
              id="instructor"
              type="text"
              value={course.instructor}
              onChange={(e) =>
                setCourse((c) => ({ ...c, instructor: e.target.value }))
              }
            />

            <label htmlFor="schedule">Schedule</label>
            <input id="schedule" type="text" value={course.schedule} readOnly />

            <label htmlFor="capacity">Capacity</label>
            <input
              id="capacity"
              type="number"
              value={course.capacity}
              onChange={(e) =>
                setCourse((c) => ({ ...c, capacity: e.target.value }))
              }
            />

            <label htmlFor="credits">Credits</label>
            <input id="credits" type="number" value={course.credits} readOnly />

            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              rows="3"
              value={course.description}
              onChange={(e) =>
                setCourse((c) => ({ ...c, description: e.target.value }))
              }
            />

            <p className="note-info">
              Saving changes to description, prerequisites, or capacity will
              create a request for administrator approval.
            </p>
          </form>

          <button className="btn btn-primary btn-save-all" onClick={saveCourse}>
            Save Changes
          </button>
        </section>
      </main>
    </div>
  );
};

export default FacultyDashboard;
