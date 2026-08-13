const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export async function analyzeMessage(data) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to analyze message' }));
    throw new Error(errorData.detail || 'Analysis request failed');
  }
  return response.json();
}

export async function getScans(skip = 0, limit = 50) {
  const response = await fetch(`${API_BASE}/scans?skip=${skip}&limit=${limit}`);
  if (!response.ok) {
    throw new Error('Failed to fetch scan history');
  }
  return response.json();
}

export async function deleteScan(id) {
  const response = await fetch(`${API_BASE}/scans/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete scan entry');
  }
  return response.json();
}
