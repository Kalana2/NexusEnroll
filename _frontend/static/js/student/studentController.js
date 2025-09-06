import { fetchCourses, filterCourses } from "./studentModel.js";
import { renderCourseList } from "./studentView.js";


document.addEventListener('click' , (e)=>{
    const target = e.target;
    const addToCardButton = target.closest('button');
    const filterApplyBtn = target.closest('button.apply');

    if(filterApplyBtn){
        const filter = {};
        const filterForm = document.querySelector('.card.filters');
        const filterInputs = filterForm.querySelectorAll('input');
        filterInputs.forEach(i=>filter[i.getAttribute('name')] = i.value);


        
        const filteredCourses = filterCourses(filter);

        
        renderCourseList(filteredCourses);
    }



    
    

})


fetchCourses().then(data=>renderCourseList(data));
