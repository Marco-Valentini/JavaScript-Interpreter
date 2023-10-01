let isTrue = true;
let isFalse = false;

console.log(isTrue && isFalse);  // Logical AND
console.log(isTrue || isFalse);  // Logical OR
console.log(!isTrue);            // Logical NOT
console.log(!isFalse);           // Logical NOT

// examples of type coercion
console.log("hello" && 5);  // 5
console.log("hello" || 5);  // "hello"
console.log(!"hello");      // false
console.log(!"");           // true
