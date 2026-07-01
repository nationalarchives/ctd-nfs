var currentPage = 1;
var pageSize = 50;

function getSnippets() {
    return Array.from(document.getElementsByClassName('snippet'));
}

function showPage(page) {
    var snippets = getSnippets();
    currentPage = page;

    var visible = snippets.filter(function (s) {
        return !s.classList.contains('hidden');
    });

    snippets.forEach(function (s) {
        s.style.display = 'none';
    });

    var start = (page - 1) * pageSize;
    var end = start + pageSize;

    visible.slice(start, end).forEach(function (s) {
        s.style.display = 'block';
    });

    var totalPages = Math.max(1, Math.ceil(visible.length / pageSize));

    var info = document.getElementById('pageInfo');
    if (info) {
        info.textContent = "Page " + page + " of " + totalPages;
    }
}

function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function searchSnippets() {
    var input = document.getElementById('searchBox');
    if (!(input instanceof HTMLInputElement)) return;

    var query = input.value.toLowerCase();
    var snippets = getSnippets();

    snippets.forEach(function (s) {
        var ref = s.getAttribute('data-ref') || '';
        var lower = ref.toLowerCase();

        var title = s.querySelector('.title');
        if (!(title instanceof HTMLElement)) return;

        if (lower.includes(query)) {
            s.classList.remove('hidden');

            if (query.length > 0) {
                var regex = new RegExp("(" + escapeRegExp(query) + ")", "gi");
                title.innerHTML = ref.replace(
                    regex,
                    '<span class="highlight">$1</span>'
                );
            } else {
                title.textContent = ref;
            }
        } else {
            s.classList.add('hidden');
        }
    });

    showPage(1);
}

function nextPage() {
    showPage(currentPage + 1);
}

function prevPage() {
    if (currentPage > 1) {
        showPage(currentPage - 1);
    }
}

function jumpToRef(ref) {
    if (!ref) return;

    var el = document.getElementById(ref);
    if (el) {
        el.scrollIntoView();
    }
}

window.onload = function () {
    showPage(1);
};
