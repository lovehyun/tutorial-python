// 모달 열기
function showMail(mailId) {
    fetch(`/mail/${mailId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            document.getElementById('modalSubject').textContent = data.subject;
            document.getElementById('modalBody').textContent = data.body;
            // document.getElementById('modalBody').innerHTML = data.body;
            document.getElementById('mailModal').style.display = 'flex';
        })
        .catch(error => console.error('Error:', error));
}

// 모달 닫기
function closeModal() {
    document.getElementById('mailModal').style.display = 'none';
}
