<template>
  <div class="interview-container">
    <!-- Основное видео (собеседник) -->
    <div class="main-video">
      <video ref="remoteVideo" autoplay playsinline></video>
      <div class="user-info">
        <span class="user-name">Собеседник</span>
        <span class="user-status">В сети</span>
      </div>
    </div>

    <!-- Ваше видео (превью) с индикацией звука -->
    <div class="local-video" :class="{ speaking: isSpeaking }">
      <video ref="localVideo" autoplay playsinline muted></video>
      <div class="volume-indicator"></div>
      <div class="user-info">
        <span class="user-name">Вы</span>
        <span class="user-status">{{
          micMuted ? "Микрофон выключен" : "Говорите..."
        }}</span>
      </div>
    </div>

    <!-- Панель управления -->
    <div class="control-panel">
      <button @click="toggleMic" :class="{ active: !micMuted }">
        <i class="icon-mic"></i>
        {{ micMuted ? "Вкл. микрофон" : "Выкл. микрофон" }}
      </button>
      <button @click="toggleCamera" :class="{ active: !cameraOff }">
        <i class="icon-camera"></i>
        {{ cameraOff ? "Вкл. камеру" : "Выкл. камеру" }}
      </button>
      <button @click="endInterview" class="end-call">
        <i class="icon-phone"></i>
        Завершить
      </button>
    </div>

    <!-- Боковая панель с чатом -->
    <div class="sidebar">
      <div class="chat-container">
        <div class="chat-messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="{ 'own-message': message.sender === 'Вы' }"
          >
            <strong>{{ message.sender }}:</strong> {{ message.text }}
          </div>
        </div>
        <div class="chat-input">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="Введите сообщение..."
            :disabled="micMuted"
          />
          <button
            @click="sendMessage"
            :disabled="micMuted || !newMessage.trim()"
          >
            <i class="icon-send"></i>
          </button>
        </div>
      </div>

      <div class="participants">
        <h3>Участники ({{ participants.length }})</h3>
        <div
          v-for="participant in participants"
          :key="participant.id"
          class="participant"
        >
          <i class="icon-user" :class="{ speaking: participant.speaking }"></i>
          {{ participant.name }}
          <span v-if="participant.id === 1">(Вы)</span>
        </div>
      </div>
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
      messages: [
        {
          sender: "Собеседник",
          text: "Здравствуйте! Давайте начнём собеседование.",
        },
      ],
      newMessage: "",
      participants: [
        { id: 1, name: "Иван Петров", speaking: false },
        { id: 2, name: "Анна Сидорова", speaking: true },
      ],
      localStream: null,
      remoteStream: null,
    };
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

        // Симуляция удаленного потока (в реальном приложении нужно WebRTC подключение)
        setTimeout(() => {
          this.remoteStream = new MediaStream(this.localStream.getTracks());
          this.$refs.remoteVideo.srcObject = this.remoteStream;
        }, 1000);
      } catch (error) {
        console.error("Ошибка доступа к медиаустройствам:", error);
      }
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
      const average = sum / dataArray.length;

      this.isSpeaking = average > 10 && !this.micMuted;
      this.participants[0].speaking = this.isSpeaking;

      this.animationId = requestAnimationFrame(this.detectSound);
    },
    toggleMic() {
      this.micMuted = !this.micMuted;
      if (this.localStream) {
        this.localStream.getAudioTracks().forEach((track) => {
          track.enabled = !this.micMuted;
        });
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
    sendMessage() {
      if (this.newMessage.trim() && !this.micMuted) {
        this.messages.push({
          sender: "Вы",
          text: this.newMessage,
        });
        this.newMessage = "";
        this.scrollChatToBottom();
      }
    },
    scrollChatToBottom() {
      const chat = this.$el.querySelector(".chat-messages");
      if (chat) {
        setTimeout(() => {
          chat.scrollTop = chat.scrollHeight;
        }, 50);
      }
    },
    endInterview() {
      if (confirm("Завершить собеседование?")) {
        if (this.localStream) {
          this.localStream.getTracks().forEach((track) => track.stop());
        }
        this.$router.push("/feedback");
      }
    },
  },
  mounted() {
    this.startVideo();
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
  display: grid;
  grid-template-columns: 3fr 1fr;
  grid-template-rows: auto 80px;
  height: 100vh;
  background: #1c1f2e;
  color: white;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.main-video {
  grid-column: 1;
  grid-row: 1;
  position: relative;
  background: #0f121f;
  height: calc(100vh - 80px);
}

.main-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.local-video {
  position: absolute;
  bottom: 100px;
  right: 20px;
  width: 200px;
  height: 120px;
  border: 2px solid #42b983;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.local-video.speaking {
  border-color: #ff5722;
  box-shadow: 0 0 15px #ff5722;
}

.local-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.volume-indicator {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.local-video.speaking .volume-indicator::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: #ff5722;
  animation: volumePulse 1.5s infinite;
}

.user-info {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.7);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.4;
}

.user-name {
  display: block;
  font-weight: bold;
}

.user-status {
  display: block;
  font-size: 0.8em;
  color: #42b983;
}

.local-video.speaking .user-status {
  color: #ff5722;
}

.control-panel {
  grid-column: 1;
  grid-row: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: #292d3e;
  padding: 10px;
}

.control-panel button {
  padding: 10px 20px;
  border-radius: 20px;
  border: none;
  background: #3a3f55;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.control-panel button:hover {
  transform: translateY(-2px);
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

.sidebar {
  grid-column: 2;
  grid-row: 1 / span 2;
  background: #252837;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #3a3f55;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  padding-right: 5px;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #3a3f55;
  border-radius: 8px;
  word-break: break-word;
}

.message.own-message {
  background: #42b983;
  color: white;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background: #3a3f55;
  color: white;
}

.chat-input input:disabled {
  opacity: 0.6;
}

.chat-input button {
  padding: 0 15px;
  border-radius: 8px;
  border: none;
  background: #42b983;
  color: white;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #3a3f55;
  cursor: not-allowed;
}

.participants {
  padding: 15px;
  border-top: 1px solid #3a3f55;
}

.participants h3 {
  margin-bottom: 15px;
  font-size: 16px;
}

.participant {
  padding: 8px 12px;
  margin-top: 5px;
  background: #3a3f55;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-user {
  color: #42b983;
}

.icon-user.speaking {
  color: #ff5722;
  animation: pulse 1.5s infinite;
}

@keyframes volumePulse {
  0% {
    transform: scaleX(0.3);
    opacity: 0.7;
  }
  50% {
    transform: scaleX(1);
    opacity: 1;
  }
  100% {
    transform: scaleX(0.3);
    opacity: 0.7;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

/* Иконки (можно заменить на реальные иконки из шрифта или SVG) */
.icon-mic::before {
  content: "🎤";
}
.icon-camera::before {
  content: "📷";
}
.icon-phone::before {
  content: "📞";
}
.icon-send::before {
  content: "✉️";
}
.icon-user::before {
  content: "👤";
}
</style>
