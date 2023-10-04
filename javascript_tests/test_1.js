let x = 10
let y = 5
console.log("Testing the arithmetic operations:")
console.log(`x + y is equal to ${x + y}`);  // Addition 15
console.log(`x - y is equal to ${x - y}`);  // Subtraction 5
console.log(`x * y is equal to ${x * y}`);  // Multiplication 50
console.log(`x / y is equal to ${x / y}`);  // Division 2
// the same result can be obtained by assignment operators (+=, -=, *=, /=)
console.log("Performing the same operations but with assignment operators we get as results:")
x += y;
console.log(`x += y is equal to ${x}`);  // 15
x = 10; // reassigning x to 10
x -= y;
console.log(`x -= y is equal to ${x}`);  // 10
x = 10; // reassigning x to 10
x *= y;
console.log(`x *= y is equal to ${x}`);  // 50
x = 10; // reassigning x to 10
x /= y;
console.log(`x /= y is equal to ${x}`);  // 10

// examples of type coercion
console.log("Some examples of type coercion (implicit casting performed on data):")
console.log(`Addition of string and number "10" + 5 : ${"10" + 5}`);  // "105"
console.log(`Substraction of string and number "10" - 5 : ${"10" - 5}`);  // 5
console.log(`Multiplication of string and number "10" * 5 : ${"10" * 5}`);  // 50
console.log(`Division of string and number "10" / 5 : ${"10" / 5}`);  // 2
// examples of NaN
console.log("Some examples of combining a string with a number:")
console.log(`Addition of string and number "hello" + 5 : ${"hello" + 5}`);  // "hello5"
console.log(`Subtraction of string and number "hello" - 5 : ${"hello" - 5}`);  // NaN
console.log(`Multiplication of string and number "hello" * 5 : ${"hello" * 5}`);  // NaN
console.log(`Division of string and number "hello" / 5 : ${"hello" / 5}`);  // NaN

 // Relational operators
console.log("Testing the relational operators:")
console.log(`x > y is equal to ${x > y}`);  // true
console.log(`x < y is equal to ${x < y}`);  // false
console.log(`x >= y is equal to ${x >= y}`);  // true
console.log(`x <= y is equal to ${x <= y}`);  // false

let a = "10"
let b = '5'

console.log("testing equality between strings and numbers")
console.log("Testing the equality operators:") // Equality operators
console.log(`x == a is equal to ${x == a}`);  // true
console.log(`y != b is equal to ${y != b}`);  // false
console.log("Testing the strict equality operators:")
console.log(`x === a is equal to ${x === a}`);  // false
console.log(`y !== b is equal to ${y !== b}`);  // true