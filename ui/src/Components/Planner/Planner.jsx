import React from "react";
import styles from "./Planner.module.css";
import { useZustandStore } from "../../store";
import Markdown from "react-markdown";

function Planner({ plan = ["Plan of execution will be displayed here!!"] }) {
  const { theme } = useZustandStore();

  return (
    <div
      className={`${styles.planner} ${
        theme === "Dark" ? styles.darkmode : styles.light
      }`}
    >
      {/* <div className={`${styles.messageContainer}`}>
              {plan &&
                plan.length > 0 &&
                plan.map((message, index) => {
                  const texts = message?.split("\n");
                  return (
                    <div key={index + 11}>
                      <div
                        key={index + 2}
                        className={`${styles.message} ${
                          styles[message.sender]
                        }`}
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
                                          <span>
                                            {item.replaceAll("#", "")}
                                          </span>
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
                                          <span>
                                            {item.replaceAll("#", "")}
                                          </span>
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
            </div> */}

      <div className={`${styles.messageContainer}`}>
        { plan && plan.length>0 && <Markdown>{plan}</Markdown>}
      </div>
    </div>
  );
}

export default Planner;
