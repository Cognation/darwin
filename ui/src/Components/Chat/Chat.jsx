import React from "react";
import styles from "./Chat.module.css";
import { useZustandStore } from "../../store";

function Chat({
  msgref,
  msgref2,
  issettingopen,
  istyping,
  inputref,
  input_msg,
  sendMessage,
  setinput_msg,
}) {
  const { messages, theme } = useZustandStore();

  return (
    <div className={`${styles.messages}`}>
      <>
        <div className={styles.messageContainer}>
          {messages &&
            messages.length > 0 &&
            messages.map((message, index) => {
              const texts = message?.text?.split("\n");
              return (
                <div key={index + 11}>
                  <div
                    key={index + 2}
                    className={`${styles.message} ${styles[message.sender]}`}
                  >
                    {texts &&
                      texts.length > 0 &&
                      texts.map((item, index) => {
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
                                {item.startsWith("**") &&
                                item.endsWith("**") ? (
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
                                {item.startsWith("**") &&
                                item.endsWith("**") ? (
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
          {!issettingopen && istyping ? (
            <div ref={msgref2} className={`${styles.message} ${styles["bot"]}`}>
              Typing...
            </div>
          ) : (
            ""
          )}
          <div ref={msgref}></div>
          {/* ) : (
            <Setting />
          )} */}
        </div>
        <textarea
          type="text"
          ref={inputref}
          value={input_msg}
          rows={
            input_msg.split(" ").length > 20 || input_msg.length > 50 ? 10 : 1
          }
          placeholder="Ask Darwin..."
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
          className={`${styles.input} ${
            theme === "Dark" ? styles.darkmode_input : null
          }`}
        />
      </>
    </div>
  );
}

export default Chat;
