// 메시지 리스트 초기화 및 업데이트
function updateMessages_OLD(messages) {
    const messageList = document.getElementById("message_list");
    messageList.innerHTML = ""; // 기존 메시지 리스트 초기화

    messages.forEach(message => {
        const li = document.createElement("li");

        // 1. FIXME: 취약한 코드 추가해서 데모
        // li.innerHTML = message;  // XSS 취약점을 의도적으로 발생시키기 위해 innerHTML 사용

        // 2. 최신 브라우저에서는 fetch를 통해서 받아온 script 구문은 실행되지 않음
        // XSS 취약점: <script> 태그를 동적으로 생성해 메시지를 실행 -->
        li.textContent = message;
        // <-- 2

        // 3. TODO: XSS 보호를 위해 textContent 사용
        // li.textContent = message;
        messageList.appendChild(li);
    });
}

// 메시지 리스트 초기화 및 업데이트
function updateMessages_EASY(messages) {
    const messageList = document.getElementById("message_list");
    messageList.innerHTML = ""; // 기존 메시지 리스트 초기화

    messages.forEach(message => {
        const li = document.createElement("li");

        // 1. FIXME: 취약한 코드 추가해서 데모
        // li.innerHTML = message;  // XSS 취약점을 의도적으로 발생시키기 위해 innerHTML 사용

        // 2. 최신 브라우저에서는 fetch를 통해서 받아온 script 구문은 실행되지 않음
        // XSS 취약점: <script> 태그를 동적으로 생성해 메시지를 실행 -->

        // 메시지에서 <script> 태그를 확인
        if (message.includes("<script>")) {
            // 스크립트 태그의 내용을 추출
            const scriptContent = message.split("<script>")[1].split("</script>")[0];

            // 스크립트 요소 생성 및 실행
            const script = document.createElement("script");
            script.textContent = scriptContent;
            li.appendChild(script); // <script>를 li에 추가하여 실행
        } else {
            // 일반 텍스트는 그대로 삽입
            li.textContent = message;
        }
        // <-- 2

        // 3. TODO: XSS 보호를 위해 textContent 사용
        // li.textContent = message;
        messageList.appendChild(li);
    });
}

// 메시지 리스트 초기화 및 업데이트
function updateMessages_NEW(messages) {
    const messageList = document.getElementById("message_list");
    messageList.innerHTML = ""; // 기존 메시지 리스트 초기화

    messages.forEach(message => {
        const li = document.createElement("li");
        
        // 1. FIXME: 취약한 코드 추가해서 데모
        // li.innerHTML = message;  // XSS 취약점을 의도적으로 발생시키기 위해 innerHTML 사용

        // 2. 최신 브라우저에서는 fetch를 통해서 받아온 script 구문은 실행되지 않음
        // XSS 취약점: <script> 태그를 동적으로 생성해 메시지를 실행 -->
        const scriptTag = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
        const matchedScript = scriptTag.exec(message);

        if (matchedScript && matchedScript[1]) {
            // <script> 태그의 내용을 추출하여 실행
            const script = document.createElement("script");
            script.innerHTML = matchedScript[1];
            li.appendChild(script);
        } else {
            // 일반 텍스트는 그대로 삽입
            li.innerHTML = message;
        }
        // <-- 2

        // 3. TODO: XSS 보호를 위해 textContent 사용
        // li.textContent = message;
        messageList.appendChild(li);
    });
}

// 메시지 제출
function submitMessage() {
    const userInput = document.getElementById("user_input").value;
    fetch("/messages", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        updateMessages_NEW(data.messages);
        document.getElementById("user_input").value = ""; // 입력 필드 초기화
    });
}

// 메시지 모두 지우기
function clearMessages() {
    fetch("/messages", {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        updateMessages_NEW(data.messages);
    });
}

// 페이지 로드 시 초기 메시지 가져오기
window.onload = function() {
    fetch("/messages")
        .then(response => response.json())
        .then(data => {
            updateMessages_NEW(data.messages);
        });
};
