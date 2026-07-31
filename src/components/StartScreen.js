import { useState } from "react";

function StartScreen({ startTest }) {
  const [checking, setChecking] = useState(false);

  const handleStart = async () => {
    setChecking(true);
    try {
      // Trigger browser's native microphone permission dialog
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(track => track.stop());
      setChecking(false);
      startTest();
    } catch (err) {
      console.error("Microphone permission check failed:", err);
      setChecking(false);
      startTest();
    }
  };

  return (
    <div className="screen">
      <h2 className="screenTitle">
        Welcome
      </h2>
      <p className="screenText">
        This system analyzes your speech patterns to detect early signs of Alzheimer's risk.
        <br /><br />
        To analyze your speech, click start screening and answer 3 short questions.
      </p>

      <button
        className="primaryBtn"
        onClick={handleStart}
        disabled={checking}
      >
        {checking ? "Requesting Access..." : "Start Screening"}
      </button>
    </div>
  );
}

export default StartScreen;