// Shared output-box behaviour for every defence_generator page: reads the
// current form answers, resets the output box, renders an optional PoFA
// result line and the defence paragraphs, and reveals the box.
//
// Expects the output_box.html markup (#output-box, #paragraphsContainer,
// #pofaResultsContainer, #copyBtn, #charCount) and form_variables.js's
// collectFormValues().
//
// A page's own generate_defence.js should call this instead of touching
// the output box directly:
//
//     function generateDefence() {
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

// Toggles the visibility of elements marked with `data-depends-on`/
// `data-value` attributes, based on the current answer of the field whose
// `data-trigger` id they reference. Works for any form on the page — not
// tied to a specific form id — via a single delegated `change` listener.
document.addEventListener('change', function (event) {
    // 1. Find if the changed field belongs to a managed trigger group
    const triggerContainer = event.target.closest('[data-trigger]');
    if (!triggerContainer) return;

    const triggerId = triggerContainer.getAttribute('data-trigger');

    // 2. Safely grab the current value whether it's a dropdown or a radio button
    const currentValue = event.target.type === 'radio'
        ? triggerContainer.querySelector('input:checked').value
        : event.target.value;

    // 3. Find and toggle all dependent elements instantly
    document.querySelectorAll(`[data-depends-on="${triggerId}"]`).forEach(field => {
        const targetValue = field.getAttribute('data-value');

        // If values match, set display to 'block', otherwise set it to 'none'
        field.style.display = (currentValue === targetValue) ? 'block' : 'none';
    });
});

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

/**
 * Calculates if a Notice to Keeper (NTK) sent by post was served in time 
 * under PoFA 2012 Schedule 4 (Paragraph 9).
 * 
 * @param {string|Date} incidentDate - The date the parking contravention occurred.
 * @param {string|Date} issueDate - The date printed on the NTK (assumed date of posting).
 * @returns {Object} An object detailing whether it was in time, the deadlines, and the math.
 */
function isNoticeToKeeperInTime(incidentDate, issueDate) {
    const incident = new Date(incidentDate);
    const posted = new Date(issueDate);
    
    // Normalize times to midday to ensure clean day-by-day arithmetic
    //incident.setHours(12,0,0,0);
    //posted.setHours(12,0,0,0);

    // Rule: The 14-day window begins the day AFTER the incident
    const targetReceivedDeadline = new Date(incident);
    targetReceivedDeadline.setDate(targetReceivedDeadline.getDate() + 14);

    // Calculate Deemed Service (2 working days after posting)
    let workingDaysAdded = 0;
    const deemedReceivedDate = new Date(posted);

    while (workingDaysAdded < 2) {
        deemedReceivedDate.setDate(deemedReceivedDate.getDate() + 1);
        const dayOfWeek = deemedReceivedDate.getDay();
        
        // 0 = Sunday, 6 = Saturday. Only count Mon-Fri as working days.
        if (dayOfWeek !== 0 && dayOfWeek !== 6) {
            workingDaysAdded++;
        }
    }

    // Is the deemed received date on or before the 14-day deadline?
    const isInTime = deemedReceivedDate <= targetReceivedDeadline;

    return {
        isInTime: isInTime,
        incidentDate: incident.toISOString().split('T')[0],
        issueDate: posted.toISOString().split('T')[0],
        deemedReceivedDate: deemedReceivedDate.toISOString().split('T')[0],
        latestAllowedReceivedDate: targetReceivedDeadline.toISOString().split('T')[0],
        daysLate: isInTime ? 0 : Math.ceil((deemedReceivedDate - targetReceivedDeadline) / (1000 * 60 * 60 * 24))
    };
}

// ==========================================
// EXAMPLES OF USE
// ==========================================

// Example 1: Issued quickly (In Time)
// Incident on a Monday, issued 4 days later on Friday.
// Deemed received on Tuesday (2 working days skipping Sat/Sun). 
console.log(isNoticeToKeeperInTime("2026-07-06", "2026-07-10")); 
/* Output:
{
  isInTime: true,
  incidentDate: '2026-07-06',
  issueDate: '2026-07-10',
  deemedReceivedDate: '2026-07-14',
  latestAllowedReceivedDate: '2026-07-20',
  daysLate: 0
}
*/

// Example 2: Issued way too late (Late)
// Incident on July 1st, but notice isn't issued until July 15th.
console.log(isNoticeToKeeperInTime("2026-07-01", "2026-07-15"));
/* Output:
{
  isInTime: false,
  incidentDate: '2026-07-01',
  issueDate: '2026-07-15',
  deemedReceivedDate: '2026-07-17',
  latestAllowedReceivedDate: '2026-07-15',
  daysLate: 2
}
*/
// Wires up the header's dark/light theme toggle button. The initial theme
// itself is already set on <html data-theme="..."> by the inline init
// script in <head> (before this file even loads) — this just handles clicks.

