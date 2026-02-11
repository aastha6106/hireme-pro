document.addEventListener("DOMContentLoaded", function () {
    var titleInput = document.getElementById("title");
    var summaryInput = document.getElementById("summary");
    var previewTitle = document.getElementById("preview-title");
    var previewSummary = document.getElementById("preview-summary");
    var summarySection = document.getElementById("preview-summary-section");
    var emptyMsg = document.getElementById("preview-empty");

    if (!titleInput || !previewTitle) return;

    var hasSections = document.querySelectorAll(".rv-entry, .rv-skill-tag").length > 0;

    function updatePreview() {
        var title = titleInput.value.trim();
        var summary = summaryInput ? summaryInput.value.trim() : "";

        previewTitle.textContent = title || "Your Name";

        if (summarySection && previewSummary) {
            if (summary) {
                previewSummary.textContent = summary;
                summarySection.style.display = "";
            } else {
                summarySection.style.display = "none";
            }
        }

        if (emptyMsg) {
            if (!title && !summary && !hasSections) {
                emptyMsg.style.display = "";
            } else {
                emptyMsg.style.display = "none";
            }
        }
    }

    titleInput.addEventListener("input", updatePreview);
    if (summaryInput) {
        summaryInput.addEventListener("input", updatePreview);
    }

    updatePreview();
});