// input a mark and say if the exam is passed or not
continue_condition = true
let mark;
while (continue_condition === true) {
    mark = prompt("Please enter your mark: ");
    if (mark >= 0 && mark <= 30) {
        console.log(`Your mark is valid : ${mark}`);
        continue_condition = false // valid input, we can accept it
    } else {
        console.log("Invalid input, please try again");
    }
}
console.log(mark)
if (mark >= 18 && mark <= 22) {
    console.log("You passed the exam with sufficient mark");
} else if (mark >= 23 && mark <= 26){
    console.log("You passed the exam with good mark");
}
else if (mark >= 27 && mark <= 30) {
    console.log("You passed the exam with very good mark");
}
else {
    console.log("You failed the exam");
}

// insert an array of marks
continue_condition = true
let marks = []
let i = 0
while (continue_condition === true) {
    let temp = prompt("Do you want to insert a mark? (Y/N): ");
    if (temp == "Y" || temp == "y") {
        let mark = prompt("Please enter a mark between 1 and 30: ");
        if (mark >= 0 && mark <= 30) {
        console.log(`Your mark is valid : ${mark}`);
        marks[i] = mark
        i++
    } else {
        console.log("Invalid input, please try again");
    }
    }
    else {continue_condition = false}
}
// print the array
console.log(`The marks inserted are ${marks}`)
console.log(`The number of marks inserted is ${marks.length}`)
console.log("Computing the number of sufficient and insufficient marks with a function")

function count_sufficient_marks(marks) {
    n_marks = marks.length
    n_sufficient_marks = 0
    n_unsufficient_marks = 0
    i = 0
    while(i < n_marks) {
        if (marks[i] >= 18) {
            n_sufficient_marks++
        } else {
            n_unsufficient_marks++
        }
        i++
    }
    return [n_sufficient_marks, n_unsufficient_marks]
}

count = count_sufficient_marks(marks)
console.log(`The number of sufficient marks is ${count[0]}`)
console.log(`The number of insufficient marks is ${count[1]}`)
