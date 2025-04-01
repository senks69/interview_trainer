<template>
  <div class="interview-container">
    <!-- Основное видео собеседника -->
    <div class="main-video">
      <video ref="remoteVideo">
        <source :src="videoSource" type="video/mp4" />
      </video>
    </div>

    <!-- Ваше видео с индикацией звука -->
    <div class="local-video">
      <video ref="localVideo" autoplay muted></video>
      <div class="volume-indicator" :class="indicatorClass"></div>
      <div class="user-info">
        <span class="user-name">Вы</span>
        <span class="user-status">{{ statusText }}</span>
      </div>
    </div>

    <!-- Уведомления -->
    <div class="notifications-container">
      <transition-group name="notification">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
        >
          {{ notification.userName }} присоединился
        </div>
      </transition-group>
    </div>

    <!-- Аватарки участников -->
    <div class="participants-container">
      <div
        v-for="participant in participants"
        :key="participant.id"
        class="avatar-wrapper"
      >
        <img :src="participant.avatar" :alt="participant.name" class="avatar" />
      </div>
    </div>

    <!-- Панель управления -->
    <div class="control-panel">
      <button @click="toggleMic" :class="{ active: !micMuted }">
        <img src="./../assets/zvuk.png" alt="" />
      </button>
      <button @click="toggleCamera" :class="{ active: !cameraOff }">
        <img src="./../assets/video.png" alt="" />
      </button>
      <button @click="endInterview" class="end-call">
        <img src="./../assets/stop.png" alt="" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "InterviewPage",
  data() {
    return {
      micMuted: false,
      cameraOff: false,
      isSpeaking: false,
      audioContext: null,
      analyser: null,
      animationId: null,
      volumeLevel: 0,
      lastSoundTime: 0,
      speakingTimeout: null,
      videoSource: require("../../data/481107642927.mp4"),
      participants: [
        {
          id: 1,
          name: "Иван Ежов",
          speaking: false,
          avatar: require("../../data/1.jpg"),
        },
        {
          id: 2,
          name: "Арсений Ильин",
          speaking: false,
          avatar: require("../../data/2.jpg"),
        },
        {
          id: 3,
          name: "Даниил Крупнов",
          speaking: false,
          avatar: require("../../data/3.jpg"),
        },
      ],
      localStream: null,
      notifications: [],
      nextNotificationId: 1,
    };
  },
  computed: {
    indicatorClass() {
      if (this.micMuted) return "muted";
      return this.isSpeaking ? "speaking" : "silent";
    },
    statusText() {
      if (this.micMuted) return "Микрофон выключен";
      return this.isSpeaking ? "Говорите!" : "Молчите!";
    },
  },
  methods: {
    async startVideo() {
      try {
        this.localStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });
        this.$refs.localVideo.srcObject = this.localStream;
        this.setupAudioAnalysis();

        // this.ws = new WebSocket("ws://localhost:8000/ws");

        // this.ws.onopen = () => {
        //   console.log("WebSocket подключен");
        //   this.sendFrames();
        // };

        // this.ws.onmessage = (event) => {
        //   console.log("Распознанная эмоция:", event.data);
        // };

        // this.ws.onclose = () => console.log("WebSocket закрыт");
        // Запускаем ваше видео файлом
        this.$refs.remoteVideo
          .play()
          .catch((e) => console.error("Ошибка воспроизведения:", e));
      } catch (error) {
        console.error("Ошибка доступа к медиаустройствам:", error);
        alert("Не удалось получить доступ к камере/микрофону");
      }
    },
    showNotification(userName) {
      const id = this.nextNotificationId++;
      this.notifications.push({ id, userName });
      setTimeout(() => {
        this.removeNotification(id);
      }, 3000);
    },
    removeNotification(id) {
      this.notifications = this.notifications.filter((n) => n.id !== id);
    },
    sendFrames() {
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");
      const video = this.$refs.localVideo;

      const send = () => {
        if (this.ws.readyState !== WebSocket.OPEN) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
          blob.arrayBuffer().then((buffer) => {
            this.ws.send(buffer);
          });
        }, "image/jpeg");

        setTimeout(send, 100); // Отправляем кадры каждые 100 мс
      };

      send();
    },
    setupAudioAnalysis() {
      try {
        this.audioContext = new (window.AudioContext ||
          window.webkitAudioContext)();
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;

        const audioSource = this.audioContext.createMediaStreamSource(
          this.localStream
        );
        audioSource.connect(this.analyser);
        this.detectSound();
      } catch (error) {
        console.error("Ошибка анализа аудио:", error);
      }
    },
    detectSound() {
      const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
      this.analyser.getByteFrequencyData(dataArray);

      let sum = 0;
      for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
      }
      this.volumeLevel = sum / dataArray.length;

      const SPEAKING_THRESHOLD = 50;
      const SILENCE_DELAY = 1000;

      if (this.volumeLevel > SPEAKING_THRESHOLD && !this.micMuted) {
        this.isSpeaking = true;
        this.lastSoundTime = Date.now();
        this.participants[0].speaking = true;
        clearTimeout(this.speakingTimeout);
      } else if (Date.now() - this.lastSoundTime > SILENCE_DELAY) {
        this.isSpeaking = false;
        this.participants[0].speaking = false;
      }

      this.animationId = requestAnimationFrame(this.detectSound);
    },
    toggleMic() {
      this.micMuted = !this.micMuted;
      if (this.localStream) {
        this.localStream.getAudioTracks().forEach((track) => {
          track.enabled = !this.micMuted;
        });
      }
      if (this.micMuted) {
        this.isSpeaking = false;
        this.participants[0].speaking = false;
      }
    },
    toggleCamera() {
      this.cameraOff = !this.cameraOff;
      if (this.localStream) {
        this.localStream.getVideoTracks().forEach((track) => {
          track.enabled = !this.cameraOff;
        });
      }
    },
    endInterview() {
      if (confirm("Вы уверены, что хотите завершить собеседование?")) {
        if (this.localStream) {
          this.localStream.getTracks().forEach((track) => track.stop());
        }
        this.$router.push("/feedback");
      }
    },
  },
  mounted() {
    this.startVideo();
    this.showNotification("Иван Ежов");
  },
  beforeUnmount() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
    if (this.localStream) {
      this.localStream.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>

<style scoped>
.interview-container {
  height: 100vh;
  background-color: #c0c0c0;
  color: white;
  font-family: "SF Compact Display", sans-serif;
  position: relative;
}

.main-video {
  width: 100%;
}

.main-video video {
  width: 100%;
  height: 100vh;
}

.local-video {
  position: absolute;
  bottom: 100px;
  right: 20px;
  width: 200px;
  height: 120px;
  overflow: hidden;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  border-top: 1px solid #ffffff;
  border-left: 1px solid #ffffff;
}

.local-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.volume-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  transition: all 0.3s ease;
}

