// src/pages/CreateUser.jsx
import React, { useState } from "react";
import "./createuser.scss";

const CreateUser = () => {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    role: "Student / Faculty / Administrator",
    program: "",
    department: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setForm((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    // Prepare new user object
    const newUser = {
      name: `${form.firstName} ${form.lastName}`,
      email: form.email,
      role: form.role,
      program: form.program,
      department: form.department,
      password: form.password,
    };

    try {
      const res = await fetch("http://localhost:3000/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });

      if (!res.ok) throw new Error("Failed to create user");

      alert("User created successfully!");
      setForm({
        firstName: "",
        lastName: "",
        email: "",
        role: "Student / Faculty / Administrator",
        program: "",
        department: "",
        password: "",
        confirmPassword: "",
      });
    } catch (err) {
      console.error(err);
      alert("Error creating user");
    }
  };

  return (
    <main className="main-content create-user">
      <header className="header">
        <h1>Create New User</h1>
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
              onClick={() => alert("Going back...")}
            >
              Back
            </button>
            <button type="submit" className="continue">
              Save
            </button>
          </div>
        </form>
      </section>
    </main>
  );
};

export default CreateUser;
