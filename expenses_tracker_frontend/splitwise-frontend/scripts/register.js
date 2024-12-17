document.getElementById("registerForm").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const mobile_no = document.getElementById("mobile_no").value;
  
    try {
      const response = await fetch("http://192.168.56.101:5001/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, mobile_no, password}),
      });

      if (response.ok) {
        const data = await response.json();
        document.getElementById("responseMessage").textContent = "User registered successfully!";
        window.location.href = "dashboard.html"; }
      else {
        const data = await response.json();
        console.log(data); // Log any additional info for debugging
        document.getElementById("responseMessage").textContent = data.error || "Registration failed!";
    } 
    } catch(error) {
      document.getElementById("responseMessage").textContent = "An error occurred: " + error.message;
    }
  });
  