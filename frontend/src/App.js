import { useState } from "react";
import axios from "axios";

import Header from "./components/Header";
import StartScreen from "./components/StartScreen";
import QuestionScreen from "./components/QuestionScreen";
import ResultScreen from "./components/ResultScreen";

import questions from "./questions";
import { sendAudio } from "./services/api";

import "./theme.css";

function App() {
  const [started, setStarted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [answers, setAnswers] = useState([]);
  const [result, setResult] = useState(null);

  const currentQuestions = questions;

  const startTest = () => {
    setStarted(true);
  };

  const handleAnswer = async (audioBlob) => {
    const currentQuestionText = currentQuestions[currentQuestion];
    const response = await sendAudio(audioBlob, currentQuestionText);

    if (response.error) {
      alert(response.error);
      return;
    }

    const responseWithQuestion = {
      ...response,
      question: currentQuestionText
    };

    const updated = [...answers, responseWithQuestion];
    setAnswers(updated);

    const next = currentQuestion + 1;

    if (next < currentQuestions.length) {
      setCurrentQuestion(next);
    } else {
      const combinedText = updated
        .map(r => r.transcript)
        .join(" ");

      const combinedDuration = updated.reduce((sum, r) => sum + (r.duration || 0), 0);
      const combinedPauses = updated.reduce((sum, r) => sum + (r.features?.pause_count || 0), 0);

      console.log("Final Transcript:", combinedText);
      console.log("Final Duration:", combinedDuration);
      console.log("Final Pauses:", combinedPauses);

      const finalRes = await axios.post(
        "http://127.0.0.1:5000/final_predict",
        {
          transcript: combinedText,
          duration: combinedDuration,
          pause_count: combinedPauses
        }
      );

      setResult(finalRes.data);
      setCurrentQuestion(next);
    }
  };

  return (
    <div className="app">
      <div className="bg">
        <div className="circle c1"></div>
        <div className="circle c2"></div>
        <div className="circle c3"></div>
      </div>

      <Header />

      {!started && (
        <StartScreen startTest={startTest} />
      )}

      {started && currentQuestion < currentQuestions.length && (
        <QuestionScreen
          questionNumber={currentQuestion + 1}
          question={currentQuestions[currentQuestion]}
          onAnswer={handleAnswer}
        />
      )}

      {started && currentQuestion >= currentQuestions.length && result && (
        <ResultScreen result={result} answers={answers} />
      )}
    </div>
  );
}

export default App;