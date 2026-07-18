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