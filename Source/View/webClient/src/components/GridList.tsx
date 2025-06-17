import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { GRID_SETTINGS } from '../constants/grid';

interface Grid {
  name: string;
  size: string;
  owner?: string;
}

const GridList: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [grids, setGrids] = useState<Grid[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importName, setImportName] = useState('');
  const [rows, setRows] = useState(GRID_SETTINGS.DEFAULT_ROWS);
  const [cols, setCols] = useState(GRID_SETTINGS.DEFAULT_COLS);
  const [gridName, setGridName] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newUserPassword, setNewUserPassword] = useState('');

  // Clear any cached state on component mount
  useEffect(() => {
    setCurrentPassword('');
    setNewUserPassword('');
    setError(null);
    setSuccess(null);
  }, []);

  useEffect(() => {
    console.log('GridList mounted, current user:', user);
    loadGrids();
  }, [user]);

  const loadGrids = async () => {
    try {
      console.log('Loading grids for user:', user);
      const response = await api.getGridList();
      const gridList = response["result:"].map((gridStr: string) => {
        const match = gridStr.match(/name: (.*?) size:(.*?)(?: owner:(.*))?$/);
        if (match) {
          return {
            name: match[1],
            size: match[2],
            owner: match[3] || undefined
          } as Grid;
        }
        return null;
      }).filter((grid): grid is Grid => grid !== null);
      setGrids(gridList);
    } catch (err) {
      setError('Failed to load grids');
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      setError('Failed to logout');
    }
  };

  const handleRemoveGrid = async (gridName: string) => {
    if (!window.confirm(`Are you sure you want to remove grid ${gridName}?`)) {
      return;
    }

    try {
      await api.removeGrid(gridName);
      setSuccess(`Grid ${gridName} removed successfully`);
      loadGrids();
    } catch (err) {
      setError('Failed to remove grid');
    }
  };

  const handleClearGrid = async (gridName: string) => {
    if (!window.confirm(`Are you sure you want to clear grid ${gridName}?`)) {
      return;
    }

    try {
      await api.clearGrid(gridName);
      setSuccess(`Grid ${gridName} cleared successfully`);
    } catch (err) {
      setError('Failed to clear grid');
    }
  };

  const handleExportGrid = async (gridName: string) => {
    try {
      const filename = `${gridName}.txt`;
      await api.exportGrid(gridName, filename);
      setSuccess(`Grid ${gridName} exported successfully to ${filename}`);
    } catch (err) {
      setError('Failed to export grid');
    }
  };

  const handleImportGrid = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!importFile || !importName) {
      setError('Please select a file and provide a grid name');
      return;
    }

    try {
      // Create a temporary file input to handle the file upload
      const formData = new FormData();
      formData.append('file', importFile);
      
      await api.importGrid(importName, importFile);
      setSuccess(`Grid ${importName} imported successfully`);
      setImportFile(null);
      setImportName('');
      loadGrids();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import grid');
    }
  };

  const handleCreateGrid = async () => {
    try {
      // Use empty string if grid name is empty, which will be converted to "Untitled" by the server
      const name = gridName.trim();
      await api.createGrid(name, rows, cols);
      setSuccess(`Grid ${name || 'Untitled'} created successfully`);
      setGridName(''); // Clear the grid name input
      loadGrids();
    } catch (err) {
      setError('Failed to create grid');
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentPassword || !newUserPassword) {
      setError('Please fill in all password fields');
      return;
    }
    if (newUserPassword.length < 8) {
      setError('New password must be at least 8 characters long');
      return;
    }
    try {
      await api.changePassword(currentPassword, newUserPassword);
      setSuccess('Password changed successfully');
      setCurrentPassword('');
      setNewUserPassword('');
    } catch (err) {
      setError('Failed to change password');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Grids</h1>
          <div className="space-x-4">
            {user?.is_admin && (
              <button
                onClick={() => navigate('/users')}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Manage Users
              </button>
            )}
            {/* <button
              onClick={() => navigate('/grid/new')}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Create New Grid
            </button> */}
            <button
              onClick={handleLogout}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
            <p className="text-green-600">{success}</p>
          </div>
        )}

        <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Create New Grid</h2>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Grid Name</label>
              <input
                type="text"
                value={gridName}
                onChange={(e) => setGridName(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Rows</label>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min={GRID_SETTINGS.MIN_ROWS}
                  max={GRID_SETTINGS.MAX_ROWS}
                  value={rows}
                  onChange={(e) => setRows(parseInt(e.target.value))}
                  className="flex-1"
                />
                <input
                  type="number"
                  min={GRID_SETTINGS.MIN_ROWS}
                  max={GRID_SETTINGS.MAX_ROWS}
                  value={rows}
                  onChange={(e) => setRows(parseInt(e.target.value) || GRID_SETTINGS.MIN_ROWS)}
                  className="w-20 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Columns</label>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min={GRID_SETTINGS.MIN_COLS}
                  max={GRID_SETTINGS.MAX_COLS}
                  value={cols}
                  onChange={(e) => setCols(parseInt(e.target.value))}
                  className="flex-1"
                />
                <input
                  type="number"
                  min={GRID_SETTINGS.MIN_COLS}
                  max={GRID_SETTINGS.MAX_COLS}
                  value={cols}
                  onChange={(e) => setCols(parseInt(e.target.value) || GRID_SETTINGS.MIN_COLS)}
                  className="w-20 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <button
              onClick={handleCreateGrid}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Create Grid
            </button>
          </div>
        </div>

        <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Import Grid</h2>
          <form onSubmit={handleImportGrid} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Grid Name</label>
              <input
                type="text"
                value={importName}
                onChange={(e) => setImportName(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Grid File</label>
              <input
                type="file"
                onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                className="mt-1 block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-medium
                  file:bg-indigo-50 file:text-indigo-700
                  hover:file:bg-indigo-100"
                accept=".txt"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Import Grid
            </button>
          </form>
        </div>

        <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Change Your Password</h2>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Current Password</label>
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">New Password</label>
              <input
                type="password"
                value={newUserPassword}
                onChange={(e) => setNewUserPassword(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
                minLength={8}
              />
            </div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Change Password
            </button>
          </form>
        </div>

        <div className="bg-white shadow sm:rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Your Grids</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Size
                  </th>
                  {user?.is_admin && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Owner
                    </th>
                  )}
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {grids.map((grid) => (
                  <tr key={grid.name}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {grid.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {grid.size}
                    </td>
                    {user?.is_admin && (
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {grid.owner}
                      </td>
                    )}
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="space-x-2">
                        <button
                          onClick={() => navigate(`/grid/${grid.name}`)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          Open
                        </button>
                        <button
                          onClick={() => handleClearGrid(grid.name)}
                          className="text-yellow-600 hover:text-yellow-900"
                        >
                          Clear
                        </button>
                        <button
                          onClick={() => handleExportGrid(grid.name)}
                          className="text-green-600 hover:text-green-900"
                        >
                          Export
                        </button>
                        <button
                          onClick={() => handleRemoveGrid(grid.name)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Remove
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GridList; 