async function download() {
    const url = document.getElementById("url").value.trim();
    const format = document.getElementById("format").value;
    if (!url) return alert("Please paste a YouTube link!");

    const status = document.getElementById("status");
    const result = document.getElementById("result");
    status.innerHTML = "Processing... This may take 10–60 seconds";
    result.innerHTML = "";

    try {
        const res = await fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url, format })
        });

        const data = await res.json();

        if (data.success) {
            status.innerHTML = "Ready!";
            result.innerHTML = `<a href="${data.file}" download>Click here to download: ${data.title}</a>`;
        } else {
            status.innerHTML = "Error: " + data.error;
        }
    } catch (e) {
        status.innerHTML = "Server offline or blocked. Try again later.";
    }
}
