const express = require("express");
const spawner = require("child_process").spawn;
const fs = require("fs");

const app = express();

app.get("/", (req,res) => {
    res.send("<h1>Selamlar</h1><br><h3>Kullanım: /words/{kelime}<\h3>");
});

app.get("/words/:word", (req,res) => {
    let word = req.params.word.toString().trim().toLowerCase();
    let path = "./words/" + word + ".json"
    if (fs.existsSync(path)) {
        console.log("Existing word: "+word);
        fs.readFile(path, "utf-8", (err, data) => {
            res.send(data);
        });
    }
    else {
        console.log("New word added to ./words: "+word);
        const chield = spawner("python3", ["./tureng-scraper/main.py", word.toString()]);
        chield.addListener("close", () => {
            fs.readFile(path, "utf-8", (err, data) => {
                res.send(data);
            });
        });
    }
});

app.listen(8080);