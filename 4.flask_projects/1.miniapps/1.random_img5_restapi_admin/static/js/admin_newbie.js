// HTML 문서 로딩 완료 후 실행
document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form"); // 업로드 폼
    const imageTable = document.querySelector("#image-table tbody"); // 이미지 목록 테이블의 tbody 부분

    // 서버에서 이미지 목록을 불러와서 테이블에 출력
    function loadImages() {
        fetch("/api/images")
            .then(res => res.json())
            .then(data => {
                imageTable.innerHTML = ""; // 기존 테이블 비우기
                data.forEach(img => {
                    const row = document.createElement("tr"); // 테이블 행 생성
                    row.innerHTML = `
                        <td><img src="${img.url}" width="100"></td>
                        <td>${img.filename}</td>
                        <td>
                            <input type="text" value="${img.keywords.join(', ')}" data-filename="${img.filename}" class="keyword-input">
                            <button class="update-btn" data-filename="${img.filename}">수정</button>
                        </td>
                        <td>
                            <button class="delete-btn" data-filename="${img.filename}">삭제</button>
                        </td>`;
                    imageTable.appendChild(row); // 테이블에 행 추가

                    // 수정 버튼에 직접 이벤트 등록
                    const updateBtn = row.querySelector(".update-btn");
                    updateBtn.addEventListener("click", () => {
                        const input = row.querySelector(".keyword-input");
                        const keywords = input.value.split(',').map(k => k.trim());
                        fetch(`/api/images/${img.filename}`, {
                            method: "PUT",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ keywords })
                        }).then(() => loadImages());
                    });

                    // 삭제 버튼에 직접 이벤트 등록
                    const deleteBtn = row.querySelector(".delete-btn");
                    deleteBtn.addEventListener("click", () => {
                        if (confirm("정말 삭제하시겠습니까?")) {
                            fetch(`/api/images/${img.filename}`, {
                                method: "DELETE"
                            }).then(() => loadImages());
                        }
                    });
                });
            });
    }

    // 이미지 업로드 폼 전송 시 처리
    uploadForm.addEventListener("submit", e => {
        e.preventDefault(); // 페이지 새로고침 방지
        const formData = new FormData(uploadForm); // 이미지와 키워드 포함한 폼 데이터 생성
        fetch("/api/images", {
            method: "POST",
            body: formData
        }).then(() => {
            uploadForm.reset(); // 입력창 초기화
            loadImages();       // 테이블 갱신
        });
    });

    // 페이지 로딩 시 이미지 목록 초기 표시
    loadImages();
});
