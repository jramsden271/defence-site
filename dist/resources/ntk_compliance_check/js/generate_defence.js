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
            ? ` (the NtK gives the location only as "${incidentAddressVal}")`
            : "";
        paragraphs.push(`The Notice to Keeper attempts to specify the land on which the vehicle was parked, but does so too vaguely${locationDescription}. A valid NtK must clearly and accurately identify the relevant land, so this is a defect that may prevent liability transferring from the driver to the keeper.`);
    }

    if (paragraphs.length === 0) {
        paragraphs.push(`Based on the answers given, no defects were identified with this Notice to Keeper under the requirements checked by this tool. This is not a guarantee that the NtK is fully compliant with PoFA 2012 — always review the NtK carefully and seek advice specific to your situation.`);
    }

    renderDefenceOutput(paragraphs, pofaResult);
}
