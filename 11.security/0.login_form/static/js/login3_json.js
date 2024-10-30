document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();  // 폼 기본 동작 막기

    // 입력된 값 가져오기
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // 백엔드에 로그인 요청 보내기
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 로그인 성공 시 메시지 표시 또는 페이지 이동
            // window.location.href = "/welcome";
            window.location.href = `/welcome?username=${encodeURIComponent(data.username)}`;
        } else {
            // 로그인 실패 시 오류 메시지 표시
            document.getElementById("error").textContent = data.message;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
