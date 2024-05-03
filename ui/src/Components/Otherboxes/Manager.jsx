import React, { useEffect, useState } from "react";
import styles from "./Manager.module.css";
import { useZustandStore } from "../../store";
import Terminal, {
  ColorMode,
  TerminalInput,
  TerminalOutput,
} from "react-terminal-ui";
import Editor from "@monaco-editor/react";
import FileEx from "../FileExplorer/FileExplorer";
import Planner from "../Planner/Planner";

function Manager({ colorMode, lineData, plan }) {
  const {
    selected,
    setselected,
    files,
    editor_expanded,
    setEditor_expanded,
    setselected_file,
    selected_file,
    selected_file_language,
    setselected_file_language,
  } = useZustandStore();

  const yellowBtnClick = () => {
    // console.log("Clicked the yellow button.");
  };

  const greenBtnClick = () => {
    // console.log("Clicked the green button.");
  };
  const redBtnClick = () => {
    // console.log("Clicked the red button.");
  };

  function handleEditorValidation(markers) {
    // model markers
    markers.forEach((marker) => console.log("onValidate:", marker.message));
  }

  const handleFileChange = (file) => {
    if (
      selected_file?.code === file?.code &&
      selected_file?.filename === file?.filename
    ) {
      return;
    }
    setselected_file(file);
    console.log("Code : ", file?.code);
    console.log("Language : ", file?.language);
    if (file?.language === "js") {
      setselected_file_language("javascript");
    } else if (file?.language === "py") {
      setselected_file_language("python");
    }else if (file?.language === "cpp") {
      setselected_file_language("cpp");
    }else if (file?.language === "c") {
      setselected_file_language("c");
    } else {
      setselected_file_language(file?.language);
    }
    setcode(file?.code);
  };

  const [code, setcode] = useState(
    `print("Here is your personal software engineer 🙂")`
  );

  return (
    <div className={styles.otherBoxes}>
      <ul className={styles.ul}>
        <li
          className={styles.li}
          onClick={(e) => {
            setEditor_expanded(!editor_expanded);
          }}
        >
          {!editor_expanded ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
            >
              <polygon points="7.293 4.707 14.586 12 7.293 19.293 8.707 20.707 17.414 12 8.707 3.293 7.293 4.707" />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
            >
              <polygon
                points="7.293 4.707 14.586 12 7.293 19.293 8.707 20.707 17.414 12 8.707 3.293 7.293 4.707"
                transform="rotate(180 12 12)"
              />
            </svg>
          )}
        </li>
        <li
          className={`${styles.li} ${
            selected === "terminal" ? styles.selected : null
          }`}
          name="terminal"
          onClick={(e) => {
            setselected("terminal");
          }}
        >
          Terminal
        </li>
        <li
          className={`${styles.li} ${
            selected === "code_editor" ? styles.selected : null
          }`}
          name="code_editor"
          onClick={(e) => {
            setselected("code_editor");
          }}
        >
          Code Editor
        </li>
        <li
          className={`${styles.li} ${
            selected === "file_explorer" ? styles.selected : null
          }`}
          name="file_explorer"
          onClick={(e) => {
            setselected("file_explorer");
          }}
        >
          File Explorer
        </li>
        <li
          className={`${styles.li} ${
            selected === "planner" ? styles.selected : null
          }`}
          name="planner"
          onClick={(e) => {
            setselected("planner");
          }}
        >
          Planner
        </li>
      </ul>
      <div className={`${styles.box}`}>
        {selected === "terminal" ? (
          <div className={styles.box} key={1}>
            <Terminal
              className={styles.terminal}
              colorMode={colorMode}
              height={"600px"}
              // height={"100%"}
              // onInput={onInput}
              redBtnCallback={redBtnClick}
              yellowBtnCallback={yellowBtnClick}
              greenBtnCallback={greenBtnClick}
            >
              {lineData}
            </Terminal>
          </div>
        ) : null}

        {selected === "code_editor" ? (
          <>
            {files.length > 0 ? (
              <div className={styles.files}>
                {files.length > 0 &&
                  files.map((file, index) => (
                    <>
                      <div
                        key={index}
                        className={`${
                          selected_file?.code === file?.code
                            ? styles.code_selected
                            : styles.file_button
                        }`}
                        onClick={() => handleFileChange(file)}
                      >
                        {file?.filename}
                      </div>
                    </>
                  ))}
              </div>
            ) : null}
            <div className={styles.box} key={2}>
              <Editor
                className={styles.editor}
                height="100%"
                width="100%"
                theme="vs-dark"
                language={selected_file_language || "python"}
                value={selected_file?.code}
                onChange={(code) => setcode(code)}
                options={{
                  inlineSuggest: true,
                  fontSize: "16px",
                  formatOnType: true,
                  autoClosingBrackets: true,
                  minimap: { scale: 10 },
                }}
                onValidate={handleEditorValidation}
              />
            </div>
          </>
        ) : null}

        {selected === "file_explorer" ? <FileEx /> : null}

        {selected === "planner" ? <Planner plan={plan} /> : null}
      </div>
    </div>
  );
}

export default Manager;
