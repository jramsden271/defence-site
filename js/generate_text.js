        // We track a global variable to store raw plain text for clean copying
        let rawPlainTextOutput = "";

        function generateText() {

            // Get page elements
            const outputBox = document.getElementById('output-box');
            const container = document.getElementById('paragraphsContainer');
            const pofaResultsContainer = document.getElementById('pofaResultsContainer');
            const copyBtn = document.getElementById('copyBtn');

            // All named, value-bearing form fields (see js/form_variables.js,
            // auto-generated from the Python form definition).
            const formValues = collectFormValues();

            // Read the selected pronoun (male / female / neutral).
            const pronoun = formValues.pronouns || "neutral";
            const subjectPronoun = pronoun === "male" ? "he" : pronoun === "female" ? "she" : "they";
            const objectPronoun = pronoun === "male" ? "him" : pronoun === "female" ? "her" : "them";
            const was_or_were = pronoun === "neutral" ? "were" : "was";

            const incidentDateVal = formValues.incidentDate;

            //console.log("Incident Date:", incidentDateVal);

            const issueDateVal = formValues.ntkDate;

            var isInTimeResult = null;
            if (issueDateVal !== null && issueDateVal !== "") {
                isInTimeResult = isNoticeToKeeperInTime(incidentDateVal, issueDateVal);

                //console.log("Is Notice to Keeper in Time Result:", isInTimeResult);
            }


            


            // Reset UI states
            //nameInput.classList.remove('input-error');
            //nameError.style.display = 'none';
            outputBox.style.display = 'none';
            container.innerHTML = ""; 
            pofaResultsContainer.innerHTML = "";
            copyBtn.textContent = "Copy Text"; // Reset copy button text if run again

            document.getElementById('charCount').textContent = "Character Count: 0";

            if (isInTimeResult !== null) {
                const resultElement = document.createElement('p');
                resultElement.textContent = `Notice to Keeper In Time: ${isInTimeResult.isInTime ? "Yes" : "No"} (Deemed Received Date: ${isInTimeResult.deemedReceivedDate}, Latest Allowed Received Date: ${isInTimeResult.latestAllowedReceivedDate})`;
                pofaResultsContainer.appendChild(resultElement);
                
            }

            // --- VALIDATION CHECK example ---
            /*
            if (username === "") {
                nameInput.classList.add('input-error');
                nameError.style.display = 'block';
                nameInput.focus();
                return;
            }
                */


            const paragraphs = [];
            paragraphs.push(`Liability is denied for the sum claimed, or at all. Except where explicitly admitted, the Particulars of Claim (POC) are denied in their entirety.`);
            paragraphs.push(`The Defendant ${was_or_were} not the driver of the vehicle at the time of the alleged incident, and ${subjectPronoun} did not commit any of the alleged acts or omissions described in the POC.`);
            paragraphs.push(`The POC relates to an event on ${incidentDateVal}, which is outside the statutory time limit for issuing a Notice to Keeper. The Defendant ${was_or_were} not aware of any incident on that date, and ${subjectPronoun} did not receive any Notice to Keeper within the required timeframe.`);








            // --- RENDER TEXT & BUILD PLAIN TEXT COPY ---
            let textToCopyBuilder = "";

            paragraphs.forEach((paraText, index) => {
                const paragraphNumber = index + 1;
                const formattedSentence = `${paragraphNumber}. ${paraText}`;

                // 1. Create a dynamic HTML element to display beautifully on the page
                const pElement = document.createElement('p');
                pElement.className = "story-paragraph";
                pElement.textContent = formattedSentence;
                container.appendChild(pElement);

                // 2. Accumulate standard plain text string lines separated by double spacing
                textToCopyBuilder += formattedSentence + "\n\n";
            });

            // Store the clean, plain text copy string without HTML tags inside it
            rawPlainTextOutput = textToCopyBuilder.trim();

            const charCountElement = document.getElementById('charCount');
            charCountElement.textContent = `Character Count: ${rawPlainTextOutput.length}`;

            // Reveal result window
            outputBox.style.display = 'block';
        }