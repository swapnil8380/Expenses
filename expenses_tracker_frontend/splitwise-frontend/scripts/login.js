document.getElementById("loginForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://192.168.56.101:5001/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    // Check if response is successful
    if (response.ok) {
      const data = await response.json();
      console.log(data);

      // Save the access token in local storage
      localStorage.setItem("access_token", data.access_token);

      // Display success message and redirect to the dashboard
      document.getElementById("responseMessage").textContent = "Login successful!";
      window.location.href = "dashboard.html";
      
    } else {
      const data = await response.json();
      console.log(data); // Log any additional info for debugging
      document.getElementById("responseMessage").textContent = data.error || "Login failed!";
    }
  } catch (error) {
    // Log the error to the console and display a message to the user
    console.error("Error during login:", error);
    document.getElementById("responseMessage").textContent = "An error occurred: " + error.message;
  }
});
