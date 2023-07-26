// if-else
let score = 80;

if (score >= 90) {
    console.log('A');
} else if (score >= 80) {
    console.log('B');
} else {
    console.log('C');
}


// for loop
for (let i = 1; i <= 5; i++) {
    console.log(i);
}

let numbers = [1, 2, 3, 4, 5];
numbers.forEach(function(number) {
    console.log(number);
});
numbers.forEach((number) => {
  console.log(number);
});


// 함수
function greet(name) {
    console.log('Hello, ' + name + '!');
}
  
greet('John');
  
function addNumbers(a, b) {
    return a + b;
}
  
let sum = addNumbers(5, 3);
console.log(sum);


// 객체
let person = {
    name: 'John',
    age: 25,
    greet: function() {
        console.log('Hello, ' + this.name + '!');
    }
};
  
console.log(person.name);
console.log(person.age);
person.greet();
