const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
});

db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err.message);
    } else {
        console.log('Connected to MySQL!');
    }
});

app.put("/", (req, res) => {
    const formData = req.body;
    
    console.log('Received formData on the server', formData);
    // Process the formData and send a response if needed


    res.send("Data received successfully!");
});  

app.listen(process.env.PORT, () => {
    console.log("Listening...");
});