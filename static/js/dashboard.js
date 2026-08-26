document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("productSearch");
    const riskFilter = document.getElementById("riskFilter");
    const resultCount = document.getElementById("resultCount");
    const noResults = document.getElementById("noResults");

    const tableRows = document.querySelectorAll(".product-row");
    const summaryCards = document.querySelectorAll(".summary-card");

    function filterProducts() {
        const searchValue = searchInput
            ? searchInput.value.toLowerCase().trim()
            : "";

        const selectedRisk = riskFilter
            ? riskFilter.value.toLowerCase()
            : "all";

        let visibleCount = 0;

        tableRows.forEach((row) => {
            const rowText = row.textContent
                .toLowerCase()
                .trim();

            /*
             * Overall Risk is the 8th table column.
             * Array index starts from 0, therefore index 7.
             */
            const overallRiskCell = row.cells[7];

            const overallRisk = overallRiskCell
                ? overallRiskCell.textContent
                    .toLowerCase()
                    .trim()
                : "";

            const matchesSearch =
                searchValue === "" ||
                rowText.includes(searchValue);

            const matchesRisk =
                selectedRisk === "all" ||
                overallRisk.includes(selectedRisk);

            if (matchesSearch && matchesRisk) {
                row.style.display = "";
                visibleCount++;
            } else {
                row.style.display = "none";
            }
        });

        if (resultCount) {
            resultCount.textContent =
                `Showing ${visibleCount} of ${tableRows.length} products`;
        }

        if (noResults) {
            noResults.style.display =
                visibleCount === 0 ? "block" : "none";
        }
    }


    /*
     * Search while typing.
     */
    if (searchInput) {
        searchInput.addEventListener(
            "input",
            filterProducts
        );
    }


    /*
     * Filter using dropdown.
     */
    if (riskFilter) {
        riskFilter.addEventListener(
            "change",
            filterProducts
        );
    }


    /*
     * Make the Critical / High / Medium / Low
     * summary cards clickable.
     */
    summaryCards.forEach((card) => {
        card.addEventListener("click", () => {

            const riskClasses = [
                "critical",
                "high",
                "medium",
                "low"
            ];

            let selectedRisk = "";

            for (const risk of riskClasses) {
                if (card.classList.contains(risk)) {
                    selectedRisk = risk;
                    break;
                }
            }

            if (riskFilter && selectedRisk) {
                riskFilter.value = selectedRisk;
            }

            /*
             * Remove active state from all cards.
             */
            summaryCards.forEach((item) => {
                item.classList.remove("active");
            });

            /*
             * Highlight selected card.
             */
            card.classList.add("active");

            filterProducts();
        });
    });


    /*
     * Clicking "All Risks" removes
     * the active card.
     */
    if (riskFilter) {
        riskFilter.addEventListener("change", () => {

            if (riskFilter.value.toLowerCase() === "all") {
                summaryCards.forEach((card) => {
                    card.classList.remove("active");
                });
            }

            filterProducts();
        });
    }


    /*
     * Run filtering once when page loads.
     */
    filterProducts();
});
EOF