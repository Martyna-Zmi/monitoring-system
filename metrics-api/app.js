const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const PORT = 8080;

const db = new sqlite3.Database('/db/metrics.db');

app.get('/metrics', (req, res) => {
    db.all('SELECT ROUND(avg(avg_cpu), 2) as avg_cpu, ROUND(avg(avg_ram), 2) as avg_ram, ROUND(avg(avg_disk), 2) as avg_disk FROM metrics', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows[0]);
    });
});

app.listen(PORT, () => {
    console.log(`Metrics API running on port ${PORT}`);
});
