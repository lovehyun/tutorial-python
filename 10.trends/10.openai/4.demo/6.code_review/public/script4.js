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

        // GitHub URL
        const githubUrl = document.getElementById("github_url").value;

        // 선택된 취약점 유형 수집 (checkbox name="vulnerability")
        const vulnCheckboxes = document.querySelectorAll("input[name='vulnerability']:checked");
        let vulnTypes = [];
        vulnCheckboxes.forEach(checkbox => {
            vulnTypes.push(checkbox.value);
        });

        // API 호출 시 취약점 유형 배열도 전송
        fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                github_url: githubUrl,
                vulnerability_types: vulnTypes
            })
        })
        .then(response => response.json())
        .then(data => {
            // 소스코드를 먼저 표시
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

            // 분석 결과 영역 업데이트
            analysisElem.innerText = data.analysis;

            // 분석 결과에서 '라인 번호:' 뒤의 숫자 또는 범위를 찾아 하이라이팅
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
