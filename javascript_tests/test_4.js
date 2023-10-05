// This script shows some examples of lexical errors managed by the interpreter
let a = 1;
// Lexical error: the keyword is not correct due to a typo
whole(a<10){
    console.log("a is less than 10")
    a++
}
// another lexical error, but the script will not reach this statement since the previous one is wrong and the error will be thrown
cons c = 10