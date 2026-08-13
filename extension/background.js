// Background Service Worker for ScamShield Extension

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'UPDATE_BADGE') {
    const { riskLevel } = message;
    if (riskLevel === 'High' || riskLevel === 'Critical') {
      chrome.action.setBadgeText({ text: '!' });
      chrome.action.setBadgeBackgroundColor({ color: riskLevel === 'Critical' ? '#f43f5e' : '#f97316' });
    } else {
      chrome.action.setBadgeText({ text: '' });
    }
    sendResponse({ status: 'ok' });
  }
});
