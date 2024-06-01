import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [numberType, setNumberType] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await axios.get(`http://localhost:9876/numbers/${numberType}`);
      setResponse(result.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <h1>Average Calculator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter number type (p, f, e, r):
          <input type="text" value={numberType} onChange={(e) => setNumberType(e.target.value)} />
        </label>
        <button type="submit">Get Numbers</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <p><strong>Window Previous State:</strong> {JSON.stringify(response.windowPrevState)}</p>
          <p><strong>Window Current State:</strong> {JSON.stringify(response.windowCurrState)}</p>
          <p><strong>Numbers:</strong> {JSON.stringify(response.numbers)}</p>
          <p><strong>Average:</strong> {response.avg}</p>
        </div>
      )}
    </div>
  );
}

export default App;
