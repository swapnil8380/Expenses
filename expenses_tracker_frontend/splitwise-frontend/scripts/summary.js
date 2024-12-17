document.getElementById("fetchSummary").addEventListener("click", async function () {
    // Retrieve the access token from local storage
    const accessToken = localStorage.getItem("access_token");
  
    if (!accessToken) {
      alert("You need to log in first!");
      return;
    }
  
    try {
      const response = await fetch("http://192.168.56.101:5001/expenses/summary", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
      });
  
      const data = await response.json();
  
      if (response.ok) {
        displaySummary(data);
      } else {
        document.getElementById("summaryData").innerHTML = `<p>Error: ${data.msg || "Failed to fetch summary!"}</p>`;
      }
    } catch (error) {
      document.getElementById("summaryData").innerHTML = `<p>An error occurred: ${error.message}</p>`;
    }
  });
  
  function displaySummary(summary) {
    const summaryContainer = document.getElementById("summaryData");
    summaryContainer.innerHTML = `
      <div class="summary-card">
        <p><strong>Total Spent:</strong> ₹${summary.total_spent}</p>
        <p><strong>Total Owed:</strong> ₹${summary.total_owned}</p>
        <p><strong>Amount Owed to Me:</strong> ₹${summary.amount_owed_to_me}</p>
        <p><strong>Amount Owed by Me:</strong> ₹${summary.amount_owed}</p>
      </div>
      <div class="details-container">
        <h3>Details</h3>
        <div>
          <h4>Owed to Me:</h4>
          <ul>${summary.owed_to_me.map(user => `<li>${user}</li>`).join("")}</ul>
        </div>
        <div>
          <h4>Owed to Others:</h4>
          <ul>${summary.owed_to_others.map(user => `<li>${user}</li>`).join("")}</ul>
        </div>
      </div>
    `;
  }
  

   // Back to Dashboard Button
   document.getElementById("backToDashboardBtn").addEventListener("click", () => {
    window.location.href = "dashboard.html";
  });