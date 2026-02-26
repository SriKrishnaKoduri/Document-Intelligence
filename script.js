async function askQuestion() {

  const questionInput = document.getElementById("questionInput");
  const resultBox = document.getElementById("resultBox");

  const answerText = document.getElementById("answerText");
  const confidence = document.getElementById("confidence");
  const similarity = document.getElementById("similarity");
  const source = document.getElementById("source");

  const question = questionInput.value.trim();

  if (!question) {
    alert("Please enter a question");
    return;
  }

  // Show loading
  answerText.innerText = "Loading answer...";
  resultBox.classList.remove("hidden");

  try {
    const response = await fetch(
      "https://krishna0506-document-intelligence.hf.space/ask-recruiter",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: question })
      }
    );

    const data = await response.json();

    // ⭐ UPDATE PAGE CONTENT
    answerText.innerText = data.answer || "No answer returned";
    confidence.innerText = data.confidence || "-";
    similarity.innerText = data.similarity_score || "-";
    source.innerText = (data.source_documents || []).join(", ");

  } catch (error) {
    console.error(error);
    answerText.innerText = "❌ Could not connect to backend.";
  }
}

function clearAll() {
  document.getElementById("questionInput").value = "";
  document.getElementById("resultBox").classList.add("hidden");
}
