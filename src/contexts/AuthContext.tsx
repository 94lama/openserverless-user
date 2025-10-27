import React, { createContext, useContext, useState, useEffect } from 'react';

export interface HTTPUser {
  name: string;
  token: string;
}

interface AuthContextType {
  user: HTTPUser | null;
  login: (name: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<HTTPUser | null>();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    setUser(storedUser ? JSON.parse(storedUser) : null);
  }, []);

  const login = async (name: string, password: string) => {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/v1/web/devel/mastrogpt/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, password }),
    });

    const data = await response.json();
    
    if (!response.ok || !data.token) throw new Error(data.output || 'Login failed');

    const userData: HTTPUser = {
      name: name,
      token: data.token
    };

    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
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
