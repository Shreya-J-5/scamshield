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
  const riskMeterFill = document.getElementById('risk-meter-fill');
  const verdictTitle = document.getElementById('verdict-title');
  const recommendationText = document.getElementById('recommendation-text');
  const flagsCount = document.getElementById('flags-count');
  const flagsList = document.getElementById('flags-list');

  const alternativeCard = document.getElementById('alternative-card');
  const altName = document.getElementById('alt-name');
  const altExplanation = document.getElementById('alt-explanation');
  const altLink = document.getElementById('alt-link');

  const saferAltsSection = document.getElementById('safer-alternatives-section');
  const providerBadge = document.getElementById('provider-badge');
  const purposeText = document.getElementById('purpose-text');
  const saferCardsList = document.getElementById('safer-cards-list');

  function showState(state) {
    initialState.classList.add('hidden');
    loadingState.classList.add('hidden');
    resultState.classList.add('hidden');
    errorState.classList.add('hidden');

    state.classList.remove('hidden');
  }

  function renderSaferAlternatives(payload) {
    if (!payload) {
      saferAltsSection.classList.add('hidden');
      return;
    }

    const providerMap = {
      gemini: '✦ AI Powered',
      cache: '⚡ Cached',
      local_fallback: '🛡 Verified List'
    };
    providerBadge.textContent = providerMap[payload.provider_source] || '🛡 Verified List';
    
    const taskTitle = payload.primary_task || 'Task Processing';
    const catLabel = payload.category ? ` (${payload.category}${payload.sub_category ? ' • ' + payload.sub_category : ''})` : '';
    purposeText.textContent = `${taskTitle}${catLabel}`;

    saferCardsList.innerHTML = '';

    if (!payload.alternatives || payload.alternatives.length === 0) {
      saferCardsList.innerHTML = `
        <div class="safer-empty-state">
          We couldn't confidently identify the exact service this website provides, so we don't want to suggest irrelevant alternatives.
        </div>
      `;
      saferAltsSection.classList.remove('hidden');
      return;
    }

    payload.alternatives.forEach(alt => {
      // Validate HTTPS URL security
      if (!alt.url || !alt.url.startsWith('https://')) return;

      const card = document.createElement('div');
      card.className = 'alt-card-item';

      const tagEmojiMap = {
        free: '🆓 Free',
        fast: '⚡ Fast',
        privacy: '🔒 Privacy',
        trusted: '✓ Trusted'
      };

      const tagsHtml = (alt.tags || []).map(t => {
        const lower = String(t).toLowerCase();
        const label = tagEmojiMap[lower] || t;
        return `<span class="tag-pill ${lower}">${label}</span>`;
      }).join(' ');

      card.innerHTML = `
        <div class="alt-card-top">
          <div class="alt-card-title-group">
            <span class="alt-card-name">${alt.name}</span>
            <span class="alt-card-domain">${alt.domain}</span>
          </div>
          <span class="trust-pill">${alt.category_label || '✓ Trusted'}</span>
        </div>
        <p class="alt-card-desc">${alt.description}</p>
        ${alt.reason ? `<p class="alt-card-reason">Reason: ${alt.reason}</p>` : ''}
        <div class="alt-card-tags">${tagsHtml}</div>
        <a href="${alt.url}" target="_blank" rel="noopener noreferrer" class="btn-open-site">Open Website ↗</a>
      `;

      saferCardsList.appendChild(card);
    });

    saferAltsSection.classList.remove('hidden');
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

      // Animate risk meter progress bar
      if (riskMeterFill) {
        const scorePercent = Math.min(100, Math.max(0, result.risk_score));
        riskMeterFill.style.width = `${scorePercent}%`;
        const colorMap = {
          Low: '#16A36A',
          Suspicious: '#D97706',
          High: '#EA580C',
          Critical: '#E5484D'
        };
        riskMeterFill.style.backgroundColor = colorMap[result.risk_level] || '#16A36A';
      }

      flagsCount.textContent = result.red_flags.length;
      flagsList.innerHTML = '';

      if (result.red_flags.length === 0) {
        flagsList.innerHTML = '<div style="font-size:11px; color:#16A36A; padding:6px;">No security red flags detected on this page.</div>';
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

      // Single alt card (backwards compatibility)
      if (result.safe_alternative) {
        altName.textContent = result.safe_alternative.name;
        altExplanation.textContent = result.safe_alternative.explanation;
        altLink.href = result.safe_alternative.url;
        alternativeCard.classList.remove('hidden');
      } else {
        alternativeCard.classList.add('hidden');
      }

      // Rich Safer Alternatives Section
      if (result.safer_alternatives_data) {
        renderSaferAlternatives(result.safer_alternatives_data);
      } else {
        saferAltsSection.classList.add('hidden');
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
