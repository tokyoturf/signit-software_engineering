const video = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const predictionElement = document.getElementById("prediction");

// Access the webcam
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
    setInterval(captureFrame, 100); // Send frames every 100ms
  })
  .catch((err) => console.error("Webcam access denied:", err));

function captureFrame() {
  // Draw video frame to canvas
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Convert canvas to JPEG blob
  canvas.toBlob(sendFrameToServer, "image/jpeg", 0.8);
}

function sendFrameToServer(blob) {
  // Send frame to Flask backend
  const formData = new FormData();
  formData.append("frame", blob, "frame.jpg");

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      predictionElement.textContent = `Sign: ${data.sign}`;
    })
    .catch((err) => console.error("Prediction error:", err));
}
