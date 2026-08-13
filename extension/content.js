// Content script for extracting page content safely
(() => {
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "EXTRACT_PAGE_DATA") {
      try {
        const pageTitle = document.title || "";
        const pageUrl = window.location.href;
        
        // Extract visible body text (safely limited to 10,000 characters)
        const rawText = document.body ? document.body.innerText || "" : "";
        const pageText = rawText.replace(/\s+/g, ' ').trim().slice(0, 10000);

        // Extract anchor link URLs (safely limited to top 20 distinct links)
        const anchors = Array.from(document.querySelectorAll('a[href]'));
        const links = Array.from(new Set(
          anchors
            .map(a => a.href)
            .filter(href => href.startsWith('http://') || href.startsWith('https://'))
        )).slice(0, 20);

        sendResponse({
          success: true,
          data: {
            page_title: pageTitle,
            page_url: pageUrl,
            page_text: pageText,
            links: links
          }
        });
      } catch (err) {
        sendResponse({
          success: false,
          error: err.message
        });
      }
    }
    return true; // Keep message channel open for async response
  });
})();
