class Detect {
  constructor({ url, element }) {
    this.url = url;
    this.element = element;
    this.video = document.createElement('video');
    this.canvas = document.createElement('canvas');
    this.canvasCtx = this.canvas.getContext('2d');
    this.boxes = document.createElement('canvas');
    this.boxesCtx = this.boxes.getContext('2d');
    this.colors = {};

    this.element.appendChild(this.video);
    this.element.appendChild(this.boxes);

    this.video.addEventListener('canplay', () => {
      this.canvas.width = this.video.videoWidth;
      this.canvas.height = this.video.videoHeight;
      this.boxes.width = this.video.videoWidth;
      this.boxes.height = this.video.videoHeight;
      this.grabFrame();
    });

    this.playVideo();
  }

  playVideo() {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        this.video.srcObject = stream;
        this.video.play();
      });
  }

  drawBoxes(results) {
    this.boxesCtx.clearRect(0, 0, this.boxes.width, this.boxes.height);

    results.forEach((result) => {
      this.drawBox(result);
    });
  }

  drawBox({ box, label, score }) {
    const x = box.left * this.boxes.width;
    const y = box.top * this.boxes.height;
    const height = (box.bottom * this.boxes.height) - y;
    const width = (box.right * this.boxes.width) - x;
    const percentage = Math.round(score * 100);

    if (!this.colors[label]) {
      this.colors[label] = '#' + ((1<<24)*Math.random()|0).toString(16);
    }

    this.boxesCtx.strokeStyle = this.colors[label];
    this.boxesCtx.fillStyle = this.colors[label];
    this.boxesCtx.font = '14px Arial';
    this.boxesCtx.lineWidth = 4;
    this.boxesCtx.strokeRect(x, y, width, height);
    this.boxesCtx.fillText(`${label}: ${percentage}%`, x + 10, y + 20);
  }

  grabFrame() {
    this.canvasCtx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
    this.canvas.toBlob((imageData) => {
      const form = new FormData();
      form.append('image', imageData);

      this.time = new Date().getTime();

      fetch(this.url, {
        method: 'POST',
        body: form,
      })
        .then(response => response.json())
        .then((results) => {
          const delta = new Date().getTime() - this.time;

          this.drawBoxes(results);
          
          setTimeout(() => {
            this.grabFrame();
          }, 1000 - delta);
        });

    }, 'image/jpeg', 70);
  }
}
