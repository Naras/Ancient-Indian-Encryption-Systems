import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import GridList from './components/GridList.tsx';
import GridEditor from './components/GridEditor.tsx';
import UserManagement from './components/UserManagement';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/grids"
            element={
              <ProtectedRoute>
                <GridList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/grid/:name"
            element={
              <ProtectedRoute>
                <GridEditor />
              </ProtectedRoute>
            }
          />
          <Route
            path="/users"
            element={
              <ProtectedRoute requireAdmin>
                <UserManagement />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/grids" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
