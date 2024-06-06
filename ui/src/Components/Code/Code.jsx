// App.js

import React, { useEffect, useRef, useState } from "react";
import styles from "./Code.module.css";
import { useZustandStore } from "../../store";
import Terminal, {
  ColorMode,
  TerminalInput,
  TerminalOutput,
} from "react-terminal-ui";
import Markdown from "react-markdown";

import { ReactComponent as SETTING_SVG } from "../../Assets/SVG/setting.svg";
import { ReactComponent as SETTING_SVG_WHITE } from "../../Assets/SVG/setting-white.svg";
import Setting from "../Setting/Setting";
import OtherBoxes from "../Otherboxes/Manager";
import { getCode } from "../../api/getCode";
import { getstream } from "../../api/getstream";
import { sendInput } from "../../api/sendInput";

const Code = () => {
  const {
    messages,
    setMessages,
    selected,
    setselected,
    selectedProject_id,
    selectedProject,
    files,
    setFiles,
    theme,
    editor_expanded,
    setEditor_expanded,
    plan,
    setplan,
  } = useZustandStore();
  const [code, setcode] = useState(
    `print("Here is your personal software engineer 🙂")`
  );
  const [language, setlanguage] = useState("python");
  const [input_msg, setinput_msg] = useState("");
  const [backendinput, setbackendinput] = useState("");
  const [istyping, setistyping] = useState(false);
  const [selected_file, setselected_file] = useState(null);
  const [id, setid] = useState(null);
  const [isinput, setisinput] = useState(false);
  // const [plan, setplan] = useState("");
  const [selected_file_language, setselected_file_language] = useState(
    selected_file?.language || "python"
  );
  const [issettingopen, setissettingopen] = useState(false);

  useEffect(() => {
    console.log("Backend input : ", backendinput);
  }, [backendinput]);

  useEffect(() => {
    console.log("selected file : ", selected_file);
    console.log("selected project : ", selectedProject);
  }, [selected_file, selectedProject]);

  const inputref = useRef(null);

  useEffect(() => {
    setplan("");
  }, [selectedProject]);

  useEffect(() => {
    inputref?.current?.focus();
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
    <TerminalOutput>$ ⎕</TerminalOutput>,
  ]);

  const callchat = async (message) => {
    if (!selectedProject) {
      // alert("Please select the project first.");
      return;
    }
    setistyping(true);
    let msgs = messages;
    msgs.push({ text: message, sender: "user" });
    setMessages(msgs);
    let ld = [<TerminalOutput>Output will appear here!!</TerminalOutput>];
    setLineData(ld);

    const formData = new FormData();
    formData.append("project_name", selectedProject);
    formData.append("customer_message", message);

    try {
      const res_text = await getCode(formData);

      if (!res_text) {
        // alert("Error in backend.");
        return;
      }

      console.log("Response : ", res_text);

      sendMessage(message, msgs);
    } catch (err) {
      console.error(err);
    }
  };

  const send_input = async () => {
    const formData = new FormData();
    formData.append("prompt_id", id);
    formData.append("response", backendinput);

    console.log("FormData : ", JSON.stringify(formData));

    const res_text = await sendInput(formData);

    const res_status = await res_text.text();

    console.log("Input req. ", res_status);

    if (JSON.parse(res_status).status === "OK") {
      let msgs = messages;
      msgs.push({ text: backendinput, sender: "user" });
      setMessages(msgs);
      setisinput(false);
    }
  };

  // Function to handle sending a message
  const sendMessage = async (message, msgs) => {
    // if (!selectedProject) {
    //   alert("Please select the project first.");
    //   return;
    // }
    // setistyping(true);
    // let msgs = messages;
    // msgs.push({ text: message, sender: "user" });
    // setMessages(msgs);
    // let ld = [<TerminalOutput>Output will appear here!!</TerminalOutput>];
    // setLineData(ld);
    let codee = "";

    let pl = plan;

    let iteration = 1;

    console.log(selectedProject);

    try {
      const res_text = await getstream();

      if (!res_text) {
        // alert("Error in backend.");
        return;
      }

      console.log("Response : ", res_text);

      const reader = res_text.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true && reader && decoder) {
        const { done, value } = await reader.read();
        if (done) {
          console.log("Done");
          setistyping(false);
          break;
        }

        const chunk = decoder.decode(value, { stream: true });

        console.log("Line : ", chunk);

        try {
          const data = chunk.trim().split("\n");

          data.forEach((element) => {
            const completeelm = JSON.parse(element);
            const out = completeelm?.out;
            console.log("Paresed Lines  : ", out);
            if (out) {
              pl = pl + out;
              pl.replaceAll("json" , "");
              pl.replaceAll("```json" , "");
              pl.replaceAll("json```" , "");
              setplan(pl);
            }

            if (completeelm && completeelm.in) {
              console.log("In : ", completeelm);
              const id = completeelm.prompt_id;
              console.log("ID : ", id);
              setisinput(true);
              setid(id);
              setbackendinput("");
            }
          });

          // if (data?.summary_text) {
          //   msgs.push({ text: data?.summary_text, sender: "bot" });
          //   setMessages(msgs);
          // }

          // if (data?.message) {
          //   pl = pl + `\n\n\n **Iteration :** ${iteration}\n\n${data?.message}`;
          //   iteration++;
          //   // pl.push(`${data?.message}\n\n`);
          //   setplan(pl);
          // }

          // if (data?.web_search) {
          //   pl =
          //     pl + `\n\n\n **Iteration :** ${iteration}\n\n${data?.web_search}`;
          //   iteration++;
          //   // pl.push(`${data?.web_search}\n\n`);
          //   setplan(pl);
          // }

          // if (data?.getIssueSummary) {
          //   pl =
          //     pl +
          //     `\n\n\n **Iteration :** ${iteration}\n\n${data?.getIssueSummary}`;
          //   iteration++;
          //   // pl.push(`${data?.web_search}\n\n`);
          //   setplan(pl);
          // }

          // if (data?.console) {
          //   let ld = lineData;
          //   ld.push(<TerminalInput>{data?.console}</TerminalInput>);
          //   ld.push(<TerminalInput>{`\n\n`}</TerminalInput>);
          //   setLineData(ld);
          // }
        } catch (err) {
          console.log("Error in parsing the content.", err);
        }

        // setTimeout(() => {
        //   let ld = lineData;
        //     ld.push(<TerminalInput>{`\n\n\n\n\n\n\n\n\n\n`}</TerminalInput>);
        //     setLineData(ld);
        // }, 1000);
      }
    } catch (err) {
      console.log(err);
      setistyping(false);
      // alert("Please try again.");
      return;
    }
  };

  return (
    <div className={`${styles.container} `}>
      <div
        className={`${styles.sidebar} ${
          theme === "Dark" ? styles.darkmode : null
        }`}
      >
        <button
          style={
            theme === "Ligth"
              ? { border: "none", background: "none", cursor: "pointer" }
              : { border: "none", background: "none", color: "white" }
          }
        >
          {theme === "Dark" ? (
            <SETTING_SVG_WHITE
              className={`${styles.sidebarli}`}
              onClick={() => {
                setissettingopen(!issettingopen);
              }}
            />
          ) : (
            <SETTING_SVG
              className={`${styles.sidebarli} `}
              onClick={() => {
                setissettingopen(!issettingopen);
              }}
            />
          )}
        </button>
      </div>
      <div
        className={`${
          editor_expanded ? styles.chatbotBox : styles.chatbotBox2
        }  ${theme === "Dark" && !issettingopen ? styles.darkmode : null}`}
      >
        {/* <div className={styles.chatHeader}>Chatbot</div> */}

        {!issettingopen ? (
          <>
            <div className={`${styles.messageContainer} `}>
              {messages &&
                messages.length > 0 &&
                messages.map((message, index) => {
                  // const texts = message?.text?.split("\n");
                  return (
                    <div key={index + 11}>
                      <div
                        key={index + 2}
                        className={`${styles.message} ${
                          styles[message.sender]
                        } ${
                          theme === "Dark"
                            ? message.sender === "user"
                              ? styles.userdarkmode
                              : styles.botdarkmode
                            : null
                        }`}
                      >
                        {message && message?.text && (
                          <Markdown>{message?.text}</Markdown>
                        )}
                      </div>
                    </div>
                  );
                })}
              <div ref={msgref}></div>
              {/* ) : (
            <Setting />
          )} */}
            </div>

            {!issettingopen && !istyping ? (
              <div
                ref={msgref2}
                className={`${styles.agent} ${
                  theme === "Dark" ? styles.agentdarkmode : null
                }`}
              >
                Agent is offline.
              </div>
            ) : (
              ""
            )}
            {!issettingopen && istyping ? (
              <div
                ref={msgref2}
                className={`${styles.agent} ${
                  theme === "Dark" ? styles.agentdarkmode : null
                }`}
              >
                Agent is online.
              </div>
            ) : (
              ""
            )}
            <textarea
              type="text"
              ref={inputref}
              value={!isinput ? input_msg : backendinput}
              rows={
                input_msg.split(" ").length > 20 || input_msg.length > 50
                  ? 10
                  : 1
              }
              placeholder="Ask Darwin..."
              onChange={(e) => {
                !isinput
                  ? setinput_msg(e.target.value)
                  : setbackendinput(e.target.value);
              }}
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  e.target.value = "";
                  setinput_msg("");
                  if (isinput) {
                    send_input();
                  } else {
                    callchat(input_msg);
                  }
                }
              }}
              className={`${styles.input} ${
                theme === "Dark" ? styles.darkmode_input : null
              }`}
            />
          </>
        ) : (
          <Setting />
        )}
      </div>

      <OtherBoxes colorMode={colorMode} lineData={lineData} plan={plan} />
    </div>
  );
};

export default Code;
