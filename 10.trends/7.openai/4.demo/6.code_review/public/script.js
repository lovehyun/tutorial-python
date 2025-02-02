document.addEventListener("DOMContentLoaded", function(){
    const form = document.getElementById("codeForm");
    const resultPre = document.getElementById("result");

    form.addEventListener("submit", function(e){
        e.preventDefault();
        const code = document.getElementById("code").value;

        fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultPre.innerText = data.error;
            } else {
                resultPre.innerText = data.analysis;
                // resultPre.innerHTML = data.analysis;
            }
        })
        .catch(error => {
            resultPre.innerText = "요청 처리 중 에러 발생: " + error;
        });
    });
});
