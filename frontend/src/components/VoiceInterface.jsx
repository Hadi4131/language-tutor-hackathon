import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const VoiceInterface = ({ personality = 'friendly', userLevel = 'intermediate', voiceId }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [analysis, setAnalysis] = useState(null);
    const [pronunciation, setPronunciation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const { getIdToken } = useAuth();

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Please allow microphone access to use this feature.');
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                await sendAudioToBackend(audioBlob);
            };
        }
    };

    const sendAudioToBackend = async (audioBlob) => {
        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.webm');

        try {
            // Get Firebase ID token
            const token = await getIdToken();

            // Use environment variable for API URL (production) or fallback to relative path (development)
            const apiUrl = import.meta.env.DEV
                ? 'http://localhost:8000'
                : (import.meta.env.VITE_API_URL || '');

            // Construct URL with query parameters
            let url = `${apiUrl}/api/v1/conversation/audio?personality=${personality}&user_level=${userLevel}`;
            if (voiceId) {
                url += `&voice_id=${voiceId}`;
            }

            const response = await axios.post(
                url,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        ...(token && { 'Authorization': `Bearer ${token}` })
                    },
                }
            );

            console.log("Response:", response.data);
            setTranscript(response.data.transcript);
            setAnalysis(response.data.analysis);
            setPronunciation(response.data.pronunciation);

            // Play returned audio or fallback
            if (response.data.audio_base64) {
                const audioSrc = `data:audio/mp3;base64,${response.data.audio_base64}`;
                const audio = new Audio(audioSrc);
                audio.play();
            }
        } catch (error) {
            console.error('Error sending audio:', error);
            alert('Error processing your speech. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleMicClick = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const getPronunciationColor = (score) => {
        if (score >= 85) return 'from-green-500 to-emerald-500';
        if (score >= 70) return 'from-yellow-500 to-orange-500';
        return 'from-orange-500 to-red-500';
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-8 p-6 w-full max-w-4xl mx-auto">
            {/* Microphone Button */}
            <div className="relative">
                <button
                    onClick={handleMicClick}
                    disabled={isLoading}
                    className={`
                        relative w-32 h-32 rounded-full shadow-2xl transition-all duration-300 transform
                        ${isRecording
                            ? 'bg-gradient-to-br from-red-500 to-pink-500 scale-110 animate-pulse'
                            : 'bg-gradient-to-br from-purple-600 to-pink-600 hover:scale-110'
                        }
                        ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-pink-500/50'}
                    `}
                >
                    {isLoading ? (
                        <Loader2 className="w-16 h-16 text-white animate-spin mx-auto" />
                    ) : isRecording ? (
                        <MicOff className="w-16 h-16 text-white mx-auto" />
                    ) : (
                        <Mic className="w-16 h-16 text-white mx-auto" />
                    )}
                </button>

                {isRecording && (
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                        <span className="px-4 py-1 bg-red-500 text-white text-sm font-bold rounded-full animate-pulse">
                            Recording...
                        </span>
                    </div>
                )}
            </div>

            <p className="text-white text-center text-lg">
                {isRecording ? 'Speak now...' : isLoading ? 'Processing...' : 'Click to start speaking'}
            </p>

            {/* Transcript */}
            {transcript && (
                <div className="w-full bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-2xl border border-white border-opacity-20 animate-fadeIn">
                    <p className="text-sm font-semibold text-cyan-300 uppercase tracking-wide mb-2">You said:</p>
                    <p className="text-white text-xl font-medium">{transcript}</p>
                </div>
            )}

            {/* Pronunciation Score */}
            {pronunciation && (
                <div className="w-full bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-2xl border border-white border-opacity-20 space-y-4 animate-fadeIn">
                    <div className="flex items-center justify-between">
                        <p className="text-sm font-semibold text-cyan-300 uppercase tracking-wide">Pronunciation Score</p>
                        <div className={`px-4 py-2 bg-gradient-to-r ${getPronunciationColor(pronunciation.score)} rounded-full`}>
                            <span className="text-white font-bold text-2xl">{Math.round(pronunciation.score)}</span>
                        </div>
                    </div>
                    {pronunciation.feedback && (
                        <p className="text-white text-sm opacity-90">{pronunciation.feedback}</p>
                    )}
                    {pronunciation.problematic_phonemes && pronunciation.problematic_phonemes.length > 0 && (
                        <div>
                            <p className="text-pink-300 text-sm font-semibold mb-2">Practice these sounds:</p>
                            <div className="flex flex-wrap gap-2">
                                {pronunciation.problematic_phonemes.map((phoneme, i) => (
                                    <span key={i} className="px-3 py-1 bg-pink-500 bg-opacity-30 text-pink-200 rounded-full text-sm">
                                        {phoneme}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* AI Analysis */}
            {analysis && (
                <div className="w-full bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-2xl border border-white border-opacity-20 space-y-4 animate-fadeIn">
                    <p className="text-sm font-semibold text-cyan-300 uppercase tracking-wide">AI Feedback</p>

                    {/* Correction */}
                    {analysis.corrected_sentence !== transcript && (
                        <div className="bg-green-500 bg-opacity-20 p-4 rounded-xl border border-green-400 border-opacity-30">
                            <p className="text-xs text-green-300 mb-1">Correction:</p>
                            <p className="text-green-100 font-medium">{analysis.corrected_sentence}</p>
                        </div>
                    )}

                    {/* Learning Tip */}
                    <div className="bg-blue-500 bg-opacity-20 p-4 rounded-xl border border-blue-400 border-opacity-30">
                        <p className="text-blue-100 font-medium">💡 {analysis.learning_tip}</p>
                    </div>

                    {/* Follow-up Question */}
                    <div className="bg-purple-500 bg-opacity-20 p-4 rounded-xl border border-purple-400 border-opacity-30">
                        <p className="text-purple-100 text-sm">❓ {analysis.follow_up_question}</p>
                    </div>
                </div>
            )}

            {/* Initial State Message */}
            {!transcript && !isRecording && !isLoading && (
                <div className="text-center space-y-4 text-white opacity-70">
                    <p className="text-lg">Press the microphone and speak in English</p>
                    <p className="text-sm">You'll get instant feedback on pronunciation and grammar</p>
                </div>
            )}
        </div>
    );
};

export default VoiceInterface;
