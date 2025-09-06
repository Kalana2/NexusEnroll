// src/pages/EditCourse.jsx
import React, { useState } from "react";
import "./courseeditform.scss";

const EditCourse = () => {
  const [form, setForm] = useState({
    courseCode: "CSCI-201",
    title: "Data Structures",
    department: "Computer Science",
    credits: 3,
    description:
      "Study of common data structures, algorithms, and applications.",
    level: "Undergraduate",
    status: "Active",
    instructors: ["Prof. A. Rahman", "Dr. L. Chen"],
    prerequisites: [{ course: "CSCI-101 • Intro to CS", grade: "C", type: "Required" }],
    gradingScheme: "A-F",
    allowAudit: "No",
    repeatable: "No",
    maxRepeats: 0,
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setForm((prev) => ({ ...prev, [id]: value }));
  };

  const handleSave = () => {
    console.log("Saving course:", form);
    alert("Course changes saved!");
  };

  return (
    <div className="modal-overlay edit-course">
      <div className="modal">
        {/* Header */}
        <div className="modal-header">
          <div className="modal-title">
            <div className="edit-icon"></div>
            Edit course
          </div>
          <div className="admin-badge">Administrator</div>
        </div>

        {/* Course header */}
        <div className="course-header">
          <h1 className="course-title">
            {form.courseCode} • {form.title}
          </h1>
          <div className="course-meta">
            <span className="badge badge-undergraduate">{form.level}</span>
            <span
              className={`badge ${
                form.status === "Active" ? "badge-active" : "badge-inactive"
              }`}
            >
              {form.status}
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="tabs">
          <a href="#" className="tab active">
            Details
          </a>
          <a href="#" className="tab">
            Scheduling
          </a>
          <a href="#" className="tab">
            Enrollment
          </a>
        </div>

        {/* Content */}
        <div className="content">
          {/* Form grid */}
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="courseCode">Course code</label>
              <input
                type="text"
                id="courseCode"
                value={form.courseCode}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                type="text"
                id="title"
                value={form.title}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="department">Department</label>
              <select
                id="department"
                value={form.department}
                onChange={handleChange}
              >
                <option>Computer Science</option>
                <option>Mathematics</option>
                <option>Engineering</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="credits">Credits</label>
              <input
                type="number"
                id="credits"
                value={form.credits}
                onChange={handleChange}
              />
            </div>
            <div className="form-group full-width">
              <label htmlFor="description">Short description</label>
              <textarea
                id="description"
                value={form.description}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="level">Level</label>
              <select id="level" value={form.level} onChange={handleChange}>
                <option>Undergraduate</option>
                <option>Graduate</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select id="status" value={form.status} onChange={handleChange}>
                <option>Active</option>
                <option>Inactive</option>
                <option>Archived</option>
              </select>
            </div>
          </div>

          {/* Instructors */}
          <div className="section">
            <div className="section-header">
              <span className="section-icon">👥</span>
              Instructors
            </div>
            <div className="search-container">
              <input
                type="text"
                className="search-input"
                placeholder="Search or add instructor"
              />
              <button className="add-button">Add</button>
            </div>
            <div>
              {form.instructors.map((inst, i) => (
                <span key={i} className="instructor-item">
                  {inst}
                </span>
              ))}
            </div>
          </div>

          {/* Prerequisites */}
          <div className="section">
            <div className="section-header">
              <span className="section-icon">📋</span>
              Prerequisites
            </div>
            <div className="search-container">
              <input
                type="text"
                className="search-input"
                placeholder="Search course"
              />
              <button className="add-button">Add</button>
            </div>
            <table className="table">
              <thead>
                <tr>
                  <th>Course</th>
                  <th>Minimum Grade</th>
                  <th>Type</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {form.prerequisites.map((p, i) => (
                  <tr key={i}>
                    <td>{p.course}</td>
                    <td>{p.grade}</td>
                    <td>{p.type}</td>
                    <td>
                      <div className="action-buttons">
                        <button className="btn-edit">Edit</button>
                        <button className="btn-remove">Remove</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Policies */}
          <div className="section">
            <div className="section-header">
              <span className="section-icon">⚙️</span>
              Policies
            </div>
            <div className="policies-grid">
              <div className="form-group">
                <label htmlFor="gradingScheme">Grading scheme</label>
                <select
                  id="gradingScheme"
                  value={form.gradingScheme}
                  onChange={handleChange}
                >
                  <option>A-F</option>
                  <option>Pass/Fail</option>
                  <option>Numeric</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="allowAudit">Allow audit</label>
                <select
                  id="allowAudit"
                  value={form.allowAudit}
                  onChange={handleChange}
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="repeatable">Repeatable</label>
                <select
                  id="repeatable"
                  value={form.repeatable}
                  onChange={handleChange}
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="maxRepeats">Max repeats</label>
                <input
                  type="number"
                  id="maxRepeats"
                  value={form.maxRepeats}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>

          {/* Warning */}
          <div className="warning">
            Changes affect upcoming terms unless applied to current sections in
            Scheduling.
          </div>
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <a href="#" className="btn-back">
            Back
          </a>
          <div className="footer-actions">
            <button className="btn-discard">✕ Discard</button>
            <button className="btn-save" onClick={handleSave}>
              Save changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditCourse;
