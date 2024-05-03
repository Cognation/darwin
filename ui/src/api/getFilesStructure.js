export const get_file_structure = async (formData) => {
  try {

    console.log("Form Data : " , formData);
    const response = await fetch(
        `${process.env.REACT_APP_BACKEND}/folder_structure`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            type: "formData",
          },
          body: formData,
        }
      );
  
      const data = await response.text();
  
      return data;
  } catch (err) {
    console.error(err);
  }
};
