function showSchedule(tab) {
  document.getElementById('current').style.display = (tab === 'current') ? 'block' : 'none';
  document.getElementById('past').style.display = (tab === 'past') ? 'block' : 'none';
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
}


const courseContainer = document.querySelector('tbody.course_list');


export function renderCourseList(courseList=[]){
  const courseTemplate = `
  <tr>
    <td>%%ID%%</td>
    <td>%%NAME%%</td>
    <td>%%INSTRUCTOR%%</td>
    <td>%%SCHEDULE%%</td>
    <td><span class="capacity limited">%%REMAIN%% / %%CAPACITY%%</span></td>
    <td>%%HALL%%</td>
    <td>
      <button class="btn small ghost">View Details</button><br />
      <button class="btn small add-to-card" data-course="%%ID%%" >Add to Cart</button>
    </td>
  </tr>`;

  courseContainer.innerHTML = ' ';

  const courses = courseList.map(course=>{
    return courseTemplate
      .replaceAll('%%ID%%' , course.id)
      .replaceAll('%%NAME%%' , course.name)
      .replaceAll('%%INSTRUCTOR%%' , course.instructor)
      .replaceAll('%%SCHEDULE%%' , course.schedule)
      .replaceAll('%%CAPACITY%%' , course.total_capacity)
      .replaceAll('%%HALL%%' , course.name)
      .replaceAll('%%REMAIN%%' ,course.total_capacity - course.current_enrollment)
      ;
  })


  courseContainer.insertAdjacentHTML('beforeend' , courses.join(' '))



}



