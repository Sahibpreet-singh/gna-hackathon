const express = require("express");
const { PythonShell } = require("python-shell");
const { exec } = require("child_process"); 
const mongoose = require("mongoose");
const path = require("path");

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.json());

const Log = require("./models/Log");

mongoose.connect("mongodb://127.0.0.1:27017/firewall_logs", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});



app.get("/dashboard", async (req, res) => {
  try {
    const logs = await Log.find().sort({ timestamp: -1 }).limit(50);
    res.render("dashboard", { logs });
  } catch (error) {
    console.error("Error fetching logs:", error);
    res.status(500).send("Failed to load dashboard");
  }
});


app.post("/predict", async (req, res) => {
  const { ip, app, packet_size, request_frequency, port } = req.body;

  let options = {
    mode: "json",
    pythonPath: "python",
    scriptPath: "./",
    args: [packet_size, request_frequency, port],
  };

  PythonShell.run("predict.py", options)
    .then(async (results) => {
      const prediction = results[0].prediction; // 1 = block, 0 = allow

      const logEntry = new Log({
        ip: ip,
        app: app || "Unknown", // ✅ Now correctly accessing req.body.app
        decision: prediction === "1" ? "block" : "allow",
        reason: prediction === "1" ? "Suspicious traffic detected" : "Normal traffic",
      });

      await logEntry.save();

      if (prediction === "1") {
        return res.json({ message: "Traffic blocked", decision: "block", ip, app });
      } else {
        return res.json({ message: "Traffic allowed", decision: "allow", ip, app });
      }
    })
    .catch((err) => {
      console.error("Python Error:", err);
      res.status(500).json({ error: "Internal Server Error" });
    });
});



app.post("/log", async (req, res) => {
  const { ip, decision, reason } = req.body;

  if (!ip || !decision) {
    return res.status(400).json({ error: "Missing parameters" });
  }

  try {
    const logEntry = new Log({ ip, decision, reason: reason || "No reason provided" });
    await logEntry.save();

    console.log(`📝 Log saved: ${ip} -> ${decision}`);
    res.json({ message: "Log received", ip, decision });
  } catch (err) {
    console.error("❌ Error saving log:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});


app.get("/logs", async (req, res) => {
  try {
    const logs = await Log.find().sort({ timestamp: -1 }).limit(50);
    res.json(logs);
  } catch (error) {
    console.error("Error fetching logs:", error);
    res.status(500).json({ error: "Failed to retrieve logs" });
  }
});


app.listen(5000, () => {
  console.log("Server running on http://127.0.0.1:5000");
});
