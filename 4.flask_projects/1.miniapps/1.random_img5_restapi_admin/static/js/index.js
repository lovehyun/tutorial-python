document.getElementById("search-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const query = document.getElementById("query").value;

    fetch(`/api/images/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            // 제목만 바꾸기
            document.getElementById("result-heading").textContent = `"${query}"에 대한 검색 결과`;

            // 결과 HTML 직접 생성
            // 방법1.
            // let html = "";
            // for (const img of data) {
            //     html += `
            //         <div class="image-box">
            //             <img src="${img.url}" width="200"><br>
            //             <small>${img.filename}</small>
            //         </div>
            //     `;
            // }

            // 방법2.
            const html = data.map(img => `
                <div class="image-box">
                    <img src="${img.url}" width="200"><br>
                    <small>${img.filename}</small>
                </div>
            `).join("");

            document.getElementById("results").innerHTML = html || "<p>검색 결과가 없습니다.</p>";
        });
});
