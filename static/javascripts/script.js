const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");

let userText = null;
const API_KEY = "PASTE-YOUR-API-KEY-HERE"; // Paste your API key here
let API_URL = "/medlocalgpt/api/v1/en/advanced/openai/ask"; // Default API URL

const sampleOptions = document.querySelector("#sample-options");


sampleOptions.addEventListener("change", () => {
    // Update the API_URL based on the selected option
    const selectedOption = sampleOptions.value;

    switch (selectedOption) {
        case "option1":
            API_URL = "/medlocalgpt/api/v1/en/advanced/openai/ask";
            break;
        case "option2":
            API_URL = "/medlocalgpt/api/v1/uk/advanced/openai/ask";
            break;
        case "option3":
            API_URL = "/medlocalgpt/api/v1/en/dataset/openai/ask";
            break;
        // Add more cases for other options as needed
        default:
            // Use the default API URL
            API_URL = "/medlocalgpt/api/v1/en/advanced/openai/ask";
            break;
    }
});

const loadDataFromLocalstorage = () => {
    // Load saved chats and theme from local storage and apply/add on the page
    const themeColor = localStorage.getItem("themeColor");

    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";

    const defaultText = `<div class="default-text">
                            <h1>⚕️ MedLocalGPT Demo</h1>
                            <p>Applying LLM-powered AI Assistant to Enhance Support for Physical Rehabilitation & Telerehabilitation Therapists, Students, and Patients. <br> Ask your (medical EBSCO) dataset using LLMs and Embeddings. <br> Optionally you can use local LLMs, OpenAI GPT models or other SaaS solutions. <br> Your chat history will be displayed here.</p>
                        </div>`

    chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
    chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to bottom of the chat container
}

const createChatElement = (content, className) => {
    // Create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv; // Return the created chat div
}


const getChatResponse = async (incomingChatDiv) => {
    const pElement = document.createElement("p");

    // Function to make URLs clickable
    function makeUrlsClickable(text) {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, (url) => {
            return `<a href="${url}" target="_blank">${url}</a>`;
        });
    }

    // Function to toggle visibility of hidden content
    function toggleHiddenContent(pElement, readMoreLink) {
        if (pElement.classList.contains('show-hidden-content')) {
            pElement.classList.remove('show-hidden-content');
            readMoreLink.textContent = 'Read More';
        } else {
            pElement.classList.add('show-hidden-content');
            readMoreLink.textContent = 'Read Less';
        }
    }

    // Define the properties and data for the API request
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: userText
        })
    }

    // Send POST request to API, get response and set the response as paragraph element text
    try {
        const response = await (await fetch(API_URL, requestOptions)).json();
        if (sampleOptions.value == "option1" || sampleOptions.value == "option2") {
            pElement.textContent = response['response'].trim();
        }
        if (sampleOptions.value == "option3") {
            // Handle option3 response with hidden content
            const answerText = response['Answer'].trim();
            pElement.innerHTML = answerText;
        
            response['Sources'].forEach((textArray) => {
              textArray.forEach((text) => {
                const textWithLinks = makeUrlsClickable(text);
                pElement.innerHTML += "<br>" + textWithLinks; // Append the text with links to the <p> element
              });
            });
        
            // Add "Read More" link
            const readMoreLink = document.createElement("span");
            readMoreLink.classList.add("read-more-link");
            readMoreLink.textContent = 'Read More';
            pElement.appendChild(readMoreLink);
        
            // Add click event listener to "Read More" link
            readMoreLink.addEventListener('click', () => {
              toggleHiddenContent(pElement, readMoreLink);
            });
          }
        
    } catch (error) {
        console.log(error);
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
    }

    // Remove the typing animation, append the paragraph element and save the chats to local storage
    incomingChatDiv.querySelector(".typing-animation").remove();
    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    localStorage.setItem("all-chats", chatContainer.innerHTML);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}


const copyResponse = (copyBtn) => {
    // Copy the text content of the response to the clipboard
    const reponseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(reponseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
}

const showTypingAnimation = () => {
    // Display the typing animation and call the getChatResponse function
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="./static/images/gpt_logo.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    // Create an incoming chat div with typing animation and append it to chat container
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
}

const handleOutgoingChat = () => {
    userText = chatInput.value.trim(); // Get chatInput value and remove extra spaces
    if (!userText) return; // If chatInput is empty return from here

    // Clear the input field and reset its height
    chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;

    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="./static/images/user.jpg" alt="user-img">
                        <p>${userText}</p>
                    </div>
                </div>`;

    // Create an outgoing chat div with user's message and append it to chat container
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
}

deleteButton.addEventListener("click", () => {
    // Remove the chats from local storage and call loadDataFromLocalstorage function
    if (confirm("Are you sure you want to delete all the chats?")) {
        localStorage.removeItem("all-chats");
        loadDataFromLocalstorage();
    }
});

themeButton.addEventListener("click", () => {
    // Toggle body's class for the theme mode and save the updated theme to the local storage 
    document.body.classList.toggle("light-mode");
    localStorage.setItem("themeColor", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {
    // Adjust the height of the input field dynamically based on its content
    chatInput.style.height = `${initialInputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If the Enter key is pressed without Shift and the window width is larger 
    // than 800 pixels, handle the outgoing chat
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleOutgoingChat();
    }
});

loadDataFromLocalstorage();
sendButton.addEventListener("click", handleOutgoingChat);