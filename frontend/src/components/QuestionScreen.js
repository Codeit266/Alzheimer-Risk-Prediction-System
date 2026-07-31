import Recorder from "./Recorder";

function QuestionScreen({ questionNumber, question, onAnswer }) {
  return (
    <div className="screen">
      <h2 className="screenTitle">
        Question {questionNumber}
      </h2>

      <p className="questionText">
        {question}
      </p>

      <Recorder onResult={onAnswer} />
    </div>
  );
}

export default QuestionScreen;