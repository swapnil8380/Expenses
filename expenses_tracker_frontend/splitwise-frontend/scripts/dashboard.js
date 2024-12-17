document.addEventListener("DOMContentLoaded", () => {
  const accessToken = localStorage.getItem("access_token");

  // Redirect to login if not authenticated
  if (!accessToken) {
    alert("Please log in first.");
    window.location.href = "login.html";
    return;
  }

  // Event listeners for dashboard actions
  document.getElementById("createGroupBtn").addEventListener("click", () => {
    window.location.href = "groups.html";
  });

  document.getElementById("viewGroupsBtn").addEventListener("click", () => {
    window.location.href = "get_groups.html";
  });

  document.getElementById("addExpenseBtn").addEventListener("click", () => {
    window.location.href = "expenses.html";
  });

  document.getElementById("summaryBtn").addEventListener("click", () => {
    window.location.href = "summary.html";
  });

});
