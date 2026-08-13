// ScamShield Popup Logic
const API_BASE = 'http://localhost:8000'; // Change to 'https://scamshield-api.onrender.com' for production deployment

document.addEventListener('DOMContentLoaded', () => {
  const initialState = document.getElementById('initial-state');
  const loadingState = document.getElementById('loading-state');
  const resultState = document.getElementById('result-state');
  const errorState = document.getElementById('error-state');

  const scanBtn = document.getElementById('scan-btn');
  const rescanBtn = document.getElementById('rescan-btn');
  const errorRetryBtn = document.getElementById('error-retry-btn');
  const errorMsg = document.getElementById('error-msg');

  const riskBadge = document.getElementById('risk-badge');
  const riskScore = document.getElementById('risk-score');
  const verdictTitle = document.getElementById('verdict-title');
  const recommendationText = document.getElementById('recommendation-text');
  const flagsCount = document.getElementById('flags-count');
  const flagsList = document.getElementById('flags-list');

  function showState(state) {
    initialState.classList.add('hidden');
    loadingState.classList.add('hidden');
    resultState.classList.add('hidden');
    errorState.classList.add('hidden');

    state.classList.remove('hidden');
  }

  async function performScan() {
    showState(loadingState);

    try {
      // Query current active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      if (!tab) {
        throw new Error('No active browser tab found');
      }

      // Check if current URL is a restricted chrome:// or edge:// page
      if (tab.url && (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://') || tab.url.startsWith('edge://') || tab.url.startsWith('about:'))) {
        throw new Error('ScamShield cannot scan internal browser pages (chrome://, edge://)');
      }

      // Send message to content script to extract page content
      let extractedData;
      try {
        const response = await chrome.tabs.sendMessage(tab.id, { action: 'EXTRACT_PAGE_DATA' });
        if (response && response.success) {
          extractedData = response.data;
        } else {
          throw new Error(response ? response.error : 'Content script did not respond');
        }
      } catch (err) {
        // Fallback: try injecting content script dynamically if not pre-loaded
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content.js']
        });
        const retryResp = await chrome.tabs.sendMessage(tab.id, { action: 'EXTRACT_PAGE_DATA' });
        if (retryResp && retryResp.success) {
          extractedData = retryResp.data;
        } else {
          throw new Error('Failed to extract page data from this tab.');
        }
      }

      // Call backend API endpoint
      const apiResponse = await fetch(`${API_BASE}/api/analyze-page`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(extractedData)
      });

      if (!apiResponse.ok) {
        throw new Error(`Backend API error (${apiResponse.status})`);
      }

      const result = await apiResponse.json();

      // Render results in UI
      riskBadge.textContent = result.risk_level.toUpperCase();
      riskBadge.className = `risk-badge ${result.risk_level}`;
      riskScore.textContent = result.risk_score;
      verdictTitle.textContent = result.verdict;
      recommendationText.textContent = result.recommendation;

      flagsCount.textContent = result.red_flags.length;
      flagsList.innerHTML = '';

      if (result.red_flags.length === 0) {
        flagsList.innerHTML = '<div style="font-size:11px; color:#34d399; padding:6px;">No security red flags detected on this page.</div>';
      } else {
        result.red_flags.forEach(flag => {
          const item = document.createElement('div');
          item.className = 'flag-item';
          item.innerHTML = `
            <div class="flag-name">${flag.rule} (+${flag.points} pts)</div>
            <div class="flag-desc">${flag.explanation}</div>
          `;
          flagsList.appendChild(item);
        });
      }

      // Send badge update message to background worker
      chrome.runtime.sendMessage({
        action: 'UPDATE_BADGE',
        riskLevel: result.risk_level
      });

      showState(resultState);
    } catch (err) {
      errorMsg.textContent = err.message || 'Scan failed';
      showState(errorState);
    }
  }

  scanBtn.addEventListener('click', performScan);
  rescanBtn.addEventListener('click', performScan);
  errorRetryBtn.addEventListener('click', () => showState(initialState));
});
