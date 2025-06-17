import axios, { AxiosError } from 'axios';
import pako from 'pako';

const API_BASE_URL = 'http://localhost:5001/Cryptology/api/v1.0';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      method: config.method,
      url: config.url,
      data: config.data,
      headers: config.headers,
    });
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      data: response.data,
      headers: response.headers,
    });
    return response;
  },
  (error) => {
    console.error('API Response Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    });
    return Promise.reject(error);
  }
);

// Add session token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('sessionToken');
  if (token) {
    config.headers['X-Session-Token'] = token;
  }
  return config;
});

export class GridExistsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'GridExistsError';
  }
}

export class GridNotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'GridNotFoundError';
  }
}

export interface GridResponse {
  'result: grid created': {
    rows: string;
    cols: string;
  };
}

export interface BandhaResponse {
  result: {
    bandhas: string[];
  };
}

export interface OperationResponse {
  result: any;
}

export interface DisplayResponse {
  "result:": {
    compressed?: boolean;
    data?: string;
    text?: string;
  };
}

export interface GridListResponse {
  "result:": string[];
}

export interface LoginResponse {
  message: string;
  token: string;
  expires: string;
  is_admin: boolean;
}

export interface User {
  username: string;
  is_admin: boolean;
}

const decompressData = (encodedData: string): string => {
  try {
    // Convert base64 to binary
    const binaryData = atob(encodedData);
    
    // Convert binary to Uint8Array
    const bytes = new Uint8Array(binaryData.length);
    for (let i = 0; i < binaryData.length; i++) {
      bytes[i] = binaryData.charCodeAt(i);
    }
    
    // Decompress using pako
    const decompressed = pako.inflate(bytes, { to: 'string' });
    return decompressed;
  } catch (error) {
    console.error('[API] Error decompressing data:', error);
    throw new Error('Failed to decompress data');
  }
};

