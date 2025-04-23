// 현재 페이지의 기본 경로를 가져오는 함수
function getBasePath() {
    // 현재 URL에서 경로 부분만 추출 (예: /board1/)
    const path = window.location.pathname;
    // 마지막 슬래시 이후의 파일명을 제외한 경로 반환
    return path.substring(0, path.lastIndexOf('/') + 1);
}

document.addEventListener('DOMContentLoaded', function() {
    const basePath = getBasePath();
    fetch(basePath + 'list')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            for (let item of data) {
                makeCard(item.id, item.title, item.message, item.image);
            }
        })
        .catch(error => console.error('Error:', error));
});

function makeCard(id, title, message, image) {
    const cardList = document.getElementById('card-list');
    const card = document.createElement('div');
    const basePath = getBasePath();

    card.className = 'card';
    card.id = `card_${id}`;
    card.innerHTML = `
        <div class="card-body">
            <p class="card-id">${id}</p>
            ${image ? `<img src="uploads/${image}" class="card-img-top" alt="...">` : ''}
            <p class="card-title">${title}</p>
            <p class="card-text">${message}</p>
            <button type="button" class="btn btn-info" onclick="modifyPost(${id})">수정</button>
            <button type="button" class="btn btn-warning" onclick="deletePost(${id})">삭제</button>
        </div>
    `;
    cardList.appendChild(card);
}

function uploadPost() {
    const formData = new FormData();
    formData.append('title', document.getElementById("input-title").value);
    formData.append('message', document.getElementById("input-text").value);
    formData.append('file', document.getElementById("input-file").files[0]);
    const basePath = getBasePath();

    fetch(basePath + 'create', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        if (data.result === 'success') {
            alert("저장 완료!");
            window.location.reload();
        } else {
            alert("서버 오류: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function deletePost(id) {
    const basePath = getBasePath();
    fetch(basePath + 'delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        if (data.result === 'success') {
            alert("삭제 완료!");
            window.location.reload();
        } else {
            alert("서버 오류: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function modifyPost(id) {
    const cardId = `#card_${id}`;
    const cardTitle = document.querySelector(`${cardId} .card-title`).textContent;
    const cardText = document.querySelector(`${cardId} .card-text`).textContent;

    const card = document.querySelector(cardId);
    card.innerHTML = `
        <div class="card-body">
            <div class="form-group">
                <input class="card-title form-control" id="mod-title" value="${cardTitle}">
            </div>
            <div class="form-group">
                <input class="card-text form-control" id="mod-text" value="${cardText}">
            </div>
            <div class="form-group">
                <input type="file" id="mod-file" class="form-control">
            </div>
            <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="delete-image">
                <label class="form-check-label" for="delete-image">이미지 삭제</label>
            </div>
            <div class="form-group">
                <button type="submit" onclick="updatePost(${id})" class="btn btn-primary">저장</button>
            </div>
        </div>
    `;
}

function updatePost(id) {
    const formData = new FormData();
    formData.append('id', id);
    formData.append('title', document.getElementById("mod-title").value);
    formData.append('message', document.getElementById("mod-text").value);
    formData.append('file', document.getElementById("mod-file").files[0]);
    formData.append('delete_image', document.getElementById("delete-image").checked);
    const basePath = getBasePath();

    fetch(basePath + 'modify', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        if (data.result === 'success') {
            alert("수정 완료!");
            window.location.reload();
        } else {
            alert("서버 오류: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
