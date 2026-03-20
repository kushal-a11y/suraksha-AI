import express from 'express'
import cors from 'cors'
import { analyze } from './API_Logic.js'

const app = express()
app.use(cors())
app.use(express.json())

app.post('/analyze', async (req, res)=>{
    try{
        const { text } = req.body;
        const response = await analyze(text);
        res.json({ result: response });
    }catch(err){
        console.error("FULL ERROR:", err); 
        res.status(500).json({error: 'Something went wrong'});
    }
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000")
})