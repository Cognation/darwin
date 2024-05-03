import axios from "axios";

export const getFileData = async (formData) => {
  try {
    const file_res = await axios.get(
        `${process.env.REACT_APP_BACKEND}/files_data/${formData}`,
        {
          headers: {
            Accept: "*",
          },
        }
      );
  
      return file_res;
  } catch (err) {
    console.error(err);
  }
};