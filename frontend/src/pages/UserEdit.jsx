// src/pages/EditUser.jsx
import React, { useEffect, useState } from "react";
import "./createuser.scss";

const EditUser = ({onClick , appState , setAppState , user}) => {
  const [form, setForm] = useState({});

  useEffect(()=>{
    setForm((form)=>{
      return {...form,
        firstName: user.name,
        lastName: user.name,
        email: user.email,
        role: user.role,
        program: user.degree,
        department: user.department,
        password: user.password,
        confirmPassword: user.password,
        id:user.id,
    }})

  } , [user])


  const handleChange = (e) => {
    const { id, value } = e.target;
    setForm((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    setAppState(state=>{
      return {...state , user: state.users?.map(user=>user.id == form.id ? form : user )}
    })

    console.log("Form submitted:", form);
    alert("User saved successfully!");
  };

  return (
    <main className="main-content">
      <header className="header">
        <h1>Edit User</h1>
      </header>

      <section className="form-container">
        <form onSubmit={handleSubmit}>
          {/* Row 1 */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                placeholder="e.g., Alex"
                value={form.firstName}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                placeholder="e.g., Carter"
                value={form.lastName}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Row 2 */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                placeholder="name@university.edu"
                value={form.email}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="role">Role</label>
              <input type="text" id="role" value={form.role} readOnly />
            </div>
          </div>

          {/* Row 3 */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="program">Program (optional)</label>
              <select
                id="program"
                value={form.program}
                onChange={handleChange}
              >
                <option value="">Select program</option>
                <option value="cs">Computer Science</option>
                <option value="math">Mathematics</option>
                <option value="eng">Engineering</option>
                <option value="bus">Business</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="department">Department</label>
              <select
                id="department"
                value={form.department}
                onChange={handleChange}
              >
                <option value="">Select department</option>
                <option value="cs">CS</option>
                <option value="math">Math</option>
                <option value="eng">Engineering</option>
                <option value="bus">Business</option>
              </select>
            </div>
          </div>

          {/* Row 4 */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                placeholder="Confirm password"
                value={form.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Footer buttons */}
          <div className="footer-buttons">
            <button
              type="button"
              className="back"
              onClick={onClick}
            >
              Back
            </button>
            <button type="submit" className="continue" onClick={handleSubmit}>
              Save
            </button>
          </div>
        </form>
      </section>
    </main>
  );
};

export default EditUser;
