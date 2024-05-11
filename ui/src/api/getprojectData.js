export const getprojectData = async(projectName)=>{
    const formData = new FormData();
      formData.append("project_name", projectName);

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

      return data;
}