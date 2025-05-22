async function invia() {
  const testo = document.getElementById("input").value;

  const response = await fetch("/api/riassunto", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(testo)
  });

  const risultato = await response.text();  // prende il testo raw

  // Rimuovi i tag <think>...</think> con regex multilinea
  const cleaned = risultato.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();

  // Aggiorna il DOM con il testo pulito
  document.getElementById("risultato").innerText = cleaned;
}

// Esempio fetch diverso: ti serve userInput definito, e usa text non json?
// Se la risposta è JSON, tieni così, altrimenti se è testo cambia in text()
fetch('/ai', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ prompt: userInput }),
})
.then(response => response.json()) // se la risposta è JSON
.then(data => {
  // Anche qui rimuovi eventuali tag <think>
  const cleanedResponse = data.response.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();
  const responseBox = document.getElementById('response-box');
  responseBox.innerText = cleanedResponse; // Mostra il testo pulito
});

// Regola altezza textarea
const textarea = document.getElementById('prompt-input');
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
});
