function number_inc() {
    console.log("+1 버튼 클릭");

    result = document.getElementById("result");

    let current = parseInt(result.innerText, 10);

    console.log("현재값: " + current);
    current = current + 1;
    console.log("덧셈이후: " + current);

    result.innerText = current;
}

function number_dec() {
    console.log("-1 버튼 클릭");

    result = document.getElementById("result");
    result.innerText = parseInt(result.innerText, 10) - 1;
}
