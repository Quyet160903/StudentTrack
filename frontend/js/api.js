// frontend/js/api.js
const BASE_URL = "http://127.0.0.1:8000";

// store tokens in memory (not localStorage)
let accessToken = null;

export function setToken(token) {
    accessToken = token;
}

export function getToken() {
    return accessToken;
}

export async function request(method, path, body = null) {
    const headers = {
        "Content-Type": "application/json"
    };

    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    const options = {
        method,
        headers
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${BASE_URL}${path}`, options);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Something went wrong");
    }

    return response.json();
}

// shorthand helpers
export const api = {
    get: (path) => request("GET", path),
    post: (path, body) => request("POST", path, body),
    put: (path, body) => request("PUT", path, body),
    delete: (path) => request("DELETE", path)
};