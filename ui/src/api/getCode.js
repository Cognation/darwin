export const getCode = async (formData) => {
  try {
    const backend_res = await fetch(`${process.env.REACT_APP_BACKEND}/chat`, {
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
