// import modules
const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

// mysql connection
const createConnection = () => {
    return mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_DATABASE,
    });
}

// Insert formData into MySQL user_data TABLE
const insertValuesIntoTable = (db, formData, callback) => {
    const selectQuery = `
        SELECT COUNT(*) AS count
        FROM user_data
        WHERE
        \`annual_income\` = ${formData["Annual Income"]}
        AND \`monthly_expense\` = ${formData["Monthly Expenditure"]}
        AND \`credit_score\` = ${formData["Credit Score"]}
        AND \`available_savings\` = ${formData["Available Savings"]}
        AND \`monthly_down_payment\` = ${formData["Monthly Down Payment"]};
        `;

    db.query(selectQuery, (selectError, results) => {
        if (selectError) {
            console.error('Error executing SELECT query frcom user_data table:', selectError);
            return;
        }

        const recordCount = results[0].count;

        // If the record doesn't exist, insert it
        if (recordCount === 0) {
            const insertQuery = `
                INSERT INTO user_data
                (\`annual_income\`, \`monthly_expense\`, \`credit_score\`, \`available_savings\`, \`monthly_down_payment\`)
                VALUES
                (${formData["Annual Income"]}, ${formData["Monthly Expenditure"]}, ${formData["Credit Score"]}, ${formData["Available Savings"]}, ${formData["Monthly Down Payment"]});
            `;

            db.query(insertQuery, (insertError) => {
                if (insertError) {
                    console.error('Error executing INSERT query:', insertError);
                } else {
                    console.log('Data inserted successfully into user_data table');
                }
                callback(false);
            });
        } else {
            console.log('Data already exists in user_data table');

            // Close the database connection
            db.end();
            callback(true);
        }
    })
};

// Calculate risk score and insert into user_risk_score table
const calculateRiskScore = (db, formData) => {
    // calculate risk score logic
    const risk_score = 0;

    // insert into table with correct user_id
    const selectQuery = `
        SELECT user_id
        FROM user_data
        WHERE
        \`annual_income\` = ${formData["Annual Income"]}
        AND \`monthly_expense\` = ${formData["Monthly Expenditure"]}
        AND \`credit_score\` = ${formData["Credit Score"]}
        AND \`available_savings\` = ${formData["Available Savings"]}
        AND \`monthly_down_payment\` = ${formData["Monthly Down Payment"]};
        `;

    db.query(selectQuery, (selectError, results) => {
        if (selectError) {
            console.error('Error executing SELECT query from user_data to calculate user_risk_score:', selectError);
            return;
        }

        const user_id = results[0].user_id;

        const insertQuery = `
            INSERT INTO user_risk_score
            (\`user_id\`, \`u_risk_score\`)
            VALUES
            (${user_id}, ${risk_score});
        `;

        db.query(insertQuery, (insertError) => {
            if (insertError) {
                console.error('Error executing INSERT query into user_risk_score table:', insertError);
            } else {
                console.log('Data inserted successfully into user_risk_score table');
            }
            // Close the database connection
            db.end();
            console.log('Database connection is closed after calculating risk score.');
        });
    });
};

// Put request to recieve data from frontend and insert into tables
app.put("/", (req, res) => {
    const formData = req.body;
    
    console.log('Received formData on the server', formData);
    res.send("Data received successfully!");

    // Create db connection
    const db = createConnection();

    // check if connection is successful
    db.connect((err) => {
        if (err) {
            console.error('Error connecting to MySQL:', err.message);
        } else {
            console.log('Connected to MySQL!');
        }
    });

    insertValuesIntoTable(db, formData, (isDisconnected) => {
        // Callback function after the data is inserted
        if (!isDisconnected) {
            calculateRiskScore(db, formData);
        } else {
            console.log('Database connection is closed. Cannot calculate risk score.');
        }
    });
});  

app.listen(process.env.PORT, () => {
    console.log("Listening...");
});

