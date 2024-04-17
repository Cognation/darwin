import React, { useEffect, useRef, useState } from "react";
import css from "./Navbar.module.css";
import { useZustandStore } from "../../store";
import styles from "./Navbar.module.css";

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
  } = useZustandStore();

  useEffect(() => {
    getprojects();
  }, []);

  const getprojects = async () => {
    try {
      const projects = await fetch(
        `${process.env.REACT_APP_BACKEND}/get_project_ids`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            type: "formData",
          },
        }
      );

      const data = JSON.parse(await projects.text());
      // console.log("Projects : ", data);

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
      setselectedProject(project.project_name);
      setselectedProject_id(project.project_id);

      const formData = new FormData();
      formData.append("project_id", project.project_id);

      const chat = await fetch(
        `${process.env.REACT_APP_BACKEND}/get_project_data`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            type: "formData",
          },
          body: formData,
        }
      );

      const data = JSON.parse(await chat.text());
      // console.log("Chat History : " , data.OI_chat);
      const chat_history = data.OI_chat;
      let msgs = [];

      for (const item of chat_history) {
        msgs.push({
          text: item?.User ? item?.User : item?.Assistant,
          sender: item?.User ? "user" : "bot",
        });
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

      const data = JSON.parse(res_text);

      // console.log("Create project res : ", data.project_id);
      // console.log("Create project res : ", data.project_name);

      setselectedProject(data.project_name);
      setselectedProject_id(data.project_id);
      getprojects();
      setMessages([]);
    } catch (err) {
      console.error("Error in create project. : ", err);
    }
  };

  return (
    <>
      <div className={css.navbar}>
        <div
          className={styles.dropdown}
          onClick={() => {
            setIsOpen(true);
          }}
        >
          <div
            className={styles.selectedOption}
            onClick={() => setIsOpen(!isOpen)}
          >
            {selectedProject ? selectedProject : "Select Project"}
          </div>
          {isOpen && (
            <ul
              className={styles.options}
              onMouseLeave={() => (isOpen && !isnew ? setIsOpen(false) : null)}
            >
              {!isnew ? (
                <li
                  className={styles.createNew}
                  onClick={() => {
                    setisnew(true);
                  }}
                >
                  Create New Project
                </li>
              ) : (
                <li className={styles.createNew}>
                  <input
                    style={{
                      border: "none",
                      padding: "5px",
                      background: "none",
                      outline: "none",
                    }}
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
              {projectList && projectList.length>0 && projectList.map((project, index) => (
                <li key={index} onClick={() => handleSelectProject(project)}>
                  {project.project_name}
                </li>
              ))}
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
          Internet
        </div>
      </div>
    </>
  );
}

export default Navbar;