const apiService = {
  // Authentication
  async login(username: string, password: string): Promise<LoginResponse> {
    console.log('Attempting login for user:', username);
    const response = await api.post('/login', { username, password });
    const { token } = response.data;
    localStorage.setItem('sessionToken', token);
    console.log('Login successful, token stored');
    return response.data;
  },

  async logout(): Promise<void> {
    console.log('Attempting logout');
    await api.post('/logout');
    localStorage.removeItem('sessionToken');
    console.log('Logout successful, token removed');
  },

  // User Management
  async createUser(username: string, password: string, isAdmin: boolean = false): Promise<void> {
    console.log('Creating user:', { username, isAdmin });
    await api.post('/users/create', { username, password, is_admin: isAdmin });
  },

  async deleteUser(username: string): Promise<void> {
    console.log('Deleting user:', username);
    await api.delete(`/users/delete/${username}`);
  },

  async listUsers(): Promise<User[]> {
    try {
      const response = await api.get('/users/list');
      console.log('List users response:', response.data);
      if (response.data && response.data.users) {
        return response.data.users;
      }
      return [];
    } catch (error) {
      console.error('Error listing users:', error);
      throw error;
    }
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    console.log('Changing password');
    await api.post('/users/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  // Grid Operations
  async createGrid(name: string, rows: number, cols: number): Promise<GridResponse> {
    console.log('Creating grid:', { name, rows, cols });
    const response = await api.get('/createGrid', {
      params: { name, rows, cols },
    });
    return response.data;
  },

  async removeGrid(name: string): Promise<void> {
    console.log('Removing grid:', name);
    await api.get('/removeGrid', {
      params: { name },
    });
  },

  async display(name: string): Promise<DisplayResponse> {
    console.log('Displaying grid:', name);
    try {
      const response = await api.get('/display', {
        params: { name },
      });
      
      // Handle compressed data
      if (response.data["result:"]?.compressed && response.data["result:"]?.data) {
        const decompressedText = decompressData(response.data["result:"].data);
        return {
          "result:": {
            text: decompressedText
          }
        };
      }
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        if (axiosError.response?.status === 404) {
          throw new GridNotFoundError('The specified grid was not found');
        }
      }
      throw error;
    }
  },

  async getBandhaLiterals(name: string): Promise<BandhaResponse> {
    console.log('Fetching bandha literals for grid:', name);
    const response = await api.get(`/bandhaLiterals?name=${encodeURIComponent(name)}`);
    console.log('Bandha literals response:', response.data);
    return response.data;
  },

  async getBandhas(name: string): Promise<OperationResponse> {
    console.log('Fetching bandhas for grid:', name);
    const response = await api.get('/bandhas', {
      params: { name },
    });
    return response.data;
  },

  async checkFit(name: string, bandha: string, text: string, x: number, y: number): Promise<OperationResponse> {
    console.log('Checking fit:', { name, bandha, text, x, y });
    const response = await api.get('/it_fits_in', {
      params: { name, bandha, text, x, y },
    });
    return response.data;
  },

  async hideText(name: string, bandha: string, text: string, x: number, y: number): Promise<OperationResponse> {
    console.log('Hiding text:', { name, bandha, text, x, y });
    const response = await api.get('/hide', {
      params: { name, bandha, text, x, y },
    });
    return response.data;
  },

  async revealText(name: string, bandha: string, x: number, y: number, length: number): Promise<OperationResponse> {
    console.log('Revealing text:', { name, bandha, x, y, length });
    const response = await api.get('/reveal', {
      params: { name, bandha, x, y, l: length },
    });
    return response.data;
  },

  async noiseFill(name: string): Promise<DisplayResponse> {
    console.log('Noise filling grid:', name);
    try {
      const response = await api.get('/noisefill', {
        params: { name },
      });
      
      // Handle compressed data
      if (response.data["result:"]?.compressed && response.data["result:"]?.data) {
        const decompressedText = decompressData(response.data["result:"].data);
        return {
          "result:": {
            text: decompressedText
          }
        };
      }
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        if (axiosError.response?.status === 404) {
          throw new GridNotFoundError('The specified grid was not found');
        }
      }
      throw error;
    }
  },

  async exportGrid(name: string): Promise<void> {
    const token = localStorage.getItem('sessionToken');
    if (!token) throw new Error('No session token found');
    
    const response = await fetch(`${API_BASE_URL}/export?name=${encodeURIComponent(name)}`, {
      headers: {
        'X-Session-Token': token,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to export grid');
    }
    
    // Get the filename from the Content-Disposition header
    const contentDisposition = response.headers.get('Content-Disposition');
    const filename = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/"/g, '')
      : `${name}.txt`;
    
    // Create a blob from the response
    const blob = await response.blob();
    
    // Create a download link and trigger the download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  async importGrid(name: string, file: File): Promise<OperationResponse> {
    console.log('Importing grid:', { name, file });
    if (!file) throw new Error('No file provided for import');
    const token = localStorage.getItem('sessionToken');
    if (!token) throw new Error('No session token found');
    
    const formData = new FormData();
    formData.append('file', file);
    console.log('Form data prepared for import:', formData);  
    console.log('URL:', `${API_BASE_URL}/import?name=${encodeURIComponent(name)}`);
    const response = await fetch(`${API_BASE_URL}/import?name=${encodeURIComponent(name)}`, {
      method: 'POST',
      headers: {
        'X-Session-Token': token,
        // 'Content-Type': 'multipart/form-data',
      },
      body: formData,
    });
    
    if (!response.ok) {
      const error = await response.json();
      console.log('Import error response:', error);
      throw new Error(error.error);
    }
    
    return response.json();
  },

  async getGridList(): Promise<GridListResponse> {
    console.log('Fetching grid list');
    const response = await api.get('/gridlist');
    return response.data;
  },

  async clearGrid(name: string): Promise<void> {
    console.log('Clearing grid:', name);
    await api.get('/clear', {
      params: { name },
    });
  }
};

export default apiService; 