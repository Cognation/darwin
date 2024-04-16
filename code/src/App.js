import './App.css';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { v1 } from 'uuid';
import Code from './Components/Code/Code';
import Failure from './Components/Failure/Failure.jsx';
import Navbar from './Components/Navbar/Navbar.jsx';

function App() {
  const uuidV1 = v1();
  const [sessId,setSessId] = useState(uuidV1.split('-')[0]);

  return (
    <div>
      <Router>
        <Routes>
          {/* <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} /> */}
          <Route path="/" element={<><Navbar/><Code sessId={sessId} setSessId={setSessId} /></>} />
          <Route path="/*" element={<Failure />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
