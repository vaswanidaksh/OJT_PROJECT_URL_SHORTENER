// Handle navbar clicks and show corresponding section
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        
        // Get the target section from the data attribute
        const targetSection = this.getAttribute('data-target');
        
        // Hide all sections and their content
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Show the target section
        document.getElementById(targetSection).classList.add('active');
        
        // If it's the Home page, show the form and the welcome text
        if (targetSection === "home") {
            document.querySelector('.form-container').style.display = "block";
            document.querySelector('.home-content').style.display = "block"; // Show the welcome text
        } else {
            document.querySelector('.form-container').style.display = "none"; // Hide the form
            document.querySelector('.home-content').style.display = "none"; // Hide the welcome text
        }
    });
});

// Shorten Me button functionality (same as Home button)
document.querySelector('#shorten-me-btn').addEventListener('click', function() {
    const formContainer = document.querySelector('.form-container');
    const homeContent = document.querySelector('.home-content');
    
    // Show the Home content (text and form) when "Shorten Me" is clicked
    formContainer.style.display = "block";
    homeContent.style.display = "block";
    
    // Ensure that the Home section is active when "Shorten Me" is clicked
    document.getElementById('home').classList.add('active');
    
    // Hide all other sections
    document.querySelectorAll('.section').forEach(section => {
        if (section.id !== "home") {
            section.classList.remove('active');
        }
    });
});

// The Generate button will now simply clear the input field and show a success message
document.querySelector('#generate-btn').addEventListener('click', function() {
    const urlInput = document.querySelector('#url-input').value.trim();  // Get the value of the input field

    if (urlInput === "") {
        alert("Please enter a valid URL.");
        return;
    }

    // If a valid URL is entered, show a success message
    alert("URL has been shortened!"); // Placeholder confirmation message

    // Optionally, clear the input field after clicking Generate
    document.querySelector('#url-input').value = '';
});
