document.addEventListener("DOMContentLoaded", async () => {
    const groupListContainer = document.getElementById("groupList");
   
  
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      alert("You need to log in first!");
      return;
    }
  
    try {
      const response = await fetch("http://192.168.56.101:5001/groups", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        groupListContainer.innerHTML = "";
  
        if (data.groups && data.groups.length > 0) {
            data.groups.forEach((group) => {
              const groupCard = document.createElement("div");
              groupCard.classList.add("group-card");
    
              const groupName = document.createElement("h3");
              groupName.textContent = group.name;
              groupCard.appendChild(groupName);
    
              const memberList = document.createElement("ul");
              group.members.forEach((member) => {
                const memberItem = document.createElement("li");
                memberItem.textContent = member.username;
                memberList.appendChild(memberItem);
              });
    
              groupCard.appendChild(memberList);
              groupListContainer.appendChild(groupCard);
            });
          } else {
            groupListContainer.innerHTML = "<p>No groups available.</p>";
          }
        } else {
          const error = await response.json();
          groupListContainer.innerHTML = `<p style="color:red;">Error: ${error.message || "Failed to fetch groups."}</p>`;
        }
      } catch (err) {
        groupListContainer.innerHTML = `<p style="color:red;">An error occurred while fetching group details.</p>`;
        console.error(err);
      }
    });
    
    // Back to Dashboard Button
    document.getElementById("backToDashboardBtn").addEventListener("click", () => {
      window.location.href = "dashboard.html";
    });