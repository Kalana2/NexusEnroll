function removeFromCart(setCart , setCourses , course){
    setCart(c=>c.filter(c=>c.name != course.name))
    setCourses(c=>[...c ,course]);
}

export default function Enrollment({course , setCart ,setCourses}){
    return <tr>
            <td>{course.name}</td>
            <td>{course.instructor}</td>
            <td>Mon/Wed 09:00–11:00</td>
            <td>
            <span className="status-tag green">Ready to Enroll</span>
            </td>
            <td>
            <button className="btn danger" onClick={()=>removeFromCart(setCart , setCourses , course)}>Remove</button>
            </td>
        </tr>
}



// <tr>
//     <td>MATH 310 — Linear Algebra</td>
//     <td>Prof. Nguyen</td>
//     <td>Tue/Thu 13:00–15:00</td>
//     <td>
//     <span className="status-tag orange">Pending Validation</span>
//     </td>
//     <td>
//     <button className="btn danger">Remove</button>
//     </td>
// </tr>
// <tr>
//     <td>ENG 102 — Composition II</td>
//     <td>Dr. Chen</td>
//     <td>Fri 09:00–11:30</td>
//     <td>
//     <span className="status-tag red">Time Conflict</span>
//     </td>
//     <td>
//     <button className="btn danger">Remove</button>
//     </td>
// </tr>