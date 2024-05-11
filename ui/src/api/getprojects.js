export const fetch_projects = async () => {
  const projects = await fetch(
    `${process.env.REACT_APP_BACKEND}/get_project_names`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        type: "formData",
      },
    }
  );

  const data = JSON.parse(await projects.text());
  console.log("Projects : ", data);

  return data;
};
