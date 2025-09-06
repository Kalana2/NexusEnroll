import supabase from "../supabase.js";

const courseData = {
    courses : []
}


export async function fetchCourses(){

    let { data: courses, error } = await supabase
    .from('courses')
    .select('id');

    console.log(data);


    const respond =await fetch("http://localhost:8002/courses" , {
        credentials:'same-origin'
    });
    const data = await respond.json()
    data?.forEach(d=>courseData.courses.push(d));
    return data;
}

export function filterCourses(filter) {
    console.log(filter , courseData.courses)

    const filtered  = courseData.courses.filter(course => {
    // For each filter condition, check if course satisfies it
        return Object.entries(filter).every(([key, value]) => {
            if (!value) return true; // Skip empty filters

            const field = course[key];

            if (Array.isArray(field)) {
            // If the field is an array, check if it contains the value
                return field.some(item => 
                    String(item).toLowerCase().includes(String(value).toLowerCase())
                );
            }

            if (typeof field === "string") {
            // Case-insensitive search for strings
                return field.toLowerCase().includes(String(value).toLowerCase());
            }

            if (typeof field === "number") {
                // Exact match for numbers
                return field === Number(value);
            }

            return false; // If no match
        });
    });

    console.log(filtered)
    return filtered;
}
