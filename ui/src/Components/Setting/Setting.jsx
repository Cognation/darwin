import React, { useEffect, useState } from "react";
import styles from "./Setting.module.css";
import { useZustandStore } from "../../store";

function Setting() {
  const [isOpen, setIsOpen] = useState(false);

  const { theme, setTheme } = useZustandStore();

  const [th , setth] = useState("System");

  useEffect(() => {
    console.log(theme);
  }, [theme]);

  const handleThemeChange = (selectedTheme) => {
    setTheme(selectedTheme);
    setth(selectedTheme);
    setIsOpen(false); // Close dropdown after selecting a theme
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`${styles.setting} ${theme==="Dark" ? styles.darkmode : null} `}>
      <div className={styles.themeSelector}>
        <div className={`${styles.text} `}>Mode : </div>
        <div className={`${styles.dropdown} ${theme==="Dark" ? styles.darkmode_dropdown : null}`} onClick={toggleDropdown}>
          <div className={`${styles.selectedTheme} ${theme==="Dark" ? styles.textmode : null}`}>{th}</div>
          {isOpen ? (
            <div className={`${styles.dropdownContent} ${theme==="Dark" ? styles.darkmode :null}`}>
              <div
                className={styles.option}
                onClick={() => handleThemeChange("Dark")}
              >
                Dark
              </div>
              <div
                className={styles.option}
                onClick={() => handleThemeChange("Light")}
              >
                Light
              </div>
              <div
                className={styles.option}
                onClick={() => handleThemeChange("System")}
              >
                System
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default Setting;
