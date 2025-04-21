document.addEventListener("DOMContentLoaded", function () {
    const today = new Date();
    const formattedToday = today.toISOString().split("T")[0];

    // Select start date input field
    const startDateInput = document.querySelector("#id_offer_start_date");
    if (startDateInput) {
        startDateInput.setAttribute("min", formattedToday);
        startDateInput.addEventListener("change", function () {
            if (endDateInput) {
                endDateInput.setAttribute("min", startDateInput.value);
            }
        });
    }

    // Select end date input field
    const endDateInput = document.querySelector("#id_offer_end_date");
    if (endDateInput) {
        endDateInput.setAttribute("min", formattedToday);
    }
});
