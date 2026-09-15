const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path) {
    const response = await fetch(`${API_BASE_URL}/api/v1${path}`);
    const data = await response.json();

    if (!response.ok) {
        const error = new Error(data.detail || "API request failed");
        error.status = response.status;
        throw error;
    }

    return data;
}

export function getSymbols() {
    return request("/symbols");
}

export function getStockAnalysis(symbol) {
    return request(`/analyze/${encodeURIComponent(symbol)}`);
}
