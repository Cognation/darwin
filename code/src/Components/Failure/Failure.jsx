import classes from "./failure.module.css";

const Failure = () => {
  const handleclick = () => {
    if (window && window.location) {
      const port = window.location.port;
      window.location.href = `http://localhost:${port}`;
    }
  };
  return (
    <div className={classes.mainFail}>
      <h1 className={classes.headFail1}>404</h1>
      <h1 className={classes.headFail2}>This page is not found!</h1>

      <p style={{ color: "blue", cursor: "pointer" }} onClick={handleclick}>
        <u> Go to homepage</u>
      </p>
    </div>
  );
};

export default Failure;
