import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { GRID_SETTINGS } from '../constants/grid';

const SAMPLE_TEXTS = [
  'this is the first message',
  'and this is the second message',
  'and at last, the third message',
  'The quick brown fox jumps over the lazy dog',
  'Pack my box with five dozen liquor jugs',
  'How vexingly quick daft zebras jump',
  'Sphinx of black quartz, judge my vow',
  'Crazy Fredrick bought many very exquisite opal jewels',
  'We promptly judged antique ivory buckles for the next prize',
  'The five boxing wizards jump quickly',
];

const GridEditor: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const [gridSize, setGridSize] = useState({ rows: 50, cols: 50 });
  const [gridName, setGridName] = useState(name === 'new' ? '' : name || '');
  const [bandhas, setBandhas] = useState<string[]>([]);
  const [selectedBandha, setSelectedBandha] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const [customText, setCustomText] = useState('');
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [operationType, setOperationType] = useState<'it_fits_in' | 'hide' | 'reveal'>('it_fits_in');
  const [result, setResult] = useState<any>(null);
  const [revealLength, setRevealLength] = useState(25);
  const [gridDisplay, setGridDisplay] = useState('');
  const [displayMode, setDisplayMode] = useState<'normal' | 'noise'>('normal');
  const [error, setError] = useState<string | null>(null);
  const [x, setX] = useState(GRID_SETTINGS.DEFAULT_X);
  const [y, setY] = useState(GRID_SETTINGS.DEFAULT_Y);
  const [length, setLength] = useState(GRID_SETTINGS.DEFAULT_LENGTH);

  useEffect(() => {
    if (name !== 'new') {
      loadGrid();
    }
  }, [name]);

  const loadGrid = async () => {
    try {
      console.log('Loading grid:', gridName);
      const response = await api.display(gridName);
      if (response["result:"]?.text) {
        setGridDisplay(response["result:"].text);
      }
      
      console.log('Fetching bandha literals for grid:', gridName);
      const bandhaResponse = await api.getBandhaLiterals(gridName);
      console.log('Bandha literals response:', bandhaResponse);
      
      if (bandhaResponse.result?.bandhas) {
        setBandhas(bandhaResponse.result.bandhas);
        if (bandhaResponse.result.bandhas.length > 0) {
          setSelectedBandha(bandhaResponse.result.bandhas[0]);
        }
      } else {
        console.error('No bandhas found in response:', bandhaResponse);
        setError('Failed to load bandha literals');
      }
    } catch (err) {
      console.error('Error loading grid:', err);
      setError('Failed to load grid');
    }
  };

  const handleCreateGrid = async () => {
    try {
      await api.createGrid(gridName, gridSize.rows, gridSize.cols);
      navigate(`/grid/${gridName}`);
    } catch (err) {
      setError('Failed to create grid');
    }
  };

  const handleOperation = async () => {
    try {
      const text = customText || selectedText;
      let response;
      
      switch (operationType) {
        case 'it_fits_in':
          response = await api.checkFit(gridName, selectedBandha, text, x, y);
          break;
        case 'hide':
          response = await api.hideText(gridName, selectedBandha, text, x, y);
          break;
        case 'reveal':
          response = await api.revealText(gridName, selectedBandha, x, y, length);
          break;
      }
      
      setResult(response);
      await loadGrid();
    } catch (err) {
      setError('Failed to perform operation');
    }
  };

  const handleDisplayModeChange = async (mode: 'normal' | 'noise') => {
    setDisplayMode(mode);
    try {
      const response = mode === 'normal' 
        ? await api.display(gridName)
        : await api.noiseFill(gridName);
      if (response["result:"]?.text) {
        setGridDisplay(response["result:"].text);
      }
    } catch (err) {
      setError('Failed to change display mode');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            {name === 'new' ? 'Create New Grid' : `Edit Grid: ${gridName}`}
          </h1>
          <button
            onClick={() => navigate('/grids')}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-600 hover:bg-gray-700"
          >
            Back to Grids
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {name === 'new' ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Please create a new grid from the Grid List page.</p>
            <button
              onClick={() => navigate('/grids')}
              className="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Go to Grid List
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Grid Operations</h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700">X Coordinate</label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      min={GRID_SETTINGS.MIN_X}
                      max={GRID_SETTINGS.MAX_X}
                      value={x}
                      onChange={(e) => {
                        const newX = parseInt(e.target.value);
                        setX(newX);
                        setPosition(prev => ({ ...prev, x: newX }));
                      }}
                      className="flex-1"
                    />
                    <input
                      type="number"
                      min={GRID_SETTINGS.MIN_X}
                      max={GRID_SETTINGS.MAX_X}
                      value={x}
                      onChange={(e) => {
                        const newX = parseInt(e.target.value) || 0;
                        setX(newX);
                        setPosition(prev => ({ ...prev, x: newX }));
                      }}
                      className="w-20 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Y Coordinate</label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      min={GRID_SETTINGS.MIN_Y}
                      max={GRID_SETTINGS.MAX_Y}
                      value={y}
                      onChange={(e) => {
                        const newY = parseInt(e.target.value);
                        setY(newY);
                        setPosition(prev => ({ ...prev, y: newY }));
                      }}
                      className="flex-1"
                    />
                    <input
                      type="number"
                      min={GRID_SETTINGS.MIN_Y}
                      max={GRID_SETTINGS.MAX_Y}
                      value={y}
                      onChange={(e) => {
                        const newY = parseInt(e.target.value) || 0;
                        setY(newY);
                        setPosition(prev => ({ ...prev, y: newY }));
                      }}
                      className="w-20 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Length (for reveal)</label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      min={1}
                      max={100}
                      value={length}
                      onChange={(e) => setLength(parseInt(e.target.value))}
                      className="flex-1"
                    />
                    <input
                      type="number"
                      min={1}
                      max={100}
                      value={length}
                      onChange={(e) => setLength(parseInt(e.target.value) || 1)}
                      className="w-20 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Operation Type</label>
                  <select
                    value={operationType}
                    onChange={(e) => setOperationType(e.target.value as any)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    <option value="it_fits_in">Check if Text Fits</option>
                    <option value="hide">Hide Text</option>
                    <option value="reveal">Reveal Text</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Bandha</label>
                  <select
                    value={selectedBandha}
                    onChange={(e) => setSelectedBandha(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    {bandhas.map((bandha) => (
                      <option key={bandha} value={bandha}>
                        {bandha}
                      </option>
                    ))}
                  </select>
                </div>

                {operationType !== 'reveal' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Sample Text</label>
                      <select
                        value={selectedText}
                        onChange={(e) => {
                          setSelectedText(e.target.value);
                          setCustomText(e.target.value);
                        }}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      >
                        {SAMPLE_TEXTS.map((text) => (
                          <option key={text} value={text}>
                            {text}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Custom Text</label>
                      <textarea
                        value={customText}
                        onChange={(e) => setCustomText(e.target.value)}
                        rows={4}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      />
                    </div>
                  </>
                )}

                <button
                  onClick={handleOperation}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Execute Operation
                </button>
              </div>
            </div>

            <div className="bg-white shadow sm:rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">Grid Display</h2>
                <div className="space-x-2">
                  <button
                    onClick={() => handleDisplayModeChange('normal')}
                    className={`px-3 py-1 border rounded-md text-sm font-medium ${
                      displayMode === 'normal'
                        ? 'bg-indigo-600 text-white'
                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    Normal Grid
                  </button>
                  <button
                    onClick={() => handleDisplayModeChange('noise')}
                    className={`px-3 py-1 border rounded-md text-sm font-medium ${
                      displayMode === 'noise'
                        ? 'bg-indigo-600 text-white'
                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    Noise-Filled Grid
                  </button>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-md font-mono text-sm whitespace-pre-wrap overflow-auto max-h-96">
                {gridDisplay || 'No grid content to display'}
              </div>
            </div>

            {result && (
              <div className="bg-white shadow sm:rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Operation Result</h2>
                <pre className="bg-gray-50 p-4 rounded-md overflow-auto">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GridEditor; 