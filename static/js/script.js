async function postData(url = "", data = {}) { 
    const response = await fetch(url, { 
    method: "POST", 
    headers: { 
    "Content-Type": "application/json",
    }, body: JSON.stringify(data), 
    }); 
    return response.json(); 
    }



sendbutton.addEventListener("click", async()=>{
    questioninput = document.getElementById("questioninput").value;
    document.getElementById("questioninput").value = "";
    document.querySelector(".right2").style.display="block"
    document.querySelector(".right1").style.display="none"
    
    question1.innerHTML = questioninput;
    //answer
    
    let result = await postData( "/api",{"question":questioninput})
    solution.innerHTML = result.result;
}) 