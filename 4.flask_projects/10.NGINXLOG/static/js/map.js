document.addEventListener('DOMContentLoaded', async function () {
    const response = await fetch('/api/locations');
    const data = await response.json();

    const tbody = document.querySelector('#ip-table tbody');
    tbody.innerHTML = '';

    const countryCount = {};

    data.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${item.ip}</td><td>${item.country}</td>`;
        tbody.appendChild(tr);

        // 국가별 접속자 수 집계
        if (countryCount[item.country]) {
            countryCount[item.country]++;
        } else {
            countryCount[item.country] = 1;
        }
    });

    // 국가명과 접속자수 배열로 변환
    const labels = Object.keys(countryCount);
    const counts = Object.values(countryCount);

    // 차트 그리기
    const ctx = document.getElementById('countryChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '접속자 수',
                data: counts,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
});
