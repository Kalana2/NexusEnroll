
        function addPrerequisite() {
            const container = document.getElementById('prerequisites-container');
            const newPrereq = document.createElement('div');
            newPrereq.className = 'prerequisite-item';
            newPrereq.innerHTML = `
                <input type="text" placeholder="e.g., MATH 101 - College Algebra">
                <button type="button" class="remove-button" onclick="removePrerequisite(this)">×</button>
            `;
            container.appendChild(newPrereq);
        }

        function removePrerequisite(button) {
            button.parentElement.remove();
        }

        function addTextbook() {
            const container = document.getElementById('textbooks-container');
            const newTextbook = document.createElement('div');
            newTextbook.className = 'textbook-row';
            newTextbook.innerHTML = `
                <input type="text" placeholder="Book Title">
                <input type="text" placeholder="Author">
                <input type="text" placeholder="ISBN">
                <button type="button" class="remove-button" onclick="removeTextbook(this)">×</button>
            `;
            container.appendChild(newTextbook);
        }

        function removeTextbook(button) {
            button.parentElement.remove();
        }

        // Form validation and submission
        document.querySelector('.btn-primary').addEventListener('click', function(e) {
            e.preventDefault();
            
            // Basic validation
            const requiredFields = document.querySelectorAll('input[required], select[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    isValid = false;
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            if (isValid) {
                alert('Course created successfully!');
            } else {
                alert('Please fill in all required fields.');
            }
        });

        // Clear form
        document.querySelector('.btn-secondary:last-child').addEventListener('click', function() {
            if (confirm('Are you sure you want to clear all fields?')) {
                document.querySelector('form').reset();
            }
        });
  