const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', () => console.log(`${client.user.tag} ONLINE`));

// ===== UNLIMITED COLAB API =====
async function coder13(prompt) {
  const res = await fetch("https://mollifyingly-unepigrammatic-jannette.ngrok-free.dev/v1/chat/completions", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: [{role: 'user', content: prompt}],
      max_tokens: 1200,
      temperature: 0.2
    })
  });
  if (!res.ok) throw new Error('Network error ' + res.status);
  const json = await res.json();
  return json.choices[0].message.content;
}
// ===============================

client.on('messageCreate', async msg => {
  if (msg.author.bot || !msg.content.startsWith('?')) return;
  const prompt = msg.content.slice(1).trim();
  if (!prompt) return;
  try {
    const text = await coder13(prompt);
    for (const chunk of [text]) await msg.channel.send('```lua\n' + chunk + '\n```');
  } catch (e) {
    await msg.channel.send('⚠️ ' + e.message);
  }
});

client.login(process.env.DISCORD_TOKEN);
      
