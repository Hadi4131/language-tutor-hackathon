# About the Project

## 💡 Inspiration
We wanted to democratize access to high-quality language tutoring. Language learners often lack confidence in speaking due to anxiety and fear of judgment. Human tutors are effective but expensive and not always available. With the advancements in **Google Cloud's Gemini** for understanding context and **ElevenLabs** for human-like speech, we realized we could build an AI tutor that feels like a real person—a safe, judgment-free zone where learners can practice speaking anytime.

## 🤖 What it does
**Echo** is an interactive web application that acts as your personal English tutor.
*   **Conversational Practice**: You speak to the AI, and it responds with a natural, human-like voice (powered by **ElevenLabs**).
*   **Real-time Feedback**: As you speak, the app analyzes your pronunciation and grammar in real-time.
*   **Adaptive Learning**: Using **Google Gemini**, the AI understands your proficiency level and adjusts its vocabulary and speaking speed accordingly.
*   **Voice Selection**: Users can choose their preferred tutor "persona" from a curated list of diverse voices (e.g., American Professional, British Formal).

## ⚙️ How we built it
We built Echo using a modern tech stack focused on speed and user experience:

1.  **Frontend**: We used **React** and **Vite** for a fast, responsive UI, designed with a "glassmorphism" aesthetic to feel transparent and modern.
2.  **Voice Integration**: We deeply integrated the **ElevenLabs API** to generate high-fidelity speech. We implemented dynamic voice selection, allowing users to instantly switch between tutor personas (e.g., swapping from "Zara" to "Frederick").
3.  **Intelligence**: The core logic is powered by **Google Cloud Vertex AI (Gemini Flash)**. We feed the user's transcript to Gemini, which generates a pedagogically sound response, including grammatical corrections and learning tips.
4.  **Speech Recognition**: We utilized **Google Cloud Speech-to-Text** for accurate transcription of user audio.
5.  **Backend**: A **FastAPI** (Python) server orchestrates the complex audio processing pipeline, stitching together STT, LLM generation, and TTS into a seamless flow.

## 🚧 Challenges we ran into
*   **Latency**: Creating a real-time conversational loop is difficult. The delay between a user finishing their sentence and the AI responding breaks immersion. We optimized the audio pipeline and used **Gemini Flash** to minimize this latency.
*   **Voice Consistency**: Ensuring the AI maintained a consistent persona (voice + teaching style) required careful prompt engineering and state management.
*   **API Resilience**: Handling the asynchronous nature of multiple AI services (STT -> LLM -> TTS) meant we had to build robust error handling. For instance, we implemented a fallback system for voice selection to ensure the app never "loses its voice" even if the API experiences hiccups.

## 🏅 Accomplishments that we're proud of
*   Achieving a near-human conversational flow where the AI feels like a supportive teacher, not a robot.
*   Successfully integrating **ElevenLabs** to give the AI distinct "personalities" through different voices.
*   Building a robust fallback system that ensures the app keeps working even if an external API has a momentary outage.

## 🧠 What we learned
*   The importance of **latency** in voice interfaces—even a second of delay contributes significantly to "cognitive load" for the user.
*   How to effectively combine distinct AI agents (Gemini for logic, ElevenLabs for voice) to create a product greater than the sum of its parts.
*   The value of **fallback mechanisms** in dependent systems; if one API fails, the user experience should degrade gracefully, not crash.

## 🚀 What's next for Echo
*   **Multimodal Input**: Letting users point their camera at objects to learn their names in English.
*   **Gamification**: Adding streaks, badges, and leaderboards to improve long-term retention.
*   **More Languages**: Expanding beyond English to support Spanish, French, and Mandarin.
