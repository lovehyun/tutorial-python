async function fetchTweets() {
    const res = await fetch('/api/tweets');
    return await res.json();
}

async function likeTweet(id) {
    await fetch(`/api/like/${id}`, { method: 'POST' });
    renderTweets();
}

async function unlikeTweet(id) {
    await fetch(`/api/unlike/${id}`, { method: 'POST' });
    renderTweets();
}

async function deleteTweet(id) {
    if (confirm('정말 삭제하시겠습니까?')) {
        await fetch(`/api/tweet/${id}`, { method: 'DELETE' });
        renderTweets();
    }
}

async function renderTweets() {
    const user = await fetchMe();
    const tweets = await fetchTweets();

    const tweetsDiv = document.getElementById('tweets');
    tweetsDiv.innerHTML = '';

    tweets.forEach(tweet => {
        const div = document.createElement('div');
        div.className = 'tweet';

        div.innerHTML = `
            <div class="tweet-body-row">
                <p class="tweet-content">${tweet.content}</p>
                ${user && user.id === tweet.user_id ? `
                    <form onsubmit="event.preventDefault(); deleteTweet(${tweet.id});" class="delete-form">
                        <button type="submit">X</button>
                    </form>
                ` : ''}
            </div>
            <p class="tweet-author">- ${tweet.username} -</p>
            <div class="tweet-actions">
                ${user ? `
                    ${tweet.liked_by_current_user ? `
                        <button onclick="unlikeTweet(${tweet.id})">Unlike</button>
                    ` : `
                        <button onclick="likeTweet(${tweet.id})">Like</button>
                    `}
                ` : `
                    <p><a href="/login.html">Log in to like</a></p>
                `}
                <span class="likes-count">Likes: ${tweet.likes_count}</span>
            </div>
        `;

        tweetsDiv.appendChild(div);
    });
}

document.addEventListener('DOMContentLoaded', renderTweets);
