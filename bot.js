// ===== 24/7 AWAKE ENDPOINT (keeps Render happy) =====
const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('OK'));
app.listen(process.env.PORT || 3000);
// =====================================================

const { Client, GatewayIntentBits } = require('discord.js');
const { HfInference } = require('@huggingface/inference');
const hf = new HfInference();   // FREE, no key needed

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => console.log(`${client.user.tag} ONLINE`));

client.on('messageCreate', async msg => {
  if (msg.author.bot || !msg.content.startsWith('?')) return;
  const prompt = msg.content.slice(1).trim();
  if (!prompt) return msg.reply('Type something after ?');

  const out = await hf.textGeneration({
    model: 'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5',
    inputs: `<|prompter|>${prompt}<|endoftext|><|assistant|>`,
    parameters: { max_new_tokens: 1200, temperature: 0.2 }
  });

  let text = out.generated_text;
  while (text.length) {
    const chunk = text.slice(0, 1900);
    text = text.slice(1900);
    await msg.channel.send('```lua\n' + chunk + '\n```');
  }
});

client.login(process.env.DISCORD_TOKEN);
  
