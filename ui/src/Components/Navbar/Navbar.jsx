import React, { useEffect, useRef, useState } from "react";
import css from "./Navbar.module.css";
import { useZustandStore } from "../../store";
import styles from "./Navbar.module.css";
import { fetch_projects } from "../../api/getprojects";
import { getprojectData } from "../../api/getprojectData";

function Navbar() {
  const {
    projectList,
    setprojectlist,
    selectedProject,
    setselectedProject,
    selectedProject_id,
    setselectedProject_id,
    messages,
    setMessages,
    theme,
    setFiles,
    setplan
  } = useZustandStore();

  useEffect(() => {
    setFiles([]);
    setplan([]);
  }, [selectedProject]);

  useEffect(() => {
    getprojects();
  }, []);

  useEffect(() => {
    console.log("project List : ", projectList);
  }, [projectList]);

  const getprojects = async () => {
    try {
      const data = await fetch_projects();
      console.log("Projectsss : ", data);

      setprojectlist(data);
    } catch (err) {
      console.error("Error in getprojects. : ", err);
    }
  };

  const [isOpen, setIsOpen] = useState(false);
  const [isnew, setisnew] = useState(false);

  const handleSelectProject = async (project) => {
    try {
      setIsOpen(false);
      if (isnew) setisnew(false);
      setselectedProject(project);

      const data = await getprojectData(project);
      // console.log("Chat History : " , data.OI_chat);
      const chat_history = data;
      let msgs = [];

      for (const item of chat_history) {
        console.log("Item : ", item);

        if (item?.user_query) {
          msgs.push({
            text: item?.user_query,
            sender: "user",
          });
        }

        if (item?.summary_text) {
          msgs.push({ text: item?.summary_text, sender: "bot" });
        }
      }
      setMessages(msgs);
    } catch (err) {
      console.error("Error in get chat. : ", err);
    }
  };

  const newprojectref = useRef(null);

  useEffect(() => {
    if (newprojectref?.current?.focus());
  }, [isnew]);

  const handleCreateNewProject = async (project_name) => {
    try {
      if (!project_name) return;
      setIsOpen(false);
      // console.log("Create new project.");

      const formData = new FormData();
      formData.append("project_name", project_name);

      const backend_res = await fetch(
        `${process.env.REACT_APP_BACKEND}/create_project`,
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

      console.log("Project listttt : " , res_text.includes("message"));

      if(res_text.includes("message")){
        alert("Project alreday exists.");
      }

      const data = JSON.parse(res_text);

      setselectedProject(data.project_name);
      getprojects();
      setMessages([]);
    } catch (err) {
      console.error("Error in create project. : ", err);
    }
  };

  return (
    <>
      <div
        className={`${css.navbar} ${theme === "Dark" ? styles.darkmode : null}`}
      >
        <div
          className={`${styles.dropdown} ${
            theme === "Dark" ? styles.projectmode : null
          }`}
        >
          <div
            className={`${styles.selectedOption} ${
              theme === "Dark" ? styles.projectmode : null
            }`}
            onClick={() => setIsOpen(!isOpen)}
          >
            {selectedProject ? selectedProject : "Select Project"}
          </div>
          {isOpen && (
            <ul
              className={`${styles.options} ${
                theme === "Dark" ? styles.optionlimode : null
              }`}
              onMouseLeave={() => (isOpen && !isnew ? setIsOpen(false) : null)}
            >
              {!isnew ? (
                <li
                  className={`${styles.createNew} ${
                    theme === "Dark"
                      ? styles.optionlimode
                      : styles.optionlilight
                  }`}
                  onClick={() => {
                    setisnew(true);
                  }}
                >
                  Create New Project
                </li>
              ) : (
                <li
                  className={`${styles.createNew} ${
                    theme === "Dark"
                      ? styles.optionlimode
                      : styles.optionlilight
                  }`}
                >
                  <input
                    style={{
                      border: "none",
                      padding: "5px",
                      background: "none",
                      outline: "none",
                    }}
                    className={`${styles.input} ${
                      theme === "Dark"
                        ? styles.optionlimode
                        : styles.optionlilight
                    }`}
                    ref={newprojectref}
                    type="text"
                    placeholder="Porject Name"
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        setisnew(false);
                        handleCreateNewProject(e.target.value);
                        e.target.value = "";
                      }
                    }}
                  />
                </li>
              )}
              {projectList &&
                projectList.length > 0 &&
                projectList.map(
                  (project, index) =>
                    project !== "" && (
                      <li
                        key={index}
                        className={`${
                          theme === "Dark"
                            ? styles.optionlimode
                            : styles.optionlilight
                        }`}
                        onClick={() => handleSelectProject(project)}
                      >
                        {project}
                      </li>
                    )
                )}
            </ul>
          )}
        </div>

        <div className={styles.internet}>
          <div className={styles.dot}>
            {window.navigator.onLine ? (
              <div className={styles.greendot}></div>
            ) : (
              <div className={styles.reddot}></div>
            )}
          </div>
          <div className={styles.text}>Internet</div>
        </div>
      </div>
    </>
  );
}

export default Navbar;
