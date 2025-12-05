const commandInput = document.getElementById("command");
const output = document.getElementById("output");

commandInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        e.preventDefault(); // مهم جداً لإيقاف إعادة تحميل الصفحة
        const cmd = commandInput.value;
        output.innerHTML += "$ " + cmd + "\n";
        commandInput.value = "";

        fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: cmd }) // لاحظ اسم key: command
        })
        .then(res => res.json())
        .then(data => {
            output.innerHTML += data.output + "\n";
            output.scrollTop = output.scrollHeight;
        });
    }
});
