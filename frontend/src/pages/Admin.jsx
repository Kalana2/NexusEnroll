import { faSignIn } from "@fortawesome/free-solid-svg-icons";
import { CourseRepository } from './../patterns/repository/CourseRepository'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./admin.scss";
// import "./courseeditform.scss";
import { useMemo, useState } from "react";
import NewCourseForm from "./NewCourseForm";
import CreateUser from "./NewUser";
import EditUser from "./UserEdit";
// import "./courseform.css";
// import "./createuser.css";

export default function Admin({setRole,appState ,setAppState}){
    const [openNewCourseFrom , setOpenNewCourseForm] = useState(false);
    const [openCreateUserForm , setOpenCreateUserForm] = useState(false);
    const [openEditUserForm , setEditUserForm] = useState(false);
    const [user , setUser] = useState({});
    

    function deleteUser(d_user){
        setAppState(state=>{
            return {...state , users : appState.users.filter(user=>user.id != d_user.id)};
        })
    }


  
    if(openNewCourseFrom){
        return <NewCourseForm onClick={()=>setOpenNewCourseForm(false)}  />
    }
    if(openCreateUserForm){
        return <CreateUser onClick={()=>setOpenCreateUserForm(false)}  appState={appState} setAppState={setAppState}/>
    }
    if(openEditUserForm){
        return <EditUser onClick={()=>setEditUserForm(false)}  appState={appState} setAppState={setAppState} user={user} />
    }



    return <>
    <div class="container admin">
        <aside class="sidebar" style={{zIndex:100 ,maxWidth:'250px'}}>
            <div class="sidebar-header">
                <img src="/src/img/logo.png" />
                <h1 class="sidebar-brand">NexusEnroll</h1>
            </div>

            <nav class="sidebar-nav">
                <div class="sidebar-section-title">Administration</div>
                <ul>
                <li class="nav-item">
                    <img src="/src/img/course.png" />
                    Courses
                </li>
                
                <li class="nav-item" tabindex="0">
                <img src="/src/img/user.png" />
                    Users
                </li>
                <li class="nav-item" tabindex="0">
                    <img src="/src/img/report.png" />
                    Reports
                </li>
                <li onClick={()=>setRole(false)} className="nav-item" tabIndex={0} style={{color : "#f25757" }}>
                    <FontAwesomeIcon icon={faSignIn} />
                        log out
                </li>
                
                </ul>
            </nav>

            <div class="sidebar-profile">
                <img src="https://i.pravatar.cc/40?img=23" alt="Alex Morgan" class="profile-pic" />
                <div class="profile-details">
                <span class="profile-name">Alex Morgan</span>
                <span class="profile-role">Administrator</span>
                </div>
            </div>
        </aside>

        <main class="main-content">
            <header class="main-header">
            <div class="header-actions">
                
                <button onclick="window.location.href='notification.html'" class="btn notif-btn"  title="Notifications"> <img src="/src/img/notification.png" /></button>
            
            </div>
            <div class="search-container">
            
                    <input id="search" type="search" placeholder="Search courses" autocomplete="off" />
                    <button class="btn sync-btn" title="search">Search</button>
            </div>
            </header>
    
            <div class ="course">     
                <div class="table-actions">
                <button class="btn new-course-btn"onclick="window.location.href='courseform.html'" onClick={()=>setOpenNewCourseForm(true)}>+ New Course</button>
                
                </div>

                <table class="courses-table" role="grid" aria-labelledby="tab-courses">
                <thead>
                    <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Course</th>
                    <th scope="col">Instructor</th>
                    <th scope="col">Schedule</th>
                    <th scope="col">Capacity</th>
                    <th scope="col" aria-label="Actions"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>CS101</td>
                    <td>Intro to CS</td>
                    <td>Dr. Lee</td>
                    <td>Mon/Wed 10:00</td>
                    <td><span class="capacity-label green">24/30</span></td>
                    <td><button onclick="window.location.href='courseeditform.html'" class="btn small-btn">Edit</button></td>
                    <td><button onclick="confirmDelete()" class="btn small-btn2">Delete</button></td>
                    </tr>
                    <tr>
                    <td>MATH210</td>
                    <td>Linear Algebra</td>
                    <td>Prof. Singh</td>
                    <td>Tue/Thu 09:00</td>
                    <td><span class="capacity-label orange">30/30</span></td>
                    <td><button onclick="window.location.href='courseeditform.html'" class="btn small-btn">Edit</button></td>
                    <td><button onclick="confirmDelete()" class="btn small-btn2">Delete</button></td>
                    </tr>
                    <tr>
                    <td>BIO120</td>
                    <td>Molecular Biology</td>
                    <td>Dr. Park</td>
                    <td>Mon 14:00</td>
                    <td><span class="capacity-label gray" title="Waitlist 5">Waitlist 5</span></td>
                    <td><button onclick="window.location.href='courseeditform.html'" class="btn small-btn">Edit</button></td>
                    <td><button onclick="confirmDelete()" class="btn small-btn2">Delete</button></td>
                    </tr>
                </tbody>
                </table>

                <div class="pagination" role="navigation" aria-label="Pagination">
                <div class="pagination-info">Showing 1-{appState?.users?.length} of {appState?.users?.length} </div>
                {/* <div class="pagination-controls">
                    <button class="btn small-btn3" aria-label="Previous Page">← Previous</button>
                    <button class="btn small-btn3" aria-label="Next Page">Next →</button>
                </div> */}
                </div>

            </div>
                
            <div class="users">
                <header class="main-header">

            <div class="search-container">
            
                    <input id="search" type="search" placeholder="Search users" autocomplete="off" />
                    <button class="btn sync-btn" title="search">Search</button>
            </div>
            </header>

            <div class ="course">     
                <div class="table-actions">
                <button onclick="window.location.href='createuser.html'" onClick={()=>setOpenCreateUserForm(true)} class="btn new-course-btn">+ New user</button>
                
                </div>

                <table class="courses-table" role="grid" aria-labelledby="tab-courses">
                <thead>
                    <tr>
                    <th scope="col">User ID</th>
                    <th scope="col">Full Name</th>
                    <th scope="col">Email Address</th>
                    <th scope="col">Phone Number</th>
                    <th scope="col">Program/ Degree</th>
                    <th scope="col" aria-label="Actions"></th>
                    </tr>
                </thead>
                <tbody>
                    {
                        appState?.users?.map((user , key)=>{
                            return <tr key={key}>
                                <td>{user.id}</td>
                                <td>{user.name}</td>
                                <td>{user.email}</td>
                                <td>{user.phone}</td>
                                <td>{user.program}</td>
                                <td><button  onClick={()=>{setUser(user); setEditUserForm(true)}} class="btn small-btn">Edit</button></td>
                                <td><button  onClick={()=>deleteUser(user)} class="btn small-btn21">Delete</button></td>
                                </tr>
                        })
                    }
                </tbody>
                </table>




        <div id="deleteModal" class="modal">
            <div class="modal-content">
                <h3>Confirm Delete</h3>
                <p>Are you sure you want to delete?</p>
                <p>This action cannot be undone.</p>
                <div class="modal-buttons">
                    <button class="btn btn-confirm" onclick="executeDelete()">Delete</button>
                    <button class="btn btn-cancel" onclick="cancelDelete()">Cancel</button>
                </div>
            </div>
        </div>












                <div class="pagination" role="navigation" aria-label="Pagination">
                <div class="pagination-info">Showing 1-3 of 128</div>
                <div class="pagination-controls">
                    <button class="btn small-btn3" aria-label="Previous Page">← Previous</button>
                    <button class="btn small-btn3" aria-label="Next Page">Next →</button>
                </div>
                </div>

                </div>

                        
            </div>





            <section class="reports-analytics" aria-label="Reports and Analytics">
            <h3 class="section-title">Reports &amp; Analytics</h3>

            <form class="report-filters">


                <label for="report-select">Report</label>
                <select name="reprtType" required>
                    <option value="" selected disabled>Select report type</option>
                    <option value="enrolmentreport">Enrolment statistics by department and semester</option>
                    <option value="workloadreport">Faculty workload reports</option>
                    <option value="popularityreport">Course popularity trends</option>
                </select>



                <label for="report-select">Course code </label>
                <select name="reprtType" required>
                    <option value="" selected disabled>Select course </option>
                    <option value="enrolmentreport">SCS101</option>
                    <option value="workloadreport">BIO120</option>
                    <option value="popularityreport">CS101</option>
                </select>
                
                <button class="btn sync-btn" title="search">Search</button>

            </form>

            <h2 class="sub-section-title">Enrolment statistics by department and semester</h2>
            <table class="reports-table" role="grid">
                <thead>
                <tr>
                    <th scope="col">Dept</th>
                    <th scope="col">Course</th>
                    <th scope="col">Enrolled</th>
                    <th scope="col">Capacity</th>
                    <th scope="col">Utilization</th>
                    <th scope="col">Status</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>CS</td>
                    <td>CS101</td>
                    <td>24</td>
                    <td>30</td>
                    <td><span class="utilization-label green-bg">80%</span></td>
                    <td>Stable</td>
                </tr>
                <tr>
                    <td>Math</td>
                    <td>MATH210</td>
                    <td>30</td>
                    <td>30</td>
                    <td><span class="utilization-label orange-bg">100%</span></td>
                    <td>Full</td>
                </tr>
                </tbody>
            </table>

            <h2 class="sub-section-title">Faculty workload reports</h2>

            <table class="reports-table" role="grid">
                <thead>
                <tr>
                    <th scope="col">Department</th>
                    <th scope="col">No. of Faculty</th>
                    <th scope="col">Avg. Teaching Hours</th>
                    <th scope="col">Avg. Research Hours</th>
                    <th scope="col">Avg. Admin Hours</th>
                    <th scope="col">Total Hours/Week</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>Computer Science</td>
                    <td>15</td>
                    <td>12</td>
                    <td>6</td>
                    <td>2</td>
                    <td>20</td>
                </tr>
                <tr>
                    <td>Electrical Engineering</td>
                    <td>12</td>
                    <td>30</td>
                    <td>3</td>
                    <td>2</td>
                    <td>20</td>
                </tr>
                </tbody>
            </table>

            <h2 class="sub-section-title">Course popularity trends</h2>

        </section>
        <section class="card">
        <h1 h1>Top 5 Most Popular Courses</h1>
            <table class="reports-table" role="grid">
    <thead>
        <tr>
        <th scope="col">Rank</th>
        <th scope="col">Course Code</th>
        <th scope="col">Course Title</th>
        <th scope="col">Department</th>
        <th scope="col">Enrolled Students</th>
        <th scope="col">Percentage of Total</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>1</td>
        <td>CS101</td>
        <td>Introduction to Programming</td>
        <td>Computer Science</td>
        <td>320</td>
        <td>5.4%</td>
        </tr>
        <tr>
        <td>2</td>
        <td>BA201</td>
        <td>Principles of Management</td>
        <td>Business Admin.</td>
        <td>295</td>
        <td>5.0%</td>
        </tr>
        <tr>
        <td>3</td>
        <td>IT205</td>
        <td>Web Development</td>
        <td>Information Tech.</td>
        <td>280</td>
        <td>4.7%</td>
        </tr>
        <tr>
        <td>4</td>
        <td>EE210</td>
        <td>Digital Electronics</td>
        <td>Electrical Eng.</td>
        <td>265</td>
        <td>4.5%</td>
        </tr>
        <tr>
        <td>5</td>
        <td>MTH110</td>
        <td>Calculus I</td>
        <td>Mathematics</td>
        <td>250</td>
        <td>4.2%</td>
        </tr>
    </tbody>
            </table>
        </section>

        <div class="grid-2">
        <section class="card">
            <h1>Least Popular Courses </h1>
            <table class="reports-table" role="grid">
                <thead>
                    <tr>
                    <th scope="col">Course Code</th>
                    <th scope="col">Course Title</th>
                    <th scope="col">Department</th>
                    <th scope="col">Enrolled Students</th>
                    
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>ME315</td>
                    <td>Thermodynamics II</td>
                    <td>Mechanical Eng.</td>
                    <td>45</td>
                    
                    </tr>
                    <tr>
                    <td>BA330</td>
                    <td>Business Law</td>
                    <td>Business Admin.</td>
                    <td>50</td>
                    </tr>
                </tbody>
                </table>
        </section>

        <section class="card">
            <h1>Course Popularity Trends </h1>
            <table class="reports-table" role="grid">
            <thead>
                <tr>
                <th>Course Code</th>
                <th>2022–2023</th>
                <th>2023–2024</th>
                <th>2024–2025</th>
                <th>Trend</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>CS101</td>
                <td>250</td>
                <td>285</td>
                <td>320</td>
                <td>📈 Rising</td>
                </tr>
                <tr>
                <td>IT205</td>
                <td>180</td>
                <td>230</td>
                <td>280</td>
                <td>📈 Rising</td>
                </tr>
                <tr>
                <td>EE210</td>
                <td>270</td>
                <td>260</td>
                <td>265</td>
                <td>➡️ Stable</td>
                </tr>
                <tr>
                <td>ME315</td>
                <td>70</td>
                <td>58</td>
                <td>45</td>
                <td>📉 Falling</td>
                </tr>
                <tr>
                <td>BA201</td>
                <td>280</td>
                <td>290</td>
                <td>295</td>
                <td>➡️ Stable</td>
                </tr>
            </tbody>
            </table>
        </section>
        </div>
        </main>
    </div>
</>
}