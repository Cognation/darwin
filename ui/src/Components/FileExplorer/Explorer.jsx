// FileExplorer.js
import React from "react";
import styles from "./Explorer.module.css";
import { useZustandStore } from "../../store";

const FileExplorer = ({ data }) => {
  // const [expandedNodes, setExpandedNodes] = useState({});

  const {
    files,
    setFiles,
    expandedNodes,
    setExpandedNodes,
    theme,
    selectedProject,
    setselected_file,
    selected_file,
  } = useZustandStore();

  function extractExtension(filename) {
    const lastDotIndex = filename.lastIndexOf(".");
    const lastSlashIndex = filename.lastIndexOf("/"); // Check for any directory separators

    // If there's no dot or the dot is before the last slash, return an empty string
    if (
      lastDotIndex === -1 ||
      (lastSlashIndex !== -1 && lastDotIndex < lastSlashIndex)
    ) {
      return "python";
    }

    return filename.substring(lastDotIndex + 1);
  }

  const toggleNode = (path) => {
    const newexpanded = expandedNodes;
    newexpanded[path] = !expandedNodes[path];
    setExpandedNodes(newexpanded);
  };

  const fetch_file_content = async (path, name) => {
    try {
      const isFilePresent = files.some((file) => file.filename === name);

      if (isFilePresent) {
        const selectedFile = files.find((file) => file.filename === name);
        setselected_file(selectedFile);
        return;
      }

      const formData = new FormData();
      formData.append("path", path);

      const file_res = await fetch(
        `${process.env.REACT_APP_BACKEND}/serve_file`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            type: "formData",
          },
          body: formData,
        }
      );

      const data = await file_res.text();

      let newfile = files;

      newfile.push({
        filename: name,
        language: extractExtension(name),
        code: extractExtension(name) === "json" ? JSON.stringify(data) : data,
      });

      setFiles(newfile);
      setselected_file({
        filename: name,
        language: extractExtension(name),
        code: extractExtension(name) === "json" ? JSON.stringify(data) : data,
      });
    } catch (err) {
      console.error(err);
    }
  };

  const renderNode = (node, parentPath = "") => {
    if(node.name === "history.json") return;
    const fullPath = parentPath ? `${parentPath}/${node.name}` : node.name;
    const isExpanded = expandedNodes[fullPath];
    const hasChildren =
      node.type === "directory" && node.children && node.children.length > 0;

    return (
      <div
        className={`${styles.node} ${
          theme === "Dark" ? styles.textmode : null
        }`}
        key={fullPath}
      >
        <div
          className={`${styles.name} ${
            theme === "Dark" ? styles.textmode : null
          } ${
            node.type === "directory"
              ? styles.directory
              : theme === "Dark"
              ? styles.filedark
              : styles.file
          }`}
          onClick={() =>
            hasChildren
              ? toggleNode(fullPath)
              : fetch_file_content(fullPath, node.name)
          }
        >
          {hasChildren && (
            <span
              className={`${styles.arrow} ${
                theme === "Dark" ? styles.textmode : null
              } ${isExpanded ? styles.expanded : styles.collapsed}`}
            />
          )}
          {node.name}
        </div>
        {isExpanded && hasChildren && (
          <div className={styles.children}>
            {node.children.map((childNode) => renderNode(childNode, fullPath))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div
      className={`${styles.fileExplorer} ${
        theme === "Dark" ? styles.textmode : null
      }`}
    >
      {selectedProject ? (
        <div className={styles.tree}>{renderNode(data)}</div>
      ) : (
        <div>Please select a project.</div>
      )}
    </div>
  );
};

export default FileExplorer;
