// 현재 페이지의 기본 경로를 가져오는 함수
function getBasePath() {
    // 현재 URL에서 경로 부분만 추출 (예: /board1/)
    const path = window.location.pathname;
    // 마지막 슬래시 이후의 파일명을 제외한 경로 반환
    return path.substring(0, path.lastIndexOf('/') + 1);
}

document.addEventListener('DOMContentLoaded', function () {
    const basePath = getBasePath();
    fetch(basePath + 'list')
        .then(res => res.json())
        .then(data => {
            data.forEach(post => {
                makeCard(post.id, post.title, post.message);
            });
        });
});

function makeCard(id, title, message) {
    const card = document.createElement('div');
    card.className = 'col-md-4';
    card.innerHTML = `
        <div class="card mb-4" id="card_${id}">
            <div class="card-body">
                <p class="card-id">${id}</p>
                <p class="card-title">${title}</p>
                <p class="card-text">${message}</p>
                <button class="btn btn-info" onclick="modifyPost(${id})">수정</button>
                <button class="btn btn-warning" onclick="deletePost(${id})">삭제</button>
            </div>
        </div>`;
    document.getElementById('card-list').appendChild(card);
}

function uploadPost() {
    const title = document.getElementById('input-title').value;
    const message = document.getElementById('input-text').value;
    const basePath = getBasePath();

    fetch(basePath + 'create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, message })
    }).then(res => res.json())
      .then(data => {
          if (data.result === 'success') {
              alert('저장 완료!');
              location.reload();
          }
      });
}

function deletePost(id) {
    const basePath = getBasePath();
    fetch(basePath + 'delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    }).then(res => res.json())
      .then(data => {
          if (data.result === 'success') {
              alert('삭제 완료!');
              location.reload();
          }
      });
}

function modifyPost(id) {
    const card = document.getElementById(`card_${id}`);
    const oldTitle = card.querySelector('.card-title').textContent;
    const oldText = card.querySelector('.card-text').textContent;

    card.innerHTML = `
        <div class="card-body">
            <input class="form-control mb-2" id="mod-title-${id}" value="${oldTitle}">
            <input class="form-control mb-2" id="mod-text-${id}" value="${oldText}">
            <button class="btn btn-primary" onclick="updatePost(${id})">저장</button>
        </div>`;
}

function updatePost(id) {
    const title = document.getElementById(`mod-title-${id}`).value;
    const message = document.getElementById(`mod-text-${id}`).value;
    const basePath = getBasePath();

    fetch(basePath + 'modify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, title, message })
    }).then(res => res.json())
      .then(data => {
          if (data.result === 'success') {
              alert('수정 완료!');
              location.reload();
          }
      });
}
