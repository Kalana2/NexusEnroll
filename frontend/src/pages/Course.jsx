


export default function Course({course , addToCart }){
    console.log(course);

    return <tr>
                <td>{course.id}</td>
                <td>{course.name}</td>
                <td>{course.instructor}</td>
                <td>{course.Schedule?.[0]} - {course.Schedule?.[1]} (Hall E)</td>
                <td>
                <span className="capacity limited">{course.total_capacity - course.current_enrollment} / {course.total_capacity}</span>
                </td>
                <td>{course.prerequisites?.join(',')}</td>
                <td>
                {/* <button className="btn small ghost">View Details</button> */}
                <br />
                <button className="btn small" onClick={()=>addToCart(course)}>Add to Cart</button>
                </td>
        </tr>
}