.volume-indicator.speaking {
  background: linear-gradient(90deg, #ff5722, #f44336);
  box-shadow: 0 0 10px rgba(244, 67, 54, 0.7);
  animation: pulse 1.5s infinite;
}

.volume-indicator.silent {
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
}

.volume-indicator.muted {
  background: #607d8b;
}

.user-info {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.7);
  padding: 5px 10px;
  font-size: 12px;
  line-height: 1.4;
  max-width: calc(100% - 20px);
}

.user-name {
  display: block;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-status {
  display: block;
  font-size: 0.8em;
}

.volume-indicator.silent ~ .user-info .user-status {
  color: #8bc34a;
}

.volume-indicator.speaking ~ .user-info .user-status {
  color: #ff9800;
  font-weight: bold;
}

.volume-indicator.muted ~ .user-info .user-status {
  color: #b0bec5;
}

.control-panel {
  position: absolute;
  bottom: 100px;
  left: 45%;
}

.control-panel button {
  margin: 0 5px;
}

.control-panel button.active {
  background: #42b983;
}

.control-panel button.end-call {
  background: #e74c3c;
}

.control-panel button.end-call:hover {
  background: #c0392b;
}

.participants-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background-color: #ccc;
  padding: 10px;
  border-radius: 8px;
  display: flex;
  gap: 10px;
}

.avatar-wrapper {
  width: 50px;
  height: 50px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.notifications-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.notification {
  padding: 12px 20px;
  background-color: #4caf50;
  color: white;
  border-radius: 4px;
  margin-bottom: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease-out;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.5s;
}

.notification-enter,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

@keyframes pulse {
  0% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
  100% {
    opacity: 0.7;
    transform: scale(1);
  }
}

@keyframes slideIn {
  from {
    transform: translateX(100px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
