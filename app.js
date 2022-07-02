const express = require("express");
const spawner = require("child_process").spawn;
const app = express();

app.get("/", (req,res) => {
    res.send("<h1>Selamlar</h1><br><h3>Kullanım: /words/{kelime}<\h3>");
});

app.get("/words/:word", (req,res) => {
    let word = encodeURIComponent(req.params.word.toString().trim().toLowerCase().replace(/[!'()/*-]/g,""));
    const chield = spawner("python3", ["./tureng-scraper/main.py", word.toString()]);
    chield.stdout.on('data', (data) => {
        res.send(data.toString());
        console.log(data.toString());
    });
});

app.listen(8080);
