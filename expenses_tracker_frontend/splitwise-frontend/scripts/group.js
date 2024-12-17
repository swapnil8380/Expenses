document.getElementById("groupForm").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    const groupName = document.getElementById("groupName").value;
    const usernamesInput = document.getElementById("groupUsernames").value;
  
    // Convert comma-separated usernames into an array
    const usernames = usernamesInput.split(",").map(name => name.trim());
  
    // Retrieve the access token from local storage
    const accessToken = localStorage.getItem("access_token");
  
    if (!accessToken) {
      document.getElementById("responseMessage").textContent = "You need to login first!";
      return;
    }
  
    try {
      const response = await fetch("http://192.168.56.101:5001/groups", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ name: groupName, usernames }),
      });
  
      const data = await response.json();
      if (response.ok) {
        document.getElementById("responseMessage").textContent = `Group created with ID: ${data.group_id}`;
        window.location.href = "expenses.html";

      } else {
        document.getElementById("responseMessage").textContent = data.error || "Failed to create group!";
      }
    } catch (error) {
      document.getElementById("responseMessage").textContent = "An error occurred: " + error.message;
    }
  });
  