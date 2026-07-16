const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const userInput = document.getElementById("user-input");
const typing = document.getElementById("typing");

let recognition;

function addMessage(sender, message) {

    const div = document.createElement("div");

    div.className = "message " + sender;

    div.innerHTML = `
        <strong>${sender === "user" ? "You" : "🌿 CalmBridge AI"}</strong><br>
        ${message}
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function speak(text){

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.rate = 0.92;
    speech.pitch = 1;
    speech.volume = 1;

    const voices = speechSynthesis.getVoices();

    const female = voices.find(v =>
        v.name.toLowerCase().includes("female") ||
        v.name.toLowerCase().includes("zira") ||
        v.name.toLowerCase().includes("google")
    );

    if(female){
        speech.voice = female;
    }

    speechSynthesis.speak(speech);
}

async function sendMessage(message){

    if(message.trim()==="") return;

    addMessage("user",message);

    userInput.value="";

    typing.classList.remove("hidden");

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })

        });

        const data = await response.json();

        typing.classList.add("hidden");

        addMessage("bot",data.reply);

        speak(data.reply);

    }
    catch(error){

        typing.classList.add("hidden");

        addMessage("bot","Sorry, something went wrong. Please try again.");

        console.error(error);

    }

}

sendBtn.onclick=()=>{

    sendMessage(userInput.value);

};

userInput.addEventListener("keypress",e=>{

    if(e.key==="Enter"){

        sendMessage(userInput.value);

    }

});

const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

if(SpeechRecognition){

    recognition = new SpeechRecognition();

    recognition.lang="en-US";

    recognition.interimResults=false;

    recognition.continuous=false;

    micBtn.onclick=()=>{

        recognition.start();

        micBtn.innerHTML="🎙️";

    };

    recognition.onresult=(event)=>{

        const transcript = event.results[0][0].transcript;

        userInput.value=transcript;

        sendMessage(transcript);

    };

    recognition.onend=()=>{

        micBtn.innerHTML="🎤";

    };

    recognition.onerror=()=>{

        micBtn.innerHTML="🎤";

        alert("Microphone not detected.");

    };

}
else{

    micBtn.disabled=true;

}