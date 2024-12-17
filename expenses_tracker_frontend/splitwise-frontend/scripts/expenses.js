document.getElementById("expenseForm").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    const groupId = document.getElementById("groupId").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const usernamesInput = document.getElementById("expenseUsernames").value;
    const description = document.getElementById("description").value;
  
    // Convert comma-separated usernames into an array
    const usernames = usernamesInput.split(",").map(name => name.trim());
    
  
    // Retrieve the access token from local storage
    const accessToken = localStorage.getItem("access_token");
  
    if (!accessToken) {
      document.getElementById("responseMessage").textContent = "You need to login first!";
      return;
    }
  
    try {
      const response = await fetch("http://192.168.56.101:5001/expenses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ group_id: groupId, amount, usernames, description }),
      });
  
      const data = await response.json();
      if (response.ok) {
        document.getElementById("responseMessage").textContent = data.message;
        window.location.href = "summary.html";
      } else {
        document.getElementById("responseMessage").textContent = data.msg || "Failed to add expense!";
      }
    } catch (error) {
      document.getElementById("responseMessage").textContent = "An error occurred: " + error.message;
    }
  });
  
   