import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import UserForm from './App.jsx'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatInterface from './chatinterface.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<UserForm />} />
        <Route path='/chat_interface' element = {<ChatInterface />}></Route>
      </Routes>
    </Router>
  </StrictMode>,
)
