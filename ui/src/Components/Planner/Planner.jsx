import React, { useEffect, useRef } from "react";
import styles from "./Planner.module.css";
import { useZustandStore } from "../../store";
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm'

function Planner({ plan = ["Plan of execution will be displayed here!!"] }) {
  const { theme } = useZustandStore();

  const ref = useRef();

  useEffect(()=>{
    ref?.current?.scrollIntoView({ behavior: "smooth" });
  } , [plan]);

  return (
    <div
      className={`${styles.planner} ${
        theme === "Dark" ? styles.darkmode : styles.light
      }`}
    >
      <div className={`${styles.messageContainer}`}>
        { plan && plan.length>0 && <Markdown remarkPlugins={[[remarkGfm, {singleTilde: true}]]} className={styles.markdown}>{plan}</Markdown>}
      </div>
      <div ref={ref}></div>
    </div>
  );
}

export default Planner;
