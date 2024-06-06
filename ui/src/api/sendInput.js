export const sendInput = async (formData) => {
    try {
      const backend_res = await fetch(`${process.env.REACT_APP_BACKEND}/in/response`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          type: "formData",
        },
        body: formData,
      });
  
      const res_text = backend_res;
      return res_text;
    } catch (err) {
      console.error(err);
    }
  };
  