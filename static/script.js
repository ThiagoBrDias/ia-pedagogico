// Navigation
function navigateTo(section) {
  // Update nav items
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active");
    if (item.dataset.section === section) {
      item.classList.add("active");
    }
  });

  // Update sections
  document.querySelectorAll(".content-section").forEach((sec) => {
    sec.classList.remove("active");
  });
  document.getElementById(section).classList.add("active");
}

// Event listeners for navigation
document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    navigateTo(item.dataset.section);
  });
});

// Utility Functions
function showLoading() {
  document.getElementById("loadingOverlay").classList.add("show");
}

function hideLoading() {
  document.getElementById("loadingOverlay").classList.remove("show");
}

function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast ${type} show`;
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

function copyToClipboard(elementId) {
  const element = document.querySelector(`#${elementId} .text-content`);
  const text = element.textContent;
  navigator.clipboard.writeText(text).then(() => {
    showToast("Texto copiado para a área de transferência!");
  });
}

// PDF Functions
async function extractTextFromPDF(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfExtractFile");
  const file = fileInput.files[0];

  // Verificar tamanho do arquivo
  const fileSizeMB = file.size / (1024 * 1024);
  if (fileSizeMB > 25) {
    showToast("Arquivo muito grande! Máximo 25MB", "error");
    hideLoading();
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    // Usar rota para arquivos grandes se for maior que 5MB
    const endpoint =
      fileSizeMB > 5 ? "/api/pdf/extract-text-large" : "/api/pdf/extract-text";

    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("extractedText");
      let textContent = data.text;

      // Se o texto foi dividido em chunks
      if (data.total_chunks && data.total_chunks > 1) {
        textContent += `\n\n[Texto dividido em ${data.total_chunks} partes. Mostrando primeira parte.]`;
      }

      resultBox.querySelector(".text-content").textContent = textContent;
      resultBox.style.display = "block";
      showToast("Texto extraído com sucesso!");
    } else {
      showToast("Erro ao extrair texto", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function mergePDFs(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfMergeFiles");
  const formData = new FormData();

  for (let file of fileInput.files) {
    formData.append("files", file);
  }

  try {
    const response = await fetch("/api/pdf/merge", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, "merged.pdf");
      showToast("PDFs mesclados com sucesso!");
    } else {
      showToast("Erro ao mesclar PDFs", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function splitPDF(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfSplitFile");
  const pages = document.getElementById("pdfPages").value;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("pages", pages);

  try {
    const response = await fetch("/api/pdf/split", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, "split.pdf");
      showToast("PDF dividido com sucesso!");
    } else {
      showToast("Erro ao dividir PDF", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function addWatermark(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfWatermarkFile");
  const watermarkText = document.getElementById("watermarkText").value;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("watermark_text", watermarkText);

  try {
    const response = await fetch("/api/pdf/add-watermark", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, "watermarked.pdf");
      showToast("Marca d'água adicionada com sucesso!");
    } else {
      showToast("Erro ao adicionar marca d'água", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

// Funções para arquivos grandes
async function splitLargePDF(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfLargeSplitFile");
  const pagesPerChunk = document.getElementById("pagesPerChunk").value;

  const file = fileInput.files[0];
  const fileSizeMB = file.size / (1024 * 1024);

  if (fileSizeMB > 25) {
    showToast("Arquivo muito grande! Máximo 25MB", "error");
    hideLoading();
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("pages_per_chunk", pagesPerChunk);

  try {
    const response = await fetch("/api/pdf/split-large", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, `split_${file.name}.zip`);
      showToast("PDF dividido com sucesso!");
    } else {
      const data = await response.json();
      showToast(data.detail || "Erro ao dividir PDF", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function compressPDF(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pdfCompressFile");
  const file = fileInput.files[0];

  const fileSizeMB = file.size / (1024 * 1024);
  if (fileSizeMB > 25) {
    showToast("Arquivo muito grande! Máximo 25MB", "error");
    hideLoading();
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/api/pdf/compress", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, `compressed_${file.name}`);
      showToast("PDF comprimido com sucesso!");
    } else {
      const data = await response.json();
      showToast(data.detail || "Erro ao comprimir PDF", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

// PPT Functions
function addSlideInput() {
  const container = document.getElementById("slidesContainer");
  const slideCount = container.children.length + 1;

  const slideDiv = document.createElement("div");
  slideDiv.className = "slide-input";
  slideDiv.innerHTML = `
        <input type="text" placeholder="Título do slide ${slideCount}" class="slide-title" required>
        <textarea placeholder="Conteúdo do slide ${slideCount}" class="slide-content" rows="3" required></textarea>
    `;

  container.appendChild(slideDiv);
}

async function createPresentation(event) {
  event.preventDefault();
  showLoading();

  const title = document.getElementById("pptTitle").value;
  const slideInputs = document.querySelectorAll(".slide-input");

  const slides = [];
  slideInputs.forEach((input) => {
    slides.push({
      title: input.querySelector(".slide-title").value,
      content: input.querySelector(".slide-content").value,
    });
  });

  const formData = new FormData();
  formData.append("title", title);
  formData.append("slides_content", JSON.stringify(slides));

  try {
    const response = await fetch("/api/ppt/create", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, `${title}.pptx`);
      showToast("Apresentação criada com sucesso!");
    } else {
      showToast("Erro ao criar apresentação", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function extractTextFromPPT(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pptExtractFile");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("/api/ppt/extract-text", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("extractedPPTText");
      let contentHTML = "";

      data.content.forEach((slide) => {
        contentHTML += `<div class="slide-info">
                    <h5>Slide ${slide.slide_number}: ${slide.title}</h5>
                    <ul>${slide.content
                      .map((c) => `<li>${c}</li>`)
                      .join("")}</ul>
                </div>`;
      });

      resultBox.querySelector(".text-content").innerHTML = contentHTML;
      resultBox.style.display = "block";
      showToast("Texto extraído com sucesso!");
    } else {
      showToast("Erro ao extrair texto", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function addSlideToPPT(event) {
  event.preventDefault();
  showLoading();

  const fileInput = document.getElementById("pptAddSlideFile");
  const slideTitle = document.getElementById("newSlideTitle").value;
  const slideContent = document.getElementById("newSlideContent").value;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("slide_title", slideTitle);
  formData.append("slide_content", slideContent);

  try {
    const response = await fetch("/api/ppt/add-slide", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      downloadFile(blob, "updated.pptx");
      showToast("Slide adicionado com sucesso!");
    } else {
      showToast("Erro ao adicionar slide", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

// AI Functions
async function improveText(event) {
  event.preventDefault();
  showLoading();

  const text = document.getElementById("textToImprove").value;
  const context = document.getElementById("improveContext").value;

  const formData = new FormData();
  formData.append("text", text);
  formData.append("context", context);

  try {
    const response = await fetch("/api/ai/improve-text", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("improvedText");
      resultBox.querySelector(".text-content").textContent = data.improved_text;
      resultBox.style.display = "block";
      showToast("Texto melhorado com sucesso!");
    } else {
      showToast("Erro ao melhorar texto", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function summarizeText(event) {
  event.preventDefault();
  showLoading();

  const text = document.getElementById("textToSummarize").value;
  const maxWords = document.getElementById("maxWords").value;

  const formData = new FormData();
  formData.append("text", text);
  formData.append("max_words", maxWords);

  try {
    const response = await fetch("/api/ai/summarize", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("summarizedText");
      resultBox.querySelector(".text-content").textContent = data.summary;
      resultBox.style.display = "block";
      showToast("Texto resumido com sucesso!");
    } else {
      showToast("Erro ao resumir texto", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function generateQuestions(event) {
  event.preventDefault();
  showLoading();

  const text = document.getElementById("textForQuestions").value;
  const numQuestions = document.getElementById("numQuestions").value;
  const difficulty = document.getElementById("questionDifficulty").value;

  const formData = new FormData();
  formData.append("text", text);
  formData.append("num_questions", numQuestions);
  formData.append("difficulty", difficulty);

  try {
    const response = await fetch("/api/ai/generate-questions", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("generatedQuestions");
      let questionsHTML = "";

      data.questions.forEach((q, index) => {
        questionsHTML += `
                    <div class="question-item">
                        <h5>Questão ${index + 1}: ${q.question}</h5>
                        <div class="alternatives">
                            ${Object.entries(q.alternatives)
                              .map(
                                ([key, value]) =>
                                  `<div><strong>${key})</strong> ${value}</div>`
                              )
                              .join("")}
                        </div>
                        <div class="correct-answer">Resposta correta: ${
                          q.correct_answer
                        }</div>
                        <div class="explanation">${q.explanation}</div>
                    </div>
                `;
      });

      resultBox.querySelector(".text-content").innerHTML = questionsHTML;
      resultBox.style.display = "block";
      showToast("Questões geradas com sucesso!");
    } else {
      showToast("Erro ao gerar questões", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function translateText(event) {
  event.preventDefault();
  showLoading();

  const text = document.getElementById("textToTranslate").value;
  const targetLanguage = document.getElementById("targetLanguage").value;

  const formData = new FormData();
  formData.append("text", text);
  formData.append("target_language", targetLanguage);

  try {
    const response = await fetch("/api/ai/translate", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("translatedText");
      resultBox.querySelector(".text-content").textContent = data.translation;
      resultBox.style.display = "block";
      showToast("Texto traduzido com sucesso!");
    } else {
      showToast("Erro ao traduzir texto", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

// Content Generator Functions
async function generateLessonPlan(event) {
  event.preventDefault();
  showLoading();

  const subject = document.getElementById("lessonSubject").value;
  const grade = document.getElementById("lessonGrade").value;
  const topic = document.getElementById("lessonTopic").value;
  const duration = document.getElementById("lessonDuration").value;

  const formData = new FormData();
  formData.append("subject", subject);
  formData.append("grade", grade);
  formData.append("topic", topic);
  formData.append("duration", duration);

  try {
    const response = await fetch("/api/content/lesson-plan", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const lessonPlan = data.lesson_plan;
      const resultBox = document.getElementById("generatedLessonPlan");

      let html = `
                <div class="lesson-section">
                    <h4>${lessonPlan.title}</h4>
                </div>
                <div class="lesson-section">
                    <h5>Objetivos:</h5>
                    <ul>${lessonPlan.objectives
                      .map((obj) => `<li>${obj}</li>`)
                      .join("")}</ul>
                </div>
                <div class="lesson-section">
                    <h5>Conteúdos:</h5>
                    <p>${lessonPlan.content}</p>
                </div>
                <div class="lesson-section">
                    <h5>Metodologia:</h5>
                    <p>${lessonPlan.methodology}</p>
                </div>
                <div class="lesson-section">
                    <h5>Recursos:</h5>
                    <ul>${lessonPlan.resources
                      .map((res) => `<li>${res}</li>`)
                      .join("")}</ul>
                </div>
                <div class="lesson-section">
                    <h5>Desenvolvimento:</h5>
                    ${lessonPlan.development
                      .map(
                        (dev) => `
                        <div style="margin-bottom: 1rem;">
                            <strong>${dev.step}</strong> (${dev.duration})<br>
                            ${dev.description}
                        </div>
                    `
                      )
                      .join("")}
                </div>
                <div class="lesson-section">
                    <h5>Avaliação:</h5>
                    <p>${lessonPlan.assessment}</p>
                </div>
                <div class="lesson-section">
                    <h5>Referências:</h5>
                    <ul>${lessonPlan.references
                      .map((ref) => `<li>${ref}</li>`)
                      .join("")}</ul>
                </div>
            `;

      resultBox.querySelector(".text-content").innerHTML = html;
      resultBox.style.display = "block";
      showToast("Plano de aula gerado com sucesso!");
    } else {
      showToast("Erro ao gerar plano de aula", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function generateExercises(event) {
  event.preventDefault();
  showLoading();

  const subject = document.getElementById("exerciseSubject").value;
  const topic = document.getElementById("exerciseTopic").value;
  const numExercises = document.getElementById("numExercises").value;
  const difficulty = document.getElementById("exerciseDifficulty").value;

  const formData = new FormData();
  formData.append("subject", subject);
  formData.append("topic", topic);
  formData.append("num_exercises", numExercises);
  formData.append("difficulty", difficulty);

  try {
    const response = await fetch("/api/content/exercise-list", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("generatedExercises");
      let html = "";

      data.exercises.forEach((ex) => {
        html += `
                    <div class="question-item">
                        <h5>Exercício ${ex.number} (${ex.type})</h5>
                        <p><strong>${ex.question}</strong></p>
                `;

        if (ex.alternatives) {
          html += `<div class="alternatives">`;
          Object.entries(ex.alternatives).forEach(([key, value]) => {
            html += `<div><strong>${key})</strong> ${value}</div>`;
          });
          html += `</div>`;
        }

        html += `
                        <div class="correct-answer">Resposta: ${ex.answer}</div>
                        ${
                          ex.explanation
                            ? `<div class="explanation">${ex.explanation}</div>`
                            : ""
                        }
                    </div>
                `;
      });

      resultBox.querySelector(".text-content").innerHTML = html;
      resultBox.style.display = "block";
      showToast("Exercícios gerados com sucesso!");
    } else {
      showToast("Erro ao gerar exercícios", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

async function generatePresentationOutline(event) {
  event.preventDefault();
  showLoading();

  const topic = document.getElementById("presentationTopic").value;
  const numSlides = document.getElementById("presentationSlides").value;
  const audience = document.getElementById("presentationAudience").value;

  const formData = new FormData();
  formData.append("topic", topic);
  formData.append("num_slides", numSlides);
  formData.append("audience", audience);

  try {
    const response = await fetch("/api/content/presentation-outline", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      const resultBox = document.getElementById("generatedOutline");
      let html = "";

      data.outline.forEach((slide) => {
        html += `
                    <div class="lesson-section">
                        <h5>Slide ${slide.slide_number}: ${slide.title}</h5>
                        <ul>${slide.content
                          .map((c) => `<li>${c}</li>`)
                          .join("")}</ul>
                        <p style="font-style: italic; color: #6b7280; margin-top: 0.5rem;">
                            💡 ${slide.visual_suggestions}
                        </p>
                    </div>
                `;
      });

      resultBox.querySelector(".text-content").innerHTML = html;
      resultBox.style.display = "block";
      showToast("Estrutura de apresentação gerada com sucesso!");
    } else {
      showToast("Erro ao gerar estrutura", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}

// Utility Functions
function downloadFile(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

async function checkHealth() {
  showLoading();
  try {
    const response = await fetch("/api/health");
    const data = await response.json();

    let message = `Status: ${data.status}\n`;
    message += `OpenAI: ${
      data.openai_configured ? "✓ Configurado" : "✗ Não configurado"
    }\n`;
    message += `Anthropic: ${
      data.anthropic_configured ? "✓ Configurado" : "✗ Não configurado"
    }`;

    alert(message);
  } catch (error) {
    showToast("Erro ao verificar status", "error");
  } finally {
    hideLoading();
  }
}

async function cleanupFiles() {
  if (!confirm("Deseja realmente limpar todos os arquivos temporários?")) {
    return;
  }

  showLoading();
  try {
    const response = await fetch("/api/cleanup", {
      method: "DELETE",
    });

    const data = await response.json();

    if (data.success) {
      showToast("Arquivos temporários removidos!");
    } else {
      showToast("Erro ao limpar arquivos", "error");
    }
  } catch (error) {
    showToast("Erro: " + error.message, "error");
  } finally {
    hideLoading();
  }
}
