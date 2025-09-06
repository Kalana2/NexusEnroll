import { useEffect, useState } from "react";
import "./student.scss";
import Course from "./Course";
import Enrollment from "./Entrollment";
import { toast, ToastContainer } from "react-toastify"
import { Element, Link } from "react-scroll";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBook, faSignIn, faTrophy } from "@fortawesome/free-solid-svg-icons";
import { faCalendar } from "@fortawesome/free-regular-svg-icons";
import { useMemo } from "react";





async function getCourses(setCourses){
    const respond = await fetch("http://localhost:8002/courses" , {
        method:"GET"
    })
    const data = await respond.json();
    if(data){
        setCourses(c=>[...c,...data])
    }

}

function notify({course ,msg}){
    if(msg) return toast(msg);

    return toast(course.name + " added to the Cart");
}



const Student = ({setRole ,appState ,setAppState}) => {
        const [cart , setCart] = useState([]);
        const [courses , setCourses] = useState([]);
        const [filters, setFilters] = useState({
            department: "",
            courseName: "",
            instructor: "",
            semester: "",
            keyword: "",
        });


        // inside Student component
        const filteredCourses = useMemo(() => {
        return appState.courses.filter((course) => {
            return (
            (filters.department === "" ||
                course.department
                ?.toLowerCase()
                .includes(filters.department.toLowerCase())) &&
            (filters.courseName === "" ||
                course.id?.toLowerCase().includes(filters.courseName.toLowerCase()) ||
                course.name?.toLowerCase().includes(filters.courseName.toLowerCase())) &&
            (filters.instructor === "" ||
                course.instructor
                ?.toLowerCase()
                .includes(filters.instructor.toLowerCase())) &&
            (filters.semester === "" ||
                course.semester
                ?.toLowerCase()
                .includes(filters.semester.toLowerCase())) &&
            (filters.keyword === "" ||
                course.keywords?.some((kw) =>
                kw.toLowerCase().includes(filters.keyword.toLowerCase())
                ))
            );
        });
        }, [filters, appState.courses]);


        // const [filter , setFilter] = useState({})

    useEffect(()=>{
        getCourses(setCourses)
    },[])

    // useEffect(()=>{
    //     //checkfor time confict
    //     cart.forEach(c=>{
    //         cart.forEach(t=>{
    //             if(c.schedule == t.schedule){
    //                 c.status = "conflict";
    //                 t.status = "conflict";
    //                 notify({msg:c.name + " has time conflict"});
    //                 notify({msg:t.name + " has time conflict"});
    //             }
    //         })
    //     })
    // },[cart])

    function addToCart(course){
        setCourses(courses.filter(c=>c.name != course.name));
        setCart(c=>[...c , course]);
        notify({course});
    }

    return (
        <div className="student-page student">
        <ToastContainer />
        <aside className="sidebar">
            <div className="sidebar-header">
            <img src="/src/img/logo.png" alt="NexusEnroll logo" />
            <h1 className="sidebar-brand">NexusEnroll</h1>
            </div>

            <nav className="sidebar-nav">
            <div className="sidebar-section-title">Student</div>
            <ul>
                <Link to="catalogue">
                    <li className="nav-item">
                        <img src="/src/img/course.png" alt="Courses" />
                        Courses
                    </li>
                </Link>

                <Link to="enrollment">
                    <li className="nav-item" tabIndex={0}>
                    <FontAwesomeIcon icon={faBook} />
                        Enrollment
                    </li>
                </Link>
                <Link to="schedule">
                    <li className="nav-item" tabIndex={0}>
                    <FontAwesomeIcon icon={faCalendar} />
                        Schedule
                    </li>
                </Link>
                <Link to="progress">
                    <li className="nav-item" tabIndex={0}>
                    <FontAwesomeIcon icon={faTrophy} />
                        progress
                    </li>
                </Link>
                    <li onClick={()=>setRole(false)} className="nav-item" tabIndex={0} style={{color : "#f25757" }}>
                    <FontAwesomeIcon icon={faSignIn} />
                        log out
                    </li>
            </ul>
            </nav>

            <div className="sidebar-profile">
            <img
                src="#"
                alt="Profile"
                className="profile-pic"
            />
            <div className="profile-details">
                <span className="profile-name">chathura priyashan</span>
                <span className="profile-role">Student</span>
            </div>
            </div>
        </aside>

        <main className="main-content">
            {/* Top bar */}
            <header className="top-bar">
            <input
                type="text"
                name="search"
                placeholder="Search courses, instructors, or keywords"
            />
            <button className="btn btn-primary">Search</button>
            </header>

            <Element name="catalogue" >
            {/* Catalogue & Filters */}
            <section className="catalogue-wrap">
            <div className="card filters">
                <h3>Filters</h3>
                <label className="field-label">Department</label>
                <input type="text" value={filters.department} onChange={(e)=>setFilters((s)=>{return {...s , department: e.target.value}})} name="department" placeholder="e.g., CS, MATH" />

                <label className="field-label">Course Number</label>
                <input type="text" name="id" value={filters.courseName} onChange={(e)=>setFilters((s)=>{return {...s , courseName: e.target.value}})} placeholder="e.g., 101" />

                <label className="field-label">Keyword</label>
                <input type="text" name="keyword" value={filters.courseName} onChange={(e)=>setFilters((s)=>{return {...s , courseName: e.target.value}})} placeholder="databases, AI" />

                <label className="field-label">Instructor</label>
                <input type="text" name="instructor" value={filters.instructor} onChange={(e)=>setFilters((s)=>{return {...s , instructor: e.target.value}})} placeholder="Name" />

                <label className="field-label">Semester</label>
                <input type="text" name="semester" value={filters.semester} onChange={(e)=>setFilters((s)=>{return {...s , semester: e.target.value}})} placeholder="Fall 2025" />

                <label className="field-label">Status</label>
                {/*<div className="status-options">
                 <label>
                    <input type="checkbox" name="open" /> Open
                </label>
                <label>
                    <input type="checkbox" name="waitlist" /> Waitlist
                </label>
                <label>
                    <input type="checkbox" name="full" /> Full
                </label>
                </div> */}

                {/* <div className="filters-actions">
                <button className="btn reset">Reset</button>
                <button className="btn apply">Apply</button>
                </div> */}
            </div>

            <section className="card course-catalogue">
                <h3>Course Catalogue</h3>
                <table>
                <thead>
                    <tr>
                    <th>ID</th>
                    <th>Course Name</th>
                    <th>Instructor</th>
                    <th>Schedule</th>
                    <th>Capacity</th>
                    <th>Prerequisites</th>
                    <th>Actions</th>
                    </tr>
                </thead>
                <tbody className="course_list">
                {filteredCourses?.map((c , i)=> <Course addToCart={addToCart} key={i} course={c}/>)}
                </tbody>
                </table>
            </section>
            </section>
            </Element>

            {/* Registration */}
            <Element name="enrollment">

            <section className="card registration">
            <div className="section-head">
                <h3>Registration & Enrollment</h3>
                <button className="btn primary">Proceed to Enrollment</button>
            </div>
            <table>
                <thead>
                <tr>
                    <th>Course</th>
                    <th>Instructor</th>
                    <th>Schedule</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody id="enrollment-list">
                    {cart.map((course , index)=><Enrollment key={index} setCart={setCart} setCourses={setCourses} course={course} />)}


                </tbody>
            </table>
            </section>
            </Element>


            {/* Schedule */}
            <Element name="schedule" >
            <section className="card schedule">
            <h3>Schedule</h3>
            <div className="tabs">
                <button className="tab-btn active">Current Semester</button>
                <button className="tab-btn">Past Semesters</button>
            </div>

            <div id="current" className="schedule-container">
                <table className="timetable">
                <thead>
                    <tr>
                    <th>Time</th>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>09:00–11:00</td>
                    <td>CS 201</td>
                    <td>CS 205</td>
                    <td>CS 201</td>
                    <td>CS 205</td>
                    <td>ENG 102</td>
                    </tr>
                    <tr>
                    <td>11:00–13:00</td>
                    <td>HIST 150</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    </tr>
                    <tr>
                    <td>13:00–15:00</td>
                    <td></td>
                    <td>MATH 310</td>
                    <td></td>
                    <td>MATH 310</td>
                    <td></td>
                    </tr>
                </tbody>
                </table>
            </div>

            <div id="past" className="schedule-container" style={{ display: "none" }}>
                <table className="timetable">
                <thead>
                    <tr>
                    <th>Time</th>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>09:00–11:00</td>
                    <td></td>
                    <td>MATH 201</td>
                    <td></td>
                    <td>CS 101</td>
                    <td></td>
                    </tr>
                    <tr>
                    <td>11:00–13:00</td>
                    <td>CS 101</td>
                    <td></td>
                    <td>ENG 101</td>
                    <td></td>
                    <td>CS 101</td>
                    </tr>
                    <tr>
                    <td>13:00–15:00</td>
                    <td>CS 201</td>
                    <td>MATH 201</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    </tr>
                </tbody>
                </table>
            </div>
            </section>
            </Element>

            {/* Progress */}
            <Element name="progress">

            <section className="card progress">
            <h3>Academic Progress</h3>
            <table>
                <thead>
                <tr>
                    <th>Course</th>
                    <th>Course Name</th>
                    <th>Semester</th>
                    <th>Grade</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>CS 101</td>
                    <td>Intro to CS</td>
                    <td>Fall 2024</td>
                    <td>A</td>
                </tr>
                <tr>
                    <td>ENG 101</td>
                    <td>Composition I</td>
                    <td>Spring 2024</td>
                    <td>B+</td>
                </tr>
                </tbody>
            </table>

            <div className="progress-title">Degree Requirements</div>
            <p>Overall Progress:</p>
            <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: "40%" }}>
                48/120
                </div>
            </div>
            <p>Core CS Credits:</p>
            <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: "70%" }}>
                7/10
                </div>
            </div>
            <p>Math Requirements:</p>
            <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: "50%" }}>
                2/4
                </div>
            </div>
            <p>Writing Intensive:</p>
            <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: "100%" }}>
                3/3
                </div>
            </div>
            </section>

            </Element>

        </main>
        </div>
    );
    };

    export default Student;
