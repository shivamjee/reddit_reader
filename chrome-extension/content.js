// Helper to create tooltip
function createTooltip(text, parentLink) {
    let tooltip = document.createElement('div');
    tooltip.className = 'link-tooltip';
    tooltip.innerHTML = text;
    document.body.appendChild(tooltip);

    const rect = parentLink.getBoundingClientRect();
    tooltip.style.top = (window.scrollY + rect.bottom + 5) + 'px';
    tooltip.style.left = (window.scrollX + rect.left) + 'px';

    // Remove tooltip on next click anywhere
    function removeTooltip() {
        tooltip.remove();
        document.removeEventListener('click', removeTooltip);
    }
    setTimeout(() => { document.addEventListener('click', removeTooltip); }, 0);
}

// Inject analyze buttons
document.querySelectorAll('h3').forEach(title => {
    const link = title.closest('a');
    if (!link) return; // skip if not a proper link

    const btn = document.createElement('button');
    btn.innerText = '🔍';
    btn.style.marginLeft = '40px';
    btn.style.fontSize = '12px';
    btn.style.cursor = 'pointer';

    btn.addEventListener('click', async (e) => {
        e.stopPropagation(); // prevent page navigation
        const urlToAnalyze = link.href;
        createTooltip('<span class="tooltip-loading">Analyzing...</span>', link);

        try {
            const response = await fetch(`http://127.0.0.1:8000/reddit?url=${encodeURIComponent(urlToAnalyze)}`);
            const data = await response.json();
            const summary = `
                <strong>Political:</strong> ${data.is_political}<br>
                <strong>Leaning:</strong> ${data.leaning || 'N/A'}<br>
                <strong>Helpfulness:</strong> ${data.helpfulness}<br>
                <strong>Summary:</strong> ${data.explanation}
            `;
            createTooltip(summary, link);
        } catch (err) {
            createTooltip('Error: ' + err.message, link);
        }
    });

    link.parentNode.appendChild(btn);
});
