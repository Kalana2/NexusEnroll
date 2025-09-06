// src/pages/Notifications.jsx
import React, { useState } from "react";
import "./notification.scss";

const Notifications = () => {
  const [notifications, setNotifications] = useState([
    {
      message:
        "NEW Course saved: Data Structures (CSCI-201) published successfully.",
      type: "System",
      time: "Just now",
      read: false,
    },
    {
      message: "Section capacity for CSCI-201 updated to 60 in two sections.",
      type: "Update",
      time: "5 min ago",
      read: false,
    },
    {
      message: "Instructor assigned: Dr. Maya Patel as Primary.",
      type: "Assignment",
      time: "12 min ago",
      read: false,
    },
    {
      message: "Catalog sync completed for Fall 2025.",
      type: "System",
      time: "1 hr ago",
      read: false,
    },
  ]);

  const markAllRead = () => {
    setNotifications(notifications.map((n) => ({ ...n, read: true })));
  };

  return (
    <div className="notification">
      <div className="main-content">
        {/* Header */}
        <div className="header">
          <h1 className="header-title">Notifications</h1>
          <div className="header-actions">
            <button className="header-btn primary" onClick={markAllRead}>
              Mark all as read
            </button>
          </div>
        </div>

        {/* Page content */}
        <div className="page-content">
          <div className="breadcrumbs">
            Administrator / <span>Notifications</span>
          </div>

          {/* Filters */}
          <div className="filter-bar">
            <div className="filter-item">
              <label className="filter-label">Filter</label>
              <input
                type="text"
                placeholder="Search notifications"
                className="filter-input search"
              />
            </div>
            <div className="filter-item">
              <label className="filter-label">Type: All</label>
              <select className="filter-select">
                <option>All</option>
                <option>System</option>
                <option>Update</option>
                <option>Assignment</option>
              </select>
            </div>
            <div className="filter-item">
              <label className="filter-label">Status: Unread</label>
              <select className="filter-select">
                <option>Unread</option>
                <option>Read</option>
                <option>All</option>
              </select>
            </div>
            <button className="more-filters-btn">search</button>
          </div>

          {/* Notifications Table */}
          <div className="notifications-table">
            <div className="table-header">
              <div className="table-cell">Message</div>
              <div className="table-cell">Type</div>
              <div className="table-cell">Time</div>
            </div>

            {notifications.map((n, index) => (
              <div
                key={index}
                className={`table-row ${n.read ? "read" : "unread"}`}
              >
                <div className="table-cell">
                  {!n.read && <strong>NEW </strong>}
                  {n.message}
                </div>
                <div className="table-cell">
                  <span className={`type-label type-${n.type.toLowerCase()}`}>
                    {n.type}
                  </span>
                </div>
                <div className="table-cell">{n.time}</div>
              </div>
            ))}
          </div>

          <div className="no-notifications">
            Only unread notifications are shown. Change Status to see all.
          </div>

          <button className="bottom-bar-btn primary">Back to Course</button>
        </div>
      </div>
    </div>
  );
};

export default Notifications;
