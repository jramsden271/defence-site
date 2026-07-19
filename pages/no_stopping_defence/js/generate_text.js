function generateText() {

    // All named, value-bearing form fields (see js/form_variables.js,
    // auto-generated from the Python form definition).
    const formValues = collectFormValues();

    // Read the selected pronoun (male / female / neutral).
    const pronoun = formValues.pronouns || "neutral";
    const subjectPronoun = pronoun === "male" ? "he" : pronoun === "female" ? "she" : "they";
    const objectPronoun = pronoun === "male" ? "him" : pronoun === "female" ? "her" : "them";
    const was_or_were = pronoun === "neutral" ? "were" : "was";

    const incidentDateVal = formValues.incidentDate;
    const issueDateVal = formValues.ntkDate;

    let pofaResult = null;
    if (issueDateVal !== null && issueDateVal !== "") {
        pofaResult = isNoticeToKeeperInTime(incidentDateVal, issueDateVal);
    }

    const paragraphs = [];
    paragraphs.push(`Liability is denied for the sum claimed, or at all. Except where explicitly admitted, the Particulars of Claim (POC) are denied in their entirety.`);
    paragraphs.push(`The Defendant ${was_or_were} not the driver of the vehicle at the time of the alleged incident, and ${subjectPronoun} did not commit any of the alleged acts or omissions described in the POC.`);
    paragraphs.push(`The POC relates to an event on ${incidentDateVal}, which is outside the statutory time limit for issuing a Notice to Keeper. The Defendant ${was_or_were} not aware of any incident on that date, and ${subjectPronoun} did not receive any Notice to Keeper within the required timeframe.`);

    renderDefenceOutput(paragraphs, pofaResult);
}
