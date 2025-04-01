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

    <!-- Ваше видео (превью) -->
    <div class="local-video">
      <video ref="localVideo" autoplay playsinline muted></video>
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
          >
            <strong>{{ message.sender }}:</strong> {{ message.text }}
          </div>
        </div>
        <div class="chat-input">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="Введите сообщение..."
          />
          <button @click="sendMessage">Отправить</button>
        </div>
      </div>

      <div class="participants">
        <h3>Участники ({{ participants.length }})</h3>
        <div
          v-for="participant in participants"
          :key="participant.id"
          class="participant"
        >
          {{ participant.name }}
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
      messages: [
        {
          sender: "Собеседник",
          text: "Здравствуйте! Давайте начнём собеседование.",
        },
      ],
      newMessage: "",
      participants: [
        { id: 1, name: "Вы" },
        { id: 2, name: "Интервьюер" },
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

        // Здесь должна быть логика подключения к удаленному потоку
        // this.remoteStream = ...
        // this.$refs.remoteVideo.srcObject = this.remoteStream
      } catch (error) {
        console.error("Ошибка доступа к медиаустройствам:", error);
      }
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
      if (this.newMessage.trim()) {
        this.messages.push({
          sender: "Вы",
          text: this.newMessage,
        });
        this.newMessage = "";
        // Здесь можно добавить прокрутку чата вниз
      }
    },
    endInterview() {
      if (this.localStream) {
        this.localStream.getTracks().forEach((track) => track.stop());
      }
      this.$router.push("/feedback");
    },
  },
  mounted() {
    this.startVideo();
  },
  beforeUnmount() {
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
  border-radius: 4px;
  overflow: hidden;
}

.local-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.control-panel {
  grid-column: 1;
  grid-row: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: #292d3e;
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
}

.control-panel button.active {
  background: #42b983;
}

.control-panel button.end-call {
  background: #e74c3c;
}

.sidebar {
  grid-column: 2;
  grid-row: 1 / span 2;
  background: #252837;
  display: flex;
  flex-direction: column;
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
}

.message {
  margin-bottom: 10px;
  padding: 8px;
  background: #3a3f55;
  border-radius: 4px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border-radius: 4px;
  border: none;
  background: #3a3f55;
  color: white;
}

.participants {
  padding: 15px;
  border-top: 1px solid #3a3f55;
}

.participant {
  padding: 8px;
  margin-top: 5px;
  background: #3a3f55;
  border-radius: 4px;
}

.user-info {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.5);
  padding: 5px 10px;
  border-radius: 4px;
}

.user-status {
  display: block;
  font-size: 0.8em;
  color: #42b983;
}
</style>
