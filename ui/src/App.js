import "./App.css";
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { v1 } from "uuid";
import Code from "./Components/Code/Code";
import Failure from "./Components/Failure/Failure.jsx";
import Navbar from "./Components/Navbar/Navbar.jsx";
import Landing from "./Components/Landing/Landing.jsx";
import FileEx from "./Components/FileExplorer/FileExplorer.jsx";
import { useZustandStore } from "./store";

function App() {
  const uuidV1 = v1();
  const [sessId, setSessId] = useState(uuidV1.split("-")[0]);

  const { theme, setTheme } = useZustandStore();

  useEffect(() => {
    if (theme === "Dark") {
      const body = document.body;

      body.style.backgroundColor = "black";
    } else if (theme === "Light") {
      const body = document.body;

      body.style.backgroundColor = "white";
    }
  } , [theme]);

  useEffect(() => {
    if (theme === "System") {
      var body = document.body;
      const handleSystemThemeChange = (e) => {
        setTheme(e.matches ? "Dark" : "Light");
        if (e.matches) {
          body.style.backgroundColor = "black";
        }
      };

      const systemThemeMediaQuery = window.matchMedia(
        "(prefers-color-scheme: dark)"
      );
      systemThemeMediaQuery.addListener(handleSystemThemeChange);
      setTheme(systemThemeMediaQuery.matches ? "Dark" : "Light");
      if (systemThemeMediaQuery.matches) {
        body.style.backgroundColor = "black";
      }

      return () => {
        systemThemeMediaQuery.removeListener(handleSystemThemeChange);
      };
    }
  }, [theme]);

  return (
    <div>
      <Router>
        <Routes>
          {/* <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} /> */}
          <Route
            path="/"
            element={
              <>
              <Landing/>
              </>
            }
          />
          <Route
            path="/code"
            element={
              <>
                <Navbar />
                <Code sessId={sessId} setSessId={setSessId} />
              </>
            }
          />
          {/* <Route path="/file" element={<><FileEx/></>} /> */}
          <Route path="/*" element={<Failure />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
