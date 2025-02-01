document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("checkForm");
    const progressElem = document.getElementById("progress");
    const errorElem = document.getElementById("error");
    const codeContainer = document.getElementById("codeContainer");
    const analysisElem = document.getElementById("analysis");
    const submitButton = document.querySelector("button");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // 버튼 비활성화
        submitButton.disabled = true;

        // 이전 결과 초기화
        errorElem.innerText = "";
        codeContainer.innerText = "";
        analysisElem.innerText = "";

        // 진행 상태 표시
        progressElem.style.display = "block";
        progressElem.innerText = "처리 중입니다...";

        const githubUrl = document.getElementById("github_url").value;

        fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ github_url: githubUrl })
        })
        .then(response => response.json())
        .then(data => {
            // 먼저 소스코드를 표시합니다.
            const codeLines = data.code.split("\n");
            codeLines.forEach((line, index) => {
                const lineDiv = document.createElement("div");
                lineDiv.className = "code-line";
                lineDiv.id = "line-" + (index + 1);

                const lineNumberSpan = document.createElement("span");
                lineNumberSpan.className = "line-number";
                lineNumberSpan.innerText = (index + 1) + " ";

                const codeText = document.createTextNode(line);
                lineDiv.appendChild(lineNumberSpan);
                lineDiv.appendChild(codeText);
                codeContainer.appendChild(lineDiv);
            });

            // 분석 결과 영역에 우선 기본 텍스트를 표시 (예: "분석 중입니다..." 혹은 바로 data.analysis)
            analysisElem.innerText = data.analysis;

            // 분석 결과에서 '라인 번호:' 뒤에 나오는 숫자나 범위를 정규표현식으로 추출합니다.
            // 예: "라인 번호: 31" 또는 "라인 번호: 31-36" 또는 "**라인 번호**: 31"
            // const regex = /라인 번호:\s*(\d+)(?:\s*-\s*(\d+))?/g;
            const regex = /라인 번호.*?(\d+(?:\s*-\s*\d+)?)/g;
            let match;
            while ((match = regex.exec(data.analysis)) !== null) {
                const start = parseInt(match[1]);
                const end = match[2] ? parseInt(match[2]) : start;
                for (let i = start; i <= end; i++) {
                    const lineElem = document.getElementById("line-" + i);
                    if (lineElem) {
                        lineElem.classList.add("highlight");
                    }
                }
            }

            // 진행 상태 숨기고 버튼 활성화
            progressElem.style.display = "none";
            submitButton.disabled = false;
        })
        .catch(error => {
            progressElem.style.display = "none";
            errorElem.innerText = "요청 처리 중 에러 발생: " + error;
            submitButton.disabled = false;
        });
    });
});
