// ===== UNLIMITED COLAB API =====
async function coder13(prompt) {
  const res = await fetch("https://mollifyingly-unepigrammatic-jannette.ngrok-free.dev/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages: [{role: "user", content: prompt}],
      max_tokens: 1200,
      temperature: 0.2
    })
  });
  const json = await res.json();
  return json.choices[0].message.content;
}
// ===============================
