import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

interface User {
  username: string
  is_admin: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('sessionToken');
    if (token) {
      // For now, we'll assume the admin user is logged in if there's a token
      // In a real app, you would validate the token with the server
      setUser({ username: 'admin', is_admin: true });
    }
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await api.login(username, password);
      console.log('Login response:', response); // Debug log
      
      // Store the token
      localStorage.setItem('sessionToken', response.token);
      
      // Set the user with admin status
      const isAdmin = username === 'admin' || response.is_admin === true;
      console.log('Setting user with admin status:', isAdmin); // Debug log
      
      setUser({ 
        username, 
        is_admin: isAdmin 
      });
      
      console.log('User state after login:', { username, is_admin: isAdmin }); // Debug log
    } catch (error) {
      console.error('Login error:', error); // Debug log
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.logout();
      localStorage.removeItem('sessionToken');
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error); // Debug log
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 