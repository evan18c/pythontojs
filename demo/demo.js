// Runs the demo
function demo() {
    let input = document.getElementById("pythonInput");
    let consoleDiv = document.getElementById("console");
    try {
        consoleDiv.innerText = "";
        console.log = function (arg) {
            consoleDiv.innerText += `${String(arg)}\n`;
        }
        python(input.value+'\n');
    } catch (e) {
        consoleDiv.innerText = `Error: ${e}`;
    }
}

// Tabs
window.onload = function() {
    let input = document.getElementById("pythonInput");
    input.addEventListener("keydown", (e) => {
        if (e.key === "Tab") {
            e.preventDefault();
            let start = input.selectionStart;
            let end = input.selectionEnd;
            input.value = input.value.substring(0, start) + "    " + input.value.substring(end);
            input.selectionStart = input.selectionEnd = start + 4;
        }
    });
}