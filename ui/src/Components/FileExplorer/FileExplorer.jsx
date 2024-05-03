import React, { useEffect, useState } from "react";
import styles from "./FileExplorer.module.css";
import Explorer from "./Explorer.jsx";

import { useZustandStore } from "../../store";

import { get_file_structure } from "../../api/getFilesStructure";

const FileExplorer = () => {
  const [files, setFiles] = useState();

  const {
    selectedProject,
    theme,
    messages
  } = useZustandStore();

  const fetchfiles = async () => {
    try {
      const formData = new FormData();
      formData.append("root_dir", `data/${selectedProject}`);

      const data = await get_file_structure(formData);

      setFiles(JSON.parse(data));
      console.log("Files Structure : " , JSON.parse(data));
    } catch (error) {
      console.error("Error fetching audio files:", error);
    }
  };

  useEffect(() => {
    try {
      fetchfiles();
    } catch (err) {
      console.error(err);
    }
  }, [messages ,  selectedProject]);

  return (
    <div className={styles.exp}>
      <div>{files ? <Explorer data={files} /> : <p>Loading...</p>}</div>
      <footer>Click on the file to acces them in the code editor.</footer>
    </div>
  );
};

export default FileExplorer;
