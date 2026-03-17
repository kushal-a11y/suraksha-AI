import 'openai'
import * as dotenv from 'dotenv'
import OpenAI from 'openai';

dotenv.config();

const client = new OpenAI({
    apiKey: process.env.ASI_ONE_API_KEY,
    baseURL: 'https://api.asi1.ai/v1',
})

const brain_of_AI = `
You are a cybersecurity expert focused on protecting Indian users from online fraud.

Analyze every message step by step and respond in the following structured format:

1. Scam Detection: (Yes/No)
2. Scam Type: (Phishing / Impersonation / Job Scam / OTP Fraud / Other)
3. Risk Level: (Low / Medium / High)
4. Explanation: Explain clearly why this is a scam in simple language.
5. Recommended Action: Give clear steps the user should take.

Keep your answers concise, practical, and easy to understand.
`;



const messages = [
  'Your bank account will be blocked. Share your OTP immediately to verify.',
  'Hey, I lost my phone. This is my new number. Can you send me ₹3000 urgently?',
  'You got selected for a job at Amazon. Pay ₹1500 for document verification.'
]

export const analyze = async (text)=>{
    const response = await client.chat.completions.create({
        model: 'asi1',
        messages: [
            {role: 'system', content: brain_of_AI},
            {role: 'user', content: text}
        ]
    })
    return response.choices[0].message.content;
}

// const response = await client.chat.completions.create({
//   model: 'asi1',
//   messages: [//{ role: 'user', content: 'Hello! How can you help me today?' }, 
//     //{ role: 'user', content: 'Hello! Why is there a hostility bw iran and US' },
//     { role: 'system', content:  brain_of_AI},
//     // { role: 'user', content:  'Your bank account will be blocked. Share your OTP immediately to verify.'},//- OTP scam
//     // { role: 'user', content:  'Hey, I lost my phone. This is my new number. Can you send me ₹3000 urgently?'},
//     { role: 'user', content:  'You got selected for a job at Amazon. Pay ₹1500 for document verification.'}],
// });

//Running Multiple messgaes - one by one

// console.log(process.env.ASI_ONE_API_KEY);\

// for (const msg of messages){
//     const response = await client.chat.completions.create({
//         model: 'asi1',
//         messages: [
//             {role: 'system', content: brain_of_AI},
//             {role: 'user', content: msg}
//         ]
//     })
//     console.log("INPUT:", msg);
//     console.log("OUTPUT:", response.choices[0].message.content);
//     console.log("-----------");
// }

// console.log(response.choices[0].message.content)