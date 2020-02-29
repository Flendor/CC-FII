function doHomework(subject, callback) {
    console.log(`Starting my ${subject} homework!`);
    callback()
}

function anunt() {
    console.log("Finished my homework!")
}

doHomework('math', anunt);
