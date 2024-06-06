export const getstream = async (formData) => {
    try {
      const backend_res = await fetch(`${process.env.REACT_APP_BACKEND}/stream`, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });
  
      const res_text = backend_res;
      return res_text;
    } catch (err) {
      console.error(err);
    }
  };
  