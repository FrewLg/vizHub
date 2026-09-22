document.addEventListener("DOMContentLoaded", function () {

    const filters = JSON.parse(
        document.getElementById(
            "enabled-filters"
        ).textContent
    );

    const allFilters = [
        "year",
        "location",
        "sex",
        "age_group",
        "cause",
        "facility_category"
    ];

    allFilters.forEach(filter => {

        const el = document.getElementById(
            `filter-${filter}`
        );

        if (!el) return;

        if (filters.includes(filter)) {
            el.classList.remove("hidden");
        } else {
            el.classList.add("hidden");
        }
    });
});