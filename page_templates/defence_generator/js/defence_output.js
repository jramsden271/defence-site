// Shared output-box behaviour for every defence_generator page: reads the
// current form answers, resets the output box, renders an optional PoFA
// result line and the defence paragraphs, and reveals the box.
//
// Expects the output_box.html markup (#output-box, #paragraphsContainer,
// #pofaResultsContainer, #copyBtn, #charCount) and form_variables.js's
// collectFormValues().
//
// A page's own generate_text.js should call this instead of touching the
// output box directly:
//
//     function generateText() {
//         const formValues = collectFormValues();
//         ... build `paragraphs` (array of strings) ...
//         ... optionally compute `pofaResult` via isNoticeToKeeperInTime() ...
//         renderDefenceOutput(paragraphs, pofaResult);
//     }

// Tracks the raw plain text for copy_to_clipboard.js to read.
let rawPlainTextOutput = "";

function renderDefenceOutput(paragraphs, pofaResult = null) {
    const outputBox = document.getElementById('output-box');
    const container = document.getElementById('paragraphsContainer');
    const pofaResultsContainer = document.getElementById('pofaResultsContainer');
    const copyBtn = document.getElementById('copyBtn');
    const charCountElement = document.getElementById('charCount');

    // Reset UI state
    outputBox.style.display = 'none';
    container.innerHTML = "";
    pofaResultsContainer.innerHTML = "";
    copyBtn.textContent = "Copy Text";
    charCountElement.textContent = "Character Count: 0";

    if (pofaResult !== null) {
        const resultElement = document.createElement('p');
        resultElement.textContent = `Notice to Keeper In Time: ${pofaResult.isInTime ? "Yes" : "No"} (Deemed Received Date: ${pofaResult.deemedReceivedDate}, Latest Allowed Received Date: ${pofaResult.latestAllowedReceivedDate})`;
        pofaResultsContainer.appendChild(resultElement);
    }

    // Render paragraphs & build the plain-text copy
    let textToCopyBuilder = "";

    paragraphs.forEach((paraText, index) => {
        const paragraphNumber = index + 1;
        const formattedSentence = `${paragraphNumber}. ${paraText}`;

        const pElement = document.createElement('p');
        pElement.className = "story-paragraph";
        pElement.textContent = formattedSentence;
        container.appendChild(pElement);

        textToCopyBuilder += formattedSentence + "\n\n";
    });

    rawPlainTextOutput = textToCopyBuilder.trim();
    charCountElement.textContent = `Character Count: ${rawPlainTextOutput.length}`;

    // Reveal result window
    outputBox.style.display = 'block';
}
