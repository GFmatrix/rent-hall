document.addEventListener("DOMContentLoaded", function() {
    let timeout; // Variable to hold the timeout reference

    function formatPhoneNumber(event) {
        const input = event.target; // Get the input element from the event

        clearTimeout(timeout); // Clear any existing timeout

        timeout = setTimeout(function() {
            let value = input.value.replace(/\D/g, ''); // Remove all non-digits

            // Format the number in (90) 123 00 00
            if (value.length > 2) {
                value = `(${value.slice(0, 2)}) ${value.slice(2, 5)} ${value.slice(5, 7)} ${value.slice(7, 9)}`;
            } else if (value.length > 0) {
                value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
            }

            input.value = value;
        }, 500); // Delay in milliseconds (e.g., 300ms)
    }

    const phoneInput = document.getElementById('id_phone_number');
    phoneInput.addEventListener('input', formatPhoneNumber); // Use 'input' event
});