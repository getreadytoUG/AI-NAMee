const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const backButton = document.getElementById('back-button');

firstMessage();

function addMessage(message, isUser = true, messageId = null) {
    const messageElement = document.createElement('div');
    console.log(message);

    // 줄바꿈을 <br>로 변환
    // messageElement.textContent = message;
    messageElement.innerHTML = message.replace(/\n/g, '<br>');

    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    
    if (messageId) {
        messageElement.setAttribute('id', messageId);
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function firstMessage() {
    addMessage("안녕하세요! 법률 정보를 기반으로 답변해 드리는 AI-NAMee 입니다.\n다음과 같은 형식으로 질문할 때 가장 좋은 성능을 가질 수 있으니 참고해 주세요!\n\n  1. 법명을 정확히 해주세요. 찾고자 하는 법명을 정확히 입력해 주실 때 가장 좋은 답변을 제시할 수 있습니다. \n 2. 한 번에 한 가지의 법에 대해서만 질문해 주세요. 두 가지 이상의 법률에 대한 질문을 하실 경우 정확한 답변이 어려울 수 있습니다. \n \n 어떻게 도와드릴까요?", false);
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message);

        // 응답을 기다리는 동안 입력 및 버튼 비활성화
        messageInput.disabled = true;
        sendButton.disabled = true;

        messageInput.value = '';

        // 각 로딩 메시지에 대한 고유 ID 생성
        const loadingMessageId = 'loading-message-' + Date.now();  
        addMessage("답변을 생성중입니다....", false, loadingMessageId);

        try {
            const response = await fetch("http://127.0.0.1:8000/legalchat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "data": message }) // 여기서 'data'로 변경
            });

            if (response.ok) {
                const data = await response.json();
                const answer = data.text; // 'answer'에서 'text'로 변경

                // 로딩 메시지를 실제 답변으로 업데이트
                const loadingMessageElement = document.getElementById(loadingMessageId);
                if (loadingMessageElement) {
                    loadingMessageElement.innerHTML = answer.replace(/\n/g, '<br>').replace(/\\n/g, '<br>').replace(/\r?\n/g, '<br>');
                }

            } else {
                // 응답이 OK가 아닐 경우 에러 메시지 표시
                const loadingMessageElement = document.getElementById(loadingMessageId);
                if (loadingMessageElement) {
                    loadingMessageElement.textContent = "답변을 가져오지 못했습니다. 다시 시도해주세요.";
                }
            }
        } catch (error) {
            // fetch 오류 처리
            const loadingMessageElement = document.getElementById(loadingMessageId);
            if (loadingMessageElement) {
                loadingMessageElement.textContent = "오류가 발생했습니다. 다시 시도해주세요.";
            }
        }

        // 응답을 받은 후 입력 및 버튼 다시 활성화
        messageInput.disabled = false;
        sendButton.disabled = false;

        // 다시 입력 필드에 포커스
        messageInput.focus();
    }
}


sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

backButton.addEventListener('click', () => {
    window.location.href = "./front.html";
});
