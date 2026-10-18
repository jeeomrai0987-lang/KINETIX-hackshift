export class ApiError extends Error {
  constructor(message, code = 'unknown_error', status = 500, details = null) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

export const TOKEN_STORAGE_KEY = 'ventureforge_token';

export async function apiClient(endpoint, options = {}) {
  const {
    method = 'GET',
    body = null,
    headers = {},
    ...customConfig
  } = options;

  const token = localStorage.getItem(TOKEN_STORAGE_KEY);

  const defaultHeaders = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };

  if (token) {
    defaultHeaders.Authorization = `Bearer ${token}`;
  }

  // Remove content-type if body is FormData or not JSON
  if (body instanceof FormData) {
    delete defaultHeaders['Content-Type'];
  }

  const url = endpoint.startsWith('http')
    ? endpoint
    : `/api/v1${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

  const config = {
    method,
    headers: {
      ...defaultHeaders,
      ...headers,
    },
    ...customConfig,
  };

  if (body && !(body instanceof FormData) && typeof body !== 'string') {
    config.body = JSON.stringify(body);
  } else if (body) {
    config.body = body;
  }

  try {
    const response = await fetch(url, config);

    // 401 Unauthorized handling
    if (response.status === 401) {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem('ventureforge_auth_user');
      if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/auth')) {
        window.location.href = '/auth';
      }
    }

    // Handle CSV or text responses if requested
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('text/csv') || contentType.includes('text/plain')) {
      const text = await response.text();
      if (!response.ok) {
        throw new ApiError(text || 'Request failed', 'request_failed', response.status);
      }
      return text;
    }

    // Handle empty response (204 No Content)
    if (response.status === 204) {
      return null;
    }

    let data;
    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const errorPayload = data?.error || {};
      const errorMessage = errorPayload.message || data?.message || response.statusText || 'Request failed';
      const errorCode = errorPayload.code || 'request_failed';
      throw new ApiError(errorMessage, errorCode, response.status, data);
    }

    return data;
  } catch (err) {
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(err.message || 'Network request failed', 'network_error', 0, err);
  }
}

apiClient.get = (endpoint, options = {}) => apiClient(endpoint, { ...options, method: 'GET' });
apiClient.post = (endpoint, body, options = {}) => apiClient(endpoint, { ...options, method: 'POST', body });
apiClient.put = (endpoint, body, options = {}) => apiClient(endpoint, { ...options, method: 'PUT', body });
apiClient.delete = (endpoint, options = {}) => apiClient(endpoint, { ...options, method: 'DELETE' });

export default apiClient;
