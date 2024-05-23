import React from "react";
import styles from "./Landing.module.css";
import { ReactComponent as Robot } from "../../Assets/SVG/robot.svg";
import { ReactComponent as Flowchart } from "../../Assets/SVG/flowchart.svg";
import { ReactComponent as Brain } from "../../Assets/SVG/brain.svg";
import { ReactComponent as Blub } from "../../Assets/SVG/blub_1.svg";
import { ReactComponent as Books } from "../../Assets/SVG/books.svg";
import { ReactComponent as Setting } from "../../Assets/SVG/setting-white.svg";
import { ReactComponent as Laptop } from "../../Assets/SVG/laptop.svg";
import { ReactComponent as Tool } from "../../Assets/SVG/tool.svg";
import { ReactComponent as Arrow } from "../../Assets/SVG/arrow.svg";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className={styles.main}>
      <div className={styles.top}>
        <div className={`${styles.heading}`}>
          <h2>Darwin</h2>
        </div>
        <ul className={styles.top_ul}>
          <li className={styles.top_li}>
            <h2 className={styles.top_li_1}>
              Darwin 🤖 - AI Software Engineer Intern
            </h2>
            <p className={styles.top_li_1}>
              Darwin is the first in the series of multiple AI Engineers with
              the capability to comprehend complex human commands, dissect them
              into actionable steps, conduct research, and generate code to
              accomplish the specified task all powered by LLMs.
            </p>
          </li>
          <li className={styles.top_li}>
            <Robot />
          </li>
        </ul>
      </div>

      <div className={styles.features}>
        <h3>Features</h3>
        <ul className={styles.features_ul}>
          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Brain className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Capable of comprehending complex codebases and architectures
            </div>
          </li>

          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Tool className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Skillful in managing changes, updates, and bug fixes within
              software projects
            </div>
          </li>

          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Books className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Conducts thorough research to gather pertinent information
            </div>
          </li>

          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Blub className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Engages in brainstorming sessions to generate innovative ideas
            </div>
          </li>

          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Laptop className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Writes code in multiple programming languages proficiently
            </div>
          </li>

          <li className={styles.features_li}>
            <div className={`${styles.image}`}>
              <Setting className={`${styles.brain}`} />
            </div>
            <div className={`${styles.text}`}>
              Executing code and debugging using internet to assess discussions
              and forums, just like software engineers do 😉!
            </div>
          </li>
        </ul>
      </div>

      <div className={styles.info}>
        <p>
          Darwin is an early-stage AI Assistant chatbot designed to support your
          advanced development inquiries. To enhance your experience, please
          consider the following guidelines:
          <ul className={styles.info_ul}>
          <li>
            Ensure that your queries are comprehensive and detailed, covering
            all aspects of your request. Include links to any relevant issues or
            references to enable Darwin to provide more accurate and tailored
            responses.
          </li>
          <br />
          <li>
            If you encounter any difficulties, please raise issues or contact
            us. Your feedback is invaluable in helping us refine and improve
            your experience.
          </li>
          </ul>
        </p>
      </div>

      <div className={styles.roadmap}>
        <Flowchart className={styles.flowchart} />
        <Link to={"/code"} className={styles.link}>
          <div className={`${styles.try}`}>
            <i> Give it a try. </i>{" "}
            <span>
              <Arrow />
            </span>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Landing;
