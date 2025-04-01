<template>
  <div class="interview-container">
    <!-- Основное видео собеседника -->
    <div class="main-video">
      <video ref="remoteVideo">
        <source :src="videoSource" type="video/mp4" />
      </video>
      <div class="user-info">
        <span class="user-name">Собеседник</span>
        <span class="user-status">В сети</span>
      </div>
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

    <!-- Панель управления -->
    <div class="control-panel">
      <button @click="toggleMic" :class="{ active: !micMuted }">
        <img src="./../assets/zvuk.png" alt="">
      </button>
      <button @click="toggleCamera" :class="{ active: !cameraOff }">
        <img src="./../assets/video.png" alt="">
      </button>
      <button @click="endInterview" class="end-call">
        <img src="./../assets/stop.png" alt="">
      </button>
    </div>

    <!-- Боковая панель с чатом -->
    <!-- <div class="sidebar">
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
          :class="{ speaking: participant.speaking }"
        >
          <i class="icon-user"></i>
          {{ participant.name }}
          <span v-if="participant.id === 1">(Вы)</span>
        </div>
      </div>
    </div> -->
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
      messages: [
        {
          sender: "Собеседник",
          text: "Здравствуйте! Давайте начнём собеседование.",
        },
      ],
      newMessage: "",
      participants: [
        { id: 1, name: "Иван Ежов", speaking: false },
        { id: 2, name: "Арсений Ильин", speaking: false },
        { id: 2, name: "Даниил Крупнов", speaking: false },
      ],
      localStream: null,
      remoteStream: null,
    };
  },
  computed: {
    indicatorClass() {
      if (this.micMuted) return "muted";
      return !this.isSpeaking ? "speaking" : "silent";
    },
    statusText() {
      if (this.micMuted) return "Микрофон выключен";
      return !this.isSpeaking ? "Говорите!" : "Молчите!";
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

        // Запускаем ваше видео файлом
        this.$refs.remoteVideo
          .play()
          .catch((e) => console.error("Ошибка воспроизведения:", e));
      } catch (error) {
        console.error("Ошибка доступа к медиаустройствам:", error);
        alert("Не удалось получить доступ к камере/микрофону");
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
      this.$nextTick(() => {
        const chat = this.$el.querySelector(".chat-messages");
        if (chat) chat.scrollTop = chat.scrollHeight;
      });
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
  /* display: grid; */
  /* grid-template-columns: 3fr 1fr; */
  /* grid-template-rows: auto 80px; */
  height: 100vh;
  /* background: #1c1f2e; */
  background-color: #c0c0c0;
  color: white;
  font-family: "SF Compact Display", sans-serif;
  position: relative;
}

.main-video {
  width: 100%;
  /* height: 100%; */
  /* grid-column: 1; */
  /* grid-row: 1; */
  /* position: relative; */
  /* background: #0f121f; */
  /* height: calc(100vh - 80px); */
}

.main-video video {
  width: 100%;
  height: 100vh;
  /* object-fit: cover; */
}

.local-video {
  position: absolute;
  bottom: 100px;
  right: 20px;
  width: 200px;
  height: 120px;
  /* border-radius: 8px; */
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
  /* border-radius: 4px; */
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
  /* height: 120px; */
  /* border-radius: 8px; */
  /* overflow: hidden; */
}

.control-panel button {
}

.control-panel button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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

/* .sidebar {
  grid-column: 2;
  grid-row: 1 / span 2;
  background: #252837;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #3a3f55;
} */

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
  border-bottom: 1px solid #3a3f55;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  padding-right: 5px;
  scrollbar-width: thin;
  scrollbar-color: #42b983 #3a3f55;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #3a3f55;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #42b983;
  border-radius: 3px;
}

.message {
  margin-bottom: 12px;
  padding: 10px 14px;
  background: #3a3f55;
  border-radius: 8px;
  word-break: break-word;
  line-height: 1.4;
  animation: fadeIn 0.3s ease;
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
  padding: 12px 14px;
  border-radius: 8px;
  border: none;
  background: #3a3f55;
  color: white;
  font-size: 14px;
  transition: all 0.2s ease;
}

.chat-input input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #42b983;
}

.chat-input input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.chat-input button {
  padding: 0 16px;
  border-radius: 8px;
  border: none;
  background: #42b983;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chat-input button:hover {
  background: #3aa876;
}

.chat-input button:disabled {
  background: #3a3f55;
  cursor: not-allowed;
  opacity: 0.7;
}

.participants {
  padding: 15px;
  overflow-y: auto;
}

.participants h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #b0bec5;
}

.participant {
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #3a3f55;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s ease;
}

.participant.speaking {
  background: rgba(255, 152, 0, 0.15);
  border-left: 3px solid #ff9800;
}

.participant:hover {
  background: #4a4f65;
}

.icon-user {
  color: #42b983;
  font-style: normal;
}

.participant.speaking .icon-user {
  color: #ff9800;
  animation: pulse 1.5s infinite;
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

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
