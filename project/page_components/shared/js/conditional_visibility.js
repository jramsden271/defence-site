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
