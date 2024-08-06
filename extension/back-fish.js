// chrome.tabs.onMessage.addListener(() => {
//     const url = tabs[0].url;
//     fetch('http://127.0.0.1:5000/process_url', {
//         method: 'POST',
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//             "url": "Add your name in the body"
//         })
//     })
//         .then(response => response.json())
//         .then(data => {
//             // Send the result back to content script
//             chrome.tabs.sendMessage(tabs[0].id, { result: data.result });
//         })
// })
chrome.tabs.onActivated.addListener(() => {
    fetch("https://reqres.in/api/users", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            "name": "morpheus",
            "job": "leader"
        })
    })
        .then((resp) => resp.json())
        .then(json => console.log(json.id))
    console.log("I Ran")
})
