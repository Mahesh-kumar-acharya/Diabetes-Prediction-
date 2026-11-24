/* Diabetes Risk Assessment — form handling */
(function () {
  "use strict";

  const form = document.getElementById("risk-form");
  const result = document.getElementById("result");
  const verdict = document.getElementById("result-verdict");
  const probability = document.getElementById("result-probability");
  const classification = document.getElementById("result-class");
  const resultKicker = document.getElementById("result-kicker");
  const submitBtn = document.getElementById("submit-btn");
  const resetBtn = document.getElementById("reset-btn");

  // Toggle switches: checkbox + visible word
  document.querySelectorAll(".field--toggle").forEach((field) => {
    const box = field.querySelector('input[type="checkbox"]');
    const text = field.querySelector(".toggle-text");
    box.addEventListener("change", () => {
      text.textContent = box.checked ? "Yes" : "No";
    });
  });

  function readForm() {
    return {
      gender: document.getElementById("gender").value,
      age: document.getElementById("age").value,
      smoking: document.getElementById("smoking").value,
      hypertension: document.getElementById("hypertension").checked ? 1 : 0,
      heart_disease: document.getElementById("heart_disease").checked ? 1 : 0,
      bmi: document.getElementById("bmi").value,
      hba1c: document.getElementById("hba1c").value,
      glucose: document.getElementById("glucose").value,
    };
  }

  function markInvalid(message) {
    let firstBad = null;
    form.querySelectorAll('input[type="number"]').forEach((input) => {
      const bad = input.value === "" || isNaN(parseFloat(input.value));
      input.classList.toggle("invalid", bad);
      if (bad && !firstBad) firstBad = input;
    });
    if (firstBad) firstBad.focus();
    showResult(message || "Incomplete entry", null, true);
  }

  function showResult(text, probabilityText, isError) {
    verdict.textContent = text;
    verdict.classList.toggle("is-diabetic", !isError && text === "Diabetic");
    probability.textContent = probabilityText || "—";
    classification.textContent = isError
      ? "—"
      : text === "Diabetic"
        ? "Class 1"
        : "Class 0";
    resultKicker.textContent = isError ? "Hold on" : "Result";
    result.classList.remove("hidden");
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = readForm();

    if (!data.age || !data.bmi || !data.hba1c || !data.glucose) {
      markInvalid("Incomplete entry");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Assessing…";

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const payload = await response.json();

      if (!response.ok) {
        showResult(payload.error || "Something went wrong", null, true);
      } else {
        const pct = (payload.probability * 100).toFixed(1) + "%";
        showResult(payload.prediction, pct, false);
        resetBtn.classList.remove("hidden");
      }
    } catch (err) {
      showResult("Could not reach the model", null, true);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Assess risk";
    }
  });

  resetBtn.addEventListener("click", () => {
    form.reset();
    document.querySelectorAll(".toggle-text").forEach((t) => {
      t.textContent = "No";
    });
    form.querySelectorAll('input[type="number"]').forEach((i) => {
      i.classList.remove("invalid");
    });
    result.classList.add("hidden");
    resetBtn.classList.add("hidden");
    document.getElementById("age").focus();
  });
})();
