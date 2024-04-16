// App.js

import React, { useEffect, useRef, useState } from "react";
import styles from "./Code.module.css";
import { useZustandStore } from "../../store";
import Terminal, {
  ColorMode,
  TerminalInput,
  TerminalOutput,
} from "react-terminal-ui";
import Editor from "@monaco-editor/react";
import { v4 as uuidv4 } from "uuid";

const Code = () => {
  const {
    messages,
    setMessages,
    selected,
    setselected,
    selectedProject_id,
    selectedProject,
  } = useZustandStore();
  const [code, setcode] = useState(
    `print("Here is your personal software engineer 🙂")`
  );
  const [language, setlanguage] = useState("python");
  const [input_msg, setinput_msg] = useState("");
  const [editor_width, seteditor_width] = useState(true);
  const [fileName, setFileName] = useState("");
  const [projects, setprojects] = useState([]);
  const [istyping, setistyping] = useState(false);

  // const sessionId = uuidv4();

  const inputref = useRef(null);

  useEffect(() => {
    inputref?.current?.focus();
    // fetchprojects();
  }, []);

  const msgref = useRef(null);
  const msgref2 = useRef(null);

  useEffect(() => {
    msgref?.current?.scrollIntoView({ behavior: "smooth" });
    msgref2?.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, code, language, input_msg]);

  const [colorMode, setColorMode] = useState(ColorMode.Dark);
  const [lineData, setLineData] = useState([
    <TerminalOutput>Output will appear here!!</TerminalOutput>,
  ]);

  const yellowBtnClick = () => {
    // console.log("Clicked the yellow button.");
  };

  const greenBtnClick = () => {
    // console.log("Clicked the green button.");
  };
  const redBtnClick = () => {
    // console.log("Clicked the red button.");
  };

  async function onInput(input) {
    let ld = [...lineData];
    ld.push(<TerminalInput>{input}</TerminalInput>);
    if (input.toLocaleLowerCase().trim() === "clear") {
      ld = [];
    }
    setLineData(ld);
  }

  function handleEditorValidation(markers) {
    // model markers
    markers.forEach((marker) => console.log("onValidate:", marker.message));
  }

  // Function to handle sending a message
  const sendMessage = async (message) => {
    if(!selectedProject){
      alert("Please select the project first.");
      return;
    }
    setistyping(true);
    let msgs = messages;
    msgs.push({ text: message, sender: "user" });
    let codee = "";
    let ld = [<TerminalOutput>Output will appear here!!</TerminalOutput>];

    const formData = new FormData();
    formData.append("project_id", selectedProject_id);
    formData.append("session_id", 1);
    formData.append("customer_message", message);

    try {
      const backend_res = await fetch(
        `${process.env.REACT_APP_BACKEND}/chat`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            type: "formData",
          },
          body: formData,
        }
      );

      const res_text = await backend_res.text();

      // console.log("Res : ", res_text);

      if (!res_text) {
        alert("Some error occured");
        return;
      }

      if (res_text[0] === "{" && res_text[1] === `"`) {
        const res_json = JSON.parse(res_text);
        setistyping(false);
        msgs.push({ text: res_json.message, sender: "bot" });
        setMessages(msgs);
        return;
      }

      if (res_text[0] !== "[" && res_text[1] !== "{") {
        setistyping(false);
        msgs.push({
          text: res_text.substring(1, res_text.length - 1),
          sender: "bot",
        });
        setMessages(msgs);
        return;
      }

      const res_json = JSON.parse(res_text);

      setistyping(false);

      // console.log("Res : ", res_json);

      for (let item of res_json) {
        // console.log("Item : ", item);

        if (item?.type === "message" && item.role !== "user") {
          msgs.push({ text: item.content, sender: "bot" });
          setMessages(msgs);
        }

        if (item?.type === "code") {
          codee += item?.content + "\n\n\n";
          setcode(codee);
          setlanguage(item?.format);
        }

        if (item?.type === "console" && item?.format === "output") {
          ld.push(<TerminalInput>{item?.content}</TerminalInput>);
          setLineData(ld);
        }
      }

      // if (res_text[0] === "[" && res_text[1] === "{") {
      //   const res_json = JSON.parse(res_text);

      //   for(let item of res_json){
      //       console.log("Item : " , item);
      //   }

      //   setlanguage(res_json[2]?.format);

      //   setcode(res_json[2].content);

      //   // console.log("JSon : ", res_json);

      //   msgs.pop();
      //   msgs.push({ text: res_json[1].content, sender: "bot" });
      //   msgs.push({ text: res_json[4].content, sender: "bot" });
      //   setMessages(msgs);

      //   let ld = [<TerminalOutput>Output will appear here!!</TerminalOutput>];
      //   ld.push(<TerminalInput>{res_json[3].content}</TerminalInput>);
      //   setLineData(ld);
      // } else {
      //   msgs.pop();

      //   try{
      //     const internet_res = JSON.parse(res_text);

      //     if(internet_res && internet_res.message){
      //       console.log("Internet Res : " , internet_res.message);
      //       msgs.push({ text: internet_res.message, sender: "bot" });
      //       setMessages(msgs);
      //       return;
      //     }
      //   }
      //   catch(err){
      //     console.error(err);
      //   }
      //   msgs.push({ text: res_text, sender: "bot" });
      //   setMessages(msgs);
      // }
    } catch (err) {
      console.log(err);
      return;
    }
  };

  return (
    <div className={styles.container}>
      <div
        className={`${editor_width ? styles.chatbotBox : styles.chatbotBox2}`}
      >
        {/* <div className={styles.chatHeader}>Chatbot</div> */}
        <div className={styles.messageContainer}>
          {/* Render messages */}
          {messages && messages.length>0 && messages.map((message, index) => {
            const texts = message?.text?.split("\n");
            return (
              <div key={index + 11}>
                <div
                  key={index + 2}
                  className={`${styles.message} ${styles[message.sender]}`}
                >
                  { texts && texts.length>0 && texts.map((item, index) => {
                    if (
                      item &&
                      index === texts.length - 2 &&
                      !texts[index + 1]
                    ) {
                      return (
                        <>
                          {item.startsWith("**") && item.endsWith("**") ? (
                            <span key={index}>
                              <b className={styles.b}>
                                <span>
                                  {item.substring(2, item.length - 2)}
                                </span>
                              </b>
                            </span>
                          ) : item.startsWith("#") ? (
                            <span key={index}>
                              <b className={styles.b}>
                                <span>{item.replaceAll("#", "")}</span>
                              </b>
                            </span>
                          ) : (
                            <span key={index}>
                              <span>{item}</span>
                            </span>
                          )}
                        </>
                      );
                    } else if (item) {
                      if (index !== texts.length - 1) {
                        return (
                          <>
                            {item.startsWith("**") && item.endsWith("**") ? (
                              <span key={index}>
                                <b>
                                  <span>
                                    {item.substring(2, item.length - 2)}
                                  </span>
                                </b>
                                <br />
                                <br />
                              </span>
                            ) : item.startsWith("#") ? (
                              <span key={index}>
                                <b>
                                  <span>{item.replaceAll("#", "")}</span>
                                </b>
                                <br />
                                <br />
                              </span>
                            ) : (
                              <span key={index}>
                                <span>{item}</span>
                                <br />
                                <br />
                              </span>
                            )}
                          </>
                        );
                      } else {
                        return (
                          <>
                            {item.startsWith("**") && item.endsWith("**") ? (
                              <span key={index}>
                                <b className={styles.b}>
                                  <span>
                                    {item.substring(2, item.length - 2)}
                                  </span>
                                </b>
                              </span>
                            ) : item.startsWith("#") ? (
                              <span key={index}>
                                <b className={styles.b}>
                                  <span>{item.replaceAll("#", "")}</span>
                                </b>
                              </span>
                            ) : (
                              <span key={index}>
                                <span>{item}</span>
                              </span>
                            )}
                          </>
                        );
                      }
                    }
                  })}
                </div>
              </div>
            );
          })}
          {istyping ? (
            <div ref={msgref2} className={`${styles.message} ${styles["bot"]}`}>
              Typing...
            </div>
          ) : (
            ""
          )}
          <div ref={msgref}></div>
        </div>
        <textarea
          type="text"
          ref={inputref}
          value={input_msg}
          rows={input_msg ? 10 : 1}
          placeholder="Message Darwin"
          onChange={(e) => {
            setinput_msg(e.target.value);
          }}
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              e.target.value = "";
              setinput_msg("");
              sendMessage(input_msg);
            }
          }}
          className={styles.input}
        />
      </div>

      <div className={styles.otherBoxes}>
        <ul className={styles.ul}>
          <li
            className={styles.li}
            onClick={(e) => {
              seteditor_width(!editor_width);
            }}
          >
            {/* <img src={editor_width ? arrow_left : arrow_right} alt="" /> */}

            {!editor_width ? (
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
          {/*<li
            className={`${styles.li} ${
              selected === "screenshot" ? styles.selected : null
            }`}
            name="screenshot"
            onClick={(e) => {
              setselected("screenshot");
            }}
          >
            Screenshot
          </li>*/}
        </ul>
        <div className={styles.box}>
          {selected === "terminal" ? (
            <div className={styles.box} key={1}>
              <Terminal
                className={styles.terminal}
                name="Terminal"
                colorMode={colorMode}
                height={"600px"}
                // height={"100%"}
                onInput={onInput}
                redBtnCallback={redBtnClick}
                yellowBtnCallback={yellowBtnClick}
                greenBtnCallback={greenBtnClick}
              >
                {lineData}
              </Terminal>
            </div>
          ) : null}

          {selected === "code_editor" ? (
            <div className={styles.box} key={2}>
              {/* <CodeMirror 
              value={code} 
              height="500px" 
              theme={vscodeDark} 
              // theme="vs-dark"
              options={{
                inlineSuggest: true,
                fontSize: "16px",
                formatOnType: true,
                autoClosingBrackets: true,
                minimap: { scale: 10 }
              }}
              /> */}

              <Editor
                className={styles.editor}
                height="100%"
                width="100%"
                theme="vs-dark"
                language={language}
                value={code}
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

              {/* <Editor
      value={code}
      padding={10}
      onValueChange={(code) => setcode(code)}
      highlight={(code) => highlight(code, languages.js)}
      style={{
        fontFamily: "monospace",
        fontSize: 17,
        border: "1px solid black"
      }}
    /> */}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Code;
