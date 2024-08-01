document.getElementById('query-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var query = document.getElementById('query').value;
    var queries = query.split(';').filter(q => q.trim() !== '');
    var resultTextarea = document.getElementById('result');
    resultTextarea.value = '';

    executeQueriesSequentially(queries, 0, resultTextarea);
});

function executeQueriesSequentially(queries, index, resultTextarea) {
    if (index >= queries.length) return;

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'query=' + encodeURIComponent(queries[index])
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultTextarea.value += formatResult(data.result) + '\n---\n';
            fetchDBInfo(); // 쿼리 실행 후 데이터베이스 정보를 갱신합니다.
        } else {
            resultTextarea.value += 'Error: ' + data.message + '\n---\n';
        }
        executeQueriesSequentially(queries, index + 1, resultTextarea);
    });
}

function formatResult(result) {
    if (result.length === 0) return "No results found.";
    let formatted = "";
    result.forEach(row => {
        formatted += Object.values(row).join("\t") + "\n";
    });
    return formatted;
}

function fetchDBInfo() {
    fetch('/db_info')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('created-at').innerText = new Date(data.created_at * 1000).toLocaleString();
            document.getElementById('last-request').innerText = new Date(data.last_request * 1000).toLocaleString();
            renderTables(data.tables, data.schema, data.counts);
        }
    });
}

function renderTables(tables, schema, counts) {
    var tablesDiv = document.getElementById('tables');
    tablesDiv.innerHTML = ''; // 기존 내용을 지웁니다.

    tables.forEach(table => {
        var tableName = table[0];
        var tableHTML = `
            <div>
                <span class="expand-btn" onclick="toggleTable('${tableName}')">[+]</span>
                <h3 style="display:inline;">테이블: ${tableName} (Entries: ${counts[tableName]})</h3>
            </div>
            <div id="table-${tableName}" class="table-content">
                <table>
                    <thead>
                        <tr>
                            <th>인덱스</th>
                            <th>컬럼 이름</th>
                            <th>데이터 타입</th>
                            <th>NOT NULL</th>
                            <th>기본값</th>
                            <th>PRIMARY KEY</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        schema[tableName].forEach(column => {
            tableHTML += `
                        <tr>
                            <td>${column[0]}</td>
                            <td>${column[1]}</td>
                            <td>${column[2]}</td>
                            <td>${column[3]}</td>
                            <td>${column[4]}</td>
                            <td>${column[5]}</td>
                        </tr>
            `;
        });
        tableHTML += `
                    </tbody>
                </table>
                <div>
                    <span class="expand-btn" onclick="toggleEntries('${tableName}')">[+]</span>
                    <span>Entries</span>
                </div>
                <div id="entries-${tableName}" class="entries-content"></div>
            </div>
        `;
        tablesDiv.innerHTML += tableHTML;
    });
}

function toggleTable(tableName) {
    var contentDiv = document.getElementById(`table-${tableName}`);
    var expandBtn = contentDiv.previousElementSibling.querySelector('.expand-btn');
    if (contentDiv.style.display === 'none' || contentDiv.style.display === '') {
        contentDiv.style.display = 'block';
        expandBtn.innerText = '[-]';
    } else {
        contentDiv.style.display = 'none';
        expandBtn.innerText = '[+]';
    }
}

function toggleEntries(tableName) {
    var entriesDiv = document.getElementById(`entries-${tableName}`);
    var expandBtn = entriesDiv.previousElementSibling.querySelector('.expand-btn');
    if (entriesDiv.style.display === 'none' || entriesDiv.style.display === '') {
        fetchEntries(tableName, entriesDiv);
        entriesDiv.style.display = 'block';
        expandBtn.innerText = '[-]';
    } else {
        entriesDiv.style.display = 'none';
        expandBtn.innerText = '[+]';
    }
}

function fetchEntries(tableName, entriesDiv) {
    fetch(`/entries/${tableName}`)
    .then(response => response.json())
    .then(entriesData => {
        if (entriesData.status === 'success') {
            if (entriesData.entries.length > 0) {
                let entriesHTML = '<table><thead><tr>';
                Object.keys(entriesData.entries[0]).forEach(key => {
                    entriesHTML += `<th>${key}</th>`;
                });
                entriesHTML += '</tr></thead><tbody>';
                entriesData.entries.forEach(entry => {
                    entriesHTML += '<tr>';
                    Object.values(entry).forEach(value => {
                        entriesHTML += `<td>${value}</td>`;
                    });
                    entriesHTML += '</tr>';
                });
                entriesHTML += '</tbody></table>';
                entriesDiv.innerHTML = entriesHTML;
            } else {
                entriesDiv.innerHTML = '<p>No entries found.</p>';
            }
        }
    });
}

// 페이지 로드 시 데이터베이스 정보를 가져옵니다.
fetchDBInfo();
