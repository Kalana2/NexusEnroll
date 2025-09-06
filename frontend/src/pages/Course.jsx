


export default function Course({course , addToCart }){
        
    return <tr>
                <td>{course?.id}</td>
                <td>{course?.name}</td>
                <td>{course?.instructor}</td>
                <td>{course?.Schedule?.[0]} - {course?.schedule}</td>
                <td>
                <span className="capacity limited">{course?.capacity.total - course?.capacity.enrolled} / {course.capacity.total}</span>
                </td>
                <td>{course?.prerequisites?.join(',')}</td>
                <td>
                {/* <button className="btn small ghost">View Details</button> */}
                <br />
                <button className="btn small" onClick={()=>addToCart(course)}>Add to Cart</button>
                </td>
        </tr>
}