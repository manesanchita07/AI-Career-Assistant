const form = document.getElementById("profileForm");
const message = document.getElementById("message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const profile = {
        name: document.getElementById("name").value,
        education: document.getElementById("education").value,

        skills: document
            .getElementById("skills")
            .value
            .split(",")
            .map(skill => skill.trim()),

        interests: document
            .getElementById("interests")
            .value
            .split(",")
            .map(interest => interest.trim()),

        career_goal: document.getElementById("career_goal").value
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();

        if (response.ok) {
            message.textContent = "Profile created successfully! 🎉";
            form.reset();
        } else {
            message.textContent = "Something went wrong.";
            console.log(data);
        }

    } catch (error) {
        message.textContent = "Could not connect to the backend.";
        console.error(error);
    }
});