let currentPage = 1;
const recordsPerPage = 5;

/** @returns {HTMLElement[]} All descriptions. */
function getDescriptions() {
    return Array.from(
        document.getElementsByClassName(
            "description"
        )
    );
}

/**
 * Highlight matching portion of a reference.
 * @param {string} ref Catalogue reference.
 * @param {string} query Search term.
 * @returns {string} HTML with highlighted match.
 */
function highlightReference(ref, query) {

    if (!query) {
        return ref;
    }

    const start =
        ref.toUpperCase()
           .indexOf(
               query.toUpperCase()
           );

    if (start === -1) {
        return ref;
    }

    const end = 
        start + query.length;

    return (
        ref.substring(0, start) +
        '<span class="highlight">' +
        ref.substring(start, end) +
        '</span>' +
        ref.substring(end)
    );
}

/**
 * Render a page of visible descriptions.
 * @param {number} page 1-based page number.
 */
function showPage(page) {

    const descriptions = 
        getDescriptions();

    const visible = 
        descriptions.filter(
            s => !s.classList.contains(
                "hidden"
            )
        );
    const totalPages = 
        Math.max(
            1, 
            Math.ceil(
                visible.length / recordsPerPage)
        );
    page = 
        Math.max(
            1, 
            Math.min(page, totalPages)
        );
    currentPage = page;

    descriptions.forEach(
        s => s.style.display = "none"
    );

    const start = 
        (page - 1) * recordsPerPage;
    const end = 
        start + recordsPerPage;

    visible
        .slice(start, end)
        .forEach(
            s => s.style.display = "block"
        );

    // document.getElementById("pageInfo").textContent = `Page ${page} of ${totalPages}`;
    const pageText =
        `Page ${page} of ${totalPages}`;

    const topInfo =
        document.getElementById("pageInfoTop");

    const bottomInfo =
        document.getElementById("pageInfoBottom");

    if (topInfo) {
        topInfo.textContent = pageText;
    }

    if (bottomInfo) {
        bottomInfo.textContent = pageText;
    }
}

function searchDescriptions() {
    const query = document
        .getElementById("searchBox")
        .value
        .trim()
        .toUpperCase();
    const descriptions = 
        getDescriptions();

    descriptions.forEach(description => {
        const ref = 
            description.getAttribute("data-ref") || "";

        const matches =
            query === "" ||
            ref.toUpperCase().includes(query);

        const title = 
            description.querySelector(".title");

        if (matches) {
            description.classList.remove("hidden");
            if (title) {
                title.innerHTML = highlightReference(ref, query);
            }

        } else {
            description.classList.add("hidden");
        }

    });

    showPage(1);
}

function goToNextPage() {
    showPage(currentPage + 1);
}

function goToPreviousPage() {
    showPage(currentPage - 1);
}

/**
 * Scroll to selected reference.
 * @param {string} ref Catalogue reference.
 */
function jumpToRef(ref) {

    if (!ref) {
        return;
    }

    const descriptions =
        getDescriptions();

    const target =
        descriptions.find(
            d => d.getAttribute("data-ref") === ref
        );

    if (!target) {
        return;
    }

    const index =
        descriptions.indexOf(target);

    const page =
        Math.floor(index / recordsPerPage) + 1;

    showPage(page);

    target.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}
/** Initialise page on load. */
window.onload = function () {
    showPage(1);
};