function setThemeIcon(button, theme) {
    button.textContent = theme === 'dark' ? '☀️' : '🌙';
    button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    setThemeIcon(toggle, document.documentElement.getAttribute('data-theme'));

    toggle.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        setThemeIcon(toggle, next);
    });
});

function generateDefence() {

    // All named, value-bearing form fields (see js/form_variables.js,
    // auto-generated from the Python form definition).
    const formValues = collectFormValues();

    const incidentDateVal = formValues.incidentDate;
    const issueDateVal = formValues.ntkDate;

    let pofaResult = null;
    if (incidentDateVal && issueDateVal) {
        pofaResult = isNoticeToKeeperInTime(incidentDateVal, issueDateVal);
    }

    const paragraphs = [];

    if (pofaResult !== null && !pofaResult.isInTime) {
        paragraphs.push(`The Notice to Keeper was not served within the statutory time limit under PoFA 2012 Schedule 4. It was deemed received on ${pofaResult.deemedReceivedDate}, which is after the latest allowed date of ${pofaResult.latestAllowedReceivedDate}. As a result, liability cannot be transferred from the driver to the keeper.`);
    }

    if (formValues.ntkHasParkingPeriod === "no") {
        paragraphs.push(`The Notice to Keeper does not specify a parking period. A valid NtK must show the period during which the vehicle was parked, so this is a defect that may prevent liability transferring from the driver to the keeper.`);
    }

    if (formValues.ntkCompliesWithPara94 === "no") {
        paragraphs.push(`The Notice to Keeper does not comply with PoFA 2012 Schedule 4 paragraph 9(4). It does not correctly warn the keeper that, if the parking charge remains unpaid and the driver's details are not known to the creditor after 28 days, the creditor will have the right to recover the charge from the keeper. This is a defect that may prevent liability transferring from the driver to the keeper.`);
    }

    if (formValues.ntkStatesLand === "wrong" || formValues.ntkStatesLand === "no") {
        paragraphs.push(`The Notice to Keeper does not correctly specify the land on which the vehicle was parked. A valid NtK must clearly and accurately identify the relevant land, so this is a defect that may prevent liability transferring from the driver to the keeper.`);
    }

    if (formValues.ntkStatesLand === "vaguely") {
        const incidentAddressVal = formValues.ntkIncidentAddress;
        const locationDescription = incidentAddressVal
            ? `The NtK gives the location only as '${incidentAddressVal}', making it impossible to ascertain the exact location of the vehicle and the contract the vehicle allegedly contravened. `
            : "";
        paragraphs.push(`The Notice to Keeper attempts to specify the land on which the vehicle was parked, but does so too vaguely. ${locationDescription}A valid NtK must clearly and accurately identify the relevant land, so this is a defect that may prevent liability transferring from the driver to the keeper.`);
    }

    /*
    if (paragraphs.length === 0) {
        paragraphs.push(`Based on the answers given, no defects were identified with this Notice to Keeper under the requirements checked by this tool. This is not a guarantee that the NtK is fully compliant with PoFA 2012 — always review the NtK carefully and seek advice specific to your situation.`);
    }
        */

    renderDefenceOutput(paragraphs, pofaResult);
}

// Auto-generated by builder/field_manifest.py — do not edit by hand.
// Regenerated fresh on every build.
//
// Lists every named, value-bearing field rendered into the form, so
// a page's generate-defence JS can read current answers without
// hardcoding each field's name/id by hand. Radio fields also list
// their `options` (the possible values), so callers can see the
// answer set without hardcoding it either.

const FORM_FIELDS = [
  {
    "kind": "date",
    "id": "incidentDate"
  },
  {
    "kind": "date",
    "id": "ntkDate"
  },
  {
    "kind": "radio",
    "name": "ntkHasParkingPeriod",
    "options": [
      "yes",
      "no",
      "notsure"
    ]
  },
  {
    "kind": "radio",
    "name": "ntkCompliesWithPara94",
    "options": [
      "yes",
      "no"
    ]
  },
  {
    "kind": "radio",
    "name": "ntkStatesLand",
    "options": [
      "yes",
      "vaguely",
      "wrong",
      "no"
    ]
  },
  {
    "kind": "text",
    "id": "ntkIncidentAddress"
  }
];

// Reads current answers for each field in FORM_FIELDS from the DOM.
// Returns { [name or id]: value }; unanswered radios are null.
function collectFormValues() {
    const values = {};
    FORM_FIELDS.forEach(field => {
        if (field.kind === 'radio') {
            const checked = document.querySelector(
                `input[name="${field.name}"]:checked`
            );
            values[field.name] = checked ? checked.value : null;
        } else {
            const el = document.getElementById(field.id);
            values[field.id] = el ? el.value.trim() : null;
        }
    });
    return values;
}
