// Copies the page's generated plain-text output to the clipboard, giving
// visual feedback on the triggering button.
//
// Expects a global `rawPlainTextOutput` string (set by
// defence_output.js's renderDefenceOutput()) and a button with
// id="copyBtn" to update on success.
function copyToClipboard() {
    const copyBtn = document.getElementById('copyBtn');

    // Check if there is data to copy
    if (!rawPlainTextOutput) return;

    // Use browser clipboard API
    navigator.clipboard.writeText(rawPlainTextOutput)
        .then(() => {
            // Visual feedback change to indicate success
            copyBtn.textContent = "Copied! ✓";
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
            alert("Could not copy text automatically. Please select it manually.");
        });
}
