import axios from "axios";

const API_URL = "http://127.0.0.1:5000/analyze";

export const sendAudio = async (audioBlob, question = "") => {

  const formData = new FormData();
  formData.append("audio", audioBlob, "audio.webm");
  if (question) {
    formData.append("question", question);
  }

  try {

    const response = await axios.post(API_URL, formData);

    return response.data;

  } catch (error) {

    if (error.response && error.response.data.error) {
      return { error: error.response.data.error };
    }

    return { error: "Something went wrong. Please try again." };
  }
};