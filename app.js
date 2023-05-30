require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const cors = require("cors");
const multer = require("multer");
const sharp = require("sharp");
const fs = require("fs");
const upload = multer({ dest: "uploads/" });
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(
  cors({
    origin: ["http://localhost:3000"],
    methods: ["GET", "POST"],
  })
);
app.use(express.json());
app.use(express.static("public"));
const port = process.env.PORT || 3001;

app.post("/color", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/color.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/colored/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/colored/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/rcrop", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/rcrop.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/rcrop/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/rcrop/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/ccrop", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/ccrop.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/ccrop/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/ccrop/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/resize", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/resize.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
    "-a",
    req.body.w,
    "-b",
    req.body.h,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/resize/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/resize/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/compress", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/compress.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
    "-a",
    req.body.size,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/compress/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/compress/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/blur", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/blur.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python script output: ${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
    res.sendFile(__dirname + `/public/blur/${req.file.filename}.jpg`);
    setTimeout(() => {
      fs.unlinkSync(`./public/blur/${req.file.filename}.jpg`);
    }, 1000);
  });
});

app.post("/pick", upload.single("file"), async (req, res) => {
  const image = sharp(req.file.path);
  const jpegImage = image.jpeg({ quality: 100 });
  const jpegFilePath = `uploads/${req.file.filename}.jpg`;
  await jpegImage.toFile(jpegFilePath);
  var filePath = `./uploads/${req.file.filename}`;
  var path = `./uploads/${req.file.filename}.jpg`;
  fs.unlinkSync(filePath);
  const pythonProcess = spawn("python", [
    "./python_scripts/pick.py",
    "-i",
    `uploads/${req.file.filename}.jpg`,
    "-s",
    req.file.filename,
  ]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(`${data}`);
    res.send(`${data}`);
  });
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error from Python script: ${data}`);
  });
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    fs.unlinkSync(path);
  });
});

app.listen(port, () => {
  console.log("Server started on port 3001");
});
