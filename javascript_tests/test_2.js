// input prompt
console.log("Enter two numbers: ");
let a = prompt("Enter a number: ");
let b = prompt("Enter another number: ");

// declare functions
function add(a, b) {return a + b;}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a*b;
}

function divide(a, b) {
    return a/b;
}

/* this is a
multiline comment */

let add_a_b = add(a, b);
let subtract_a_b = subtract(a, b);
let multiply_a_b = multiply(a, b);
let divide_a_b = divide(a, b);

// call functions
console.log(`The sum of ${a} and ${b} is ${add_a_b}`);
console.log(`The difference of ${a} and ${b} is ${subtract_a_b}`);
console.log(`The product of ${a} and ${b} is ${multiply_a_b}`);
console.log(`The quotient of ${a} and ${b} is ${divide_a_b}`);

let c = 10;

function operate(a, b){
    let d = add(a, b)
    let e = multiply(a, b)
    c = subtract(a, b)  // c is a global variable and it is modified
    a = divide(a, b)    // a is a global variable, but it is not modified because it has the same binding as one of the formal parameter of the function
    b = 100
    return [a, b, c, d, e]  // return an array
}

array = operate(a, b);

console.log("the variables after the function 'operate' is called are: ")
console.log(`the array returned by the function 'operate' is: ${array}`)
console.log("the length of the array returned by the function 'operate' is array.length = " + array.length)
console.log(`global variable a =  ${a}  (not modified by the function 'operate')`)
console.log(`global variable b =  ${b}  (not modified by the function 'operate')`)
console.log(`global variable c =  ${c}  (modified by the function 'operate')`)
console.log(`local variable a =  ${array[0]} (note that it is different from the global variable a)`)
console.log(`local variable b =  ${array[1]} (note that it is different from the global variable b)`)
console.log(`local variable c =  ${array[2]}  (note that it is the same as the global variable c)`)
console.log(`local variable d =  ${array[3]}`)
console.log(`local variable e =  ${array[4]}`)
console.log(`if you try to access an element of the array that is not defined, you get undefined: array[5] = ${array[5]}`)