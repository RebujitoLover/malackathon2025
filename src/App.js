import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './App.css';

function App() {
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  // Obtener datos cuando la página carga
  useEffect(() => {
    axios.get('http://localhost:5000/api/datos')
      .then(response => {
        console.log('Datos recibidos:', response.data);
        setDatos(response.data);
        setCargando(false);
      })
      .catch(err => {
        console.error('Error:', err);
        setError('No se pudieron cargar los datos');
        setCargando(false);
      });
  }, []);

  if (cargando) return <div className="App">Cargando datos... ⏳</div>;
  if (error) return <div className="App">Error: {error} ❌</div>;

  return (
    <div className="App">
      <h1>📊 Dashboard de Datos</h1>
      
      <div className="tabla">
        <h2>Datos de la Base de Datos</h2>
        <table>
          <thead>
            <tr>
              {datos.length > 0 && Object.keys(datos[0]).map(key => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {datos.slice(0, 10).map((fila, index) => (
              <tr key={index}>
                {Object.values(fila).map((valor, i) => (
                  <td key={i}>{valor}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grafico">
        <h2>Gráfico de Ejemplo</h2>
        <BarChart width={600} height={300} data={datos.slice(0, 10)}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={datos.length > 0 ? Object.keys(datos[0])[0] : ''} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={datos.length > 0 ? Object.keys(datos[0])[1] : ''} fill="#8884d8" />
        </BarChart>
      </div>
    </div>
  );
}

export default App;