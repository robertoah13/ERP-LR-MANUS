import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Clientes from './pages/Clientes'
import Pacientes from './pages/Pacientes'
import OrdensServico from './pages/OrdensServico'
import Producao from './pages/Producao'
import Estoque from './pages/Estoque'
import Financeiro from './pages/Financeiro'
import Agenda from './pages/Agenda'
import Login from './pages/Login'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/clientes" element={<Clientes />} />
          <Route path="/pacientes" element={<Pacientes />} />
          <Route path="/ordens-servico" element={<OrdensServico />} />
          <Route path="/producao" element={<Producao />} />
          <Route path="/estoque" element={<Estoque />} />
          <Route path="/financeiro" element={<Financeiro />} />
          <Route path="/agenda" element={<Agenda />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
