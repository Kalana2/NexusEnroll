// src/pages/CourseForm.jsx
import React, { useState } from "react";
import "./courseform.scss";


const NewCourseForm = () => {
    const [prerequisites, setPrerequisites] = useState([""]);
    const [textbooks, setTextbooks] = useState([{ title: "", author: "", isbn: "" }]);
    const [startDate , setStartDate] = useState('');
    const [endDate , setEndDate] = useState('');
    const [semester , setSemester] = useState('');
    const [startTime , setStartTime] = useState('')
    const [endTime , setEndTime] = useState('')
    const [code , setCode] = useState('')
    const [department , setDepartment] = useState('');
    const [capacity , setCapacity] = useState(0);
    const [title, setTitle] = useState('');
    const [credit ,setCredit]= useState(1);
    const [description ,setDescription]= useState(1);
    const [instructor , setInstructor] = useState('')
    const [room , setRoom] = useState('')


  // Handlers for prerequisites
  const addPrerequisite = () => setPrerequisites([...prerequisites, ""]);
  const removePrerequisite = (index) => {
    setPrerequisites(prerequisites.filter((_, i) => i !== index));
  };
  const updatePrerequisite = (index, value) => {
    const updated = [...prerequisites];
    updated[index] = value;
    setPrerequisites(updated);
  };

  // Handlers for textbooks
  const addTextbook = () =>
    setTextbooks([...textbooks, { title: "", author: "", isbn: "" }]);
  const removeTextbook = (index) => {
    setTextbooks(textbooks.filter((_, i) => i !== index));
  };
  const updateTextbook = (index, field, value) => {
    const updated = [...textbooks];
    updated[index][field] = value;
    setTextbooks(updated);
  };

  // Submit handler
  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      prerequisites,
      textbooks,
      startDate ,
      endDate,
      endTime,
      startTime,
      department,
      capacity,
      title,
      credit,
      description,
      instructor,
      room,
      code
    };
    console.log("Form submitted:", data);
    alert("Course created (check console for data)");
  };

  return (
    <div className=".course_form form-container">
      <div className="container">
        <h1 className="heading">Add New Course</h1>
        <p className="subheading">
          Create a new course offering with all necessary details and requirements.
        </p>
      </div>

      <form className="form-content" onSubmit={handleSubmit}>
        {/* Basic Information Section */}
        <div className="section">
          <h2 className="section-title">Basic Information</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="course-code">
                Course Code <span className="required">*</span>
              </label>
              <input type="text" id="course-code" value={code} placeholder="e.g., CS 101" onChange={(e)=>setCode(e.target.value)} />
            </div>
            <div className="form-group">
              <label htmlFor="department">
                Department <span className="required">*</span>
              </label>
              <select id="department"  value={department} onSelect={e=>setDepartment(e.target.value)}>
                <option value="">Select Department</option>
                <option value="cs">Computer Science</option>
                <option value="math">Mathematics</option>
                <option value="eng">Engineering</option>
                <option value="bus">Business</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group full-width">
              <label htmlFor="course-title">
                Course Title <span className="required">*</span>
              </label>
              <input
                value={title}
                onChange={(e)=>setTitle(e.target.value)}
                type="text"
                id="course-title"
                placeholder="e.g., Introduction to Computer Science"
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="credit-hours">
                Credit <span className="required">*</span>
              </label>
              <input type="number" value={credit} onChange={e=>setCredit(e.target.value)} id="credit-hours" defaultValue={3} min={1} max={6} />
            </div>

            <div className="form-group">
              <label htmlFor="student-capacity">
                Student Capacity <span className="required">*</span>
              </label>
              <input type="number" value={capacity} onChange={e=>setCapacity(e.target.value)} id="student-capacity" defaultValue={30} min={1} />
            </div>
          </div>



          <div className="form-row">
            <div className="form-group full-width">
              <label htmlFor="course-description">
                Course Description <span className="required">*</span>
              </label>
              <textarea
                value={description}
                OnChange={(e)=>setDescription(e.target.value)}
                id="course-description"
                placeholder="Provide a detailed description..."
              />
            </div>
          </div>
        </div>

        {/* Schedule & Semester Section */}
        <div className="section">
          <h2 className="section-title">Schedule & Semester</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="semester">
                Semester <span className="required">*</span>
              </label>
              <select id="semester" value={semester} onChange={(e)=>setSemester(e.target.value)}>
                <option value="">Select Semester</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start-date">
                Start Date <span className="required">*</span>
              </label>
              <input type="date" id="start-date" onChange={(e)=>setStartDate(e.target.value)} />
            </div>
            <div className="form-group">
              <label htmlFor="end-date">
                End Date <span className="required">*</span>
              </label>
              <input type="date" id="end-date" onChange={(e)=>setEndDate(e.target.value)} />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start-time">
                Start time <span className="required">*</span>
              </label>
              <input type="date" value={startTime} onChange={(e)=>setStartTime(e.target.value)} id="start-time" />
            </div>
            <div className="form-group">
              <label htmlFor="end-time">
                End time <span className="required">*</span>
              </label>
              <input type="date" id="end-time" value={endTime} onChange={(e)=>setEndTime(e.target.value)}  />
            </div>
          </div>
        </div>




        {/* Faculty & Prerequisites Section */}
        <div className="section">
          <h2 className="section-title">Faculty & Prerequisites</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="instructor">
                Instructor Assignment <span className="required">*</span>
              </label>
              <select id="instructor" value={instructor} onSelect={e=>setInstructor(e.target.value)}>
                <option value="">Select Instructor</option>
                <option value="dr-smith">Dr. Smith</option>
                <option value="prof-johnson">Prof. Johnson</option>
                <option value="dr-williams">Dr. Williams</option>
              </select>
            </div>


            <div className="form-group">
              <label htmlFor="room-assignment">Room Assignment</label>
              <input
                value={room}
                onChange={e=>setRoom(e.target.value)}
                type="text"
                id="room-assignment"
                placeholder="e.g., Building A - Room 101"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group full-width">
              <label>Prerequisites</label>
              {prerequisites.map((p, index) => (
                <div key={index} className="prerequisite-item">
                  <input
                    type="text"
                    value={p}
                    onChange={(e) => updatePrerequisite(index, e.target.value)}
                    placeholder="e.g., MATH 101 - College Algebra"
                  />
                  <button
                    type="button"
                    className="remove-button"
                    onClick={() => removePrerequisite(index)}
                  >
                    ×
                  </button>
                </div>
              ))}
              <button type="button" className="add-button" onClick={addPrerequisite}>
                + Add Prerequisite
              </button>
            </div>
          </div>
        </div>

        {/* Course Materials Section */}
        <div className="section">
          <h2 className="section-title">Course Materials</h2>

          <div className="form-row">
            <div className="form-group full-width">
              <label>Required Textbooks</label>
              {textbooks.map((book, index) => (
                <div key={index} className="textbook-row">
                  <input
                    type="text"
                    placeholder="Book Title"
                    value={book.title}
                    onChange={(e) => updateTextbook(index, "title", e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Author"
                    value={book.author}
                    onChange={(e) => updateTextbook(index, "author", e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="ISBN"
                    value={book.isbn}
                    onChange={(e) => updateTextbook(index, "isbn", e.target.value)}
                  />
                  <button
                    type="button"
                    className="remove-button"
                    onClick={() => removeTextbook(index)}
                  >
                    ×
                  </button>
                </div>
              ))}
              <button type="button" className="add-button" onClick={addTextbook}>
                + Add Textbook
              </button>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group full-width">
              <label htmlFor="additional-resources">Additional Resources</label>
              <textarea
                id="additional-resources"
                placeholder="List any additional resources..."
              />
            </div>
          </div>
        </div>

        {/* Form Actions */}
        <div className="form-actions">
          <div className="secondary-actions">
            <button type="button" className="btn btn-secondary">
              📄 Save as Draft
            </button>
            <button type="reset" className="btn btn-secondary">
              × Clear
            </button>
          </div>
          <button type="submit" className="btn btn-primary">
            Create Course
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewCourseForm;
