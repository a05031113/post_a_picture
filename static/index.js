const msg = document.getElementById("msg");
const input = document.getElementById("input");
const submit = document.getElementById("submit");
const insert = document.getElementById("insert");
const add = document.getElementById("add");
let uploading = false;
getMessage();
submit.addEventListener("click", ()=>{
    if (!uploading){
        uploading = true;
        if (!msg.value){
            console.log("no msg")
            return false;
        }
        if (!input.files){
            console.log("no file")
            return false;
        }
        const file = input.files[0]
        updateProfilePhoto(file);
    }
})
add.addEventListener("click", ()=>{
    input.click();
});
input.addEventListener("change", (event)=>{
    const file = event.target.files[0];
    if (file){
        let src = URL.createObjectURL(file);
        add.src = src;
    }
});
async function updateProfilePhoto(file){
    try{
        const { url } = await fetch("/api/upload/url").then(res => res.json())
        const responseUrl = await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "multipart/form-data"
            },
            body: file
        });
        if (responseUrl.status == 200){
            const imageFile = url.split('?')[0].split("/");
            const fileName = imageFile[imageFile.length-1];
            const data = {
                "msg": msg.value,
                "imgName": fileName
            }
            const responseSuccess = await fetch("/api/upload/success", {
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    "Content-Type": "application/json"
                }
            });
            if (responseSuccess.status === 200){
                const responseMsg = await fetch("/api/message/new");
                const result = await responseMsg.json();
                const data = result.data;
                const messageHtml = `
                    <div class="messageBox">
                        <img class="messageImg" src="${data.imgURL}" alt="">
                        <div class="message">message: ${data.msg}</div>
                    </div>
                `
                insert.insertAdjacentHTML("afterbegin", messageHtml);
                uploading = false;
                msg.value = null;
                add.src = "/static/add.png";
            }
        }
    }catch(error){
        console.log({"error": error});
        uploading = false;
    }
}
async function getMessage(){
    try{
        const response = await fetch("/api/messages");
        const result = await response.json();
        const data = result.data;
        let messageHtml = ``;
        for (i=0; i<data.length; i++){
            messageHtml = messageHtml + `
                <div class="messageBox">
                    <img class="messageImg" src="${data[i].imgURL}" alt="">
                    <div class="message">message: ${data[i].msg}</div>
                </div>
            `
        }
        insert.insertAdjacentHTML("beforeend", messageHtml);
    }catch(error){
        console.log(error);
    }
}