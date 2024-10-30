document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();  // 폼 기본 동작 막기

    // 입력된 값 가져오기
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // FormData 객체 생성
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    // 백엔드에 로그인 요청 보내기
    fetch("/login", {
        method: "POST",
        body: formData  // Content-Type은 자동 설정됨 (multipart/form-data; boundary=... (여기에 내용추가됨))
    })
    .then(response => {
        if (response.ok) {
            // 로그인 성공 시 페이지 이동
            window.location.href = "/welcome";
        } else {
            // 로그인 실패 시 오류 메시지 표시
            document.getElementById("error").textContent = "Invalid credentials. Please try again.";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
