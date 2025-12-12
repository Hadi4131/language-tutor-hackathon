import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import { WelcomePage } from './components/WelcomePage';
import Login from './components/Login';
import Signup from './components/Signup';
import VoiceInterface from './components/VoiceInterface';
import VoiceSelector from './components/VoiceSelector';
import { Mic, Sparkles, CheckCircle, Zap, Brain, Volume2, Home, HelpCircle, LogOut } from 'lucide-react';
import { useAuth } from './contexts/AuthContext';

function MainApp() {
    const [showAbout, setShowAbout] = useState(false);
    const [selectedVoice, setSelectedVoice] = useState(null);
    const { logout, currentUser } = useAuth();

    const handleLogout = async () => {
        try {
            await logout();
        } catch (error) {
            console.error('Failed to log out', error);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 relative overflow-hidden">
            {/* Animated gradient overlay for depth */}
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-900/30 via-purple-900/30 to-pink-900/30 animate-pulse-slow"></div>

            {/* Content */}
            <div className="relative z-10">
                {/* Header */}
                <nav className="fixed top-0 left-0 right-0 z-50 bg-white bg-opacity-10 backdrop-blur-md border-b border-white border-opacity-20">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex items-center justify-between h-20">
                            <div className="flex items-center space-x-3">
                                <div className="w-12 h-12 bg-white bg-opacity-20 backdrop-blur-sm rounded-full flex items-center justify-center border border-white border-opacity-30">
                                    <span className="text-3xl">🗣️</span>
                                </div>
                                <div>
                                    <h1 className="text-xl font-bold text-white">AI Language Tutor</h1>
                                    <p className="text-xs text-white opacity-70">
                                        {currentUser?.email || 'Practice • Learn • Improve'}
                                    </p>
                                </div>
                            </div>
                            <div className="flex items-center space-x-3">
                                <button
                                    onClick={() => setShowAbout(!showAbout)}
                                    className="px-6 py-3 bg-white bg-opacity-20 backdrop-blur-sm text-white rounded-full hover:scale-105 hover:bg-opacity-30 transition-all font-semibold border border-white border-opacity-30 flex items-center space-x-2"
                                >
                                    <HelpCircle className="w-4 h-4" />
                                    <span className="hidden md:inline">{showAbout ? 'Practice' : 'How It Works'}</span>
                                </button>
                                <button
                                    onClick={handleLogout}
                                    className="px-6 py-3 bg-red-500 bg-opacity-30 backdrop-blur-sm text-white rounded-full hover:scale-105 hover:bg-opacity-40 transition-all font-semibold border border-red-400 border-opacity-30 flex items-center space-x-2"
                                >
                                    <LogOut className="w-4 h-4" />
                                    <span className="hidden md:inline">Logout</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Main Content */}
                <div className="pt-24 pb-24 px-4 min-h-screen">
                    {showAbout ? (
                        /* About Section */
                        <div className="max-w-6xl mx-auto space-y-8 animate-fadeIn">
                            {/* Hero */}
                            <div className="text-center mb-12">
                                <h2 className="text-5xl md:text-6xl font-bold text-white mb-4">
                                    Master English with
                                    <span className="block mt-2 bg-gradient-to-r from-cyan-400 to-pink-400 bg-clip-text text-transparent">
                                        AI Technology
                                    </span>
                                </h2>
                                <p className="text-xl text-gray-200 max-w-2xl mx-auto">
                                    Real-time pronunciation feedback, intelligent grammar corrections, and personalized learning tips
                                </p>
                            </div>

                            {/* Quick Start */}
                            <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-3xl p-10 border border-white border-opacity-20 card-hover">
                                <h3 className="text-3xl font-bold text-white mb-8 text-center flex items-center justify-center">
                                    <Sparkles className="w-8 h-8 mr-3 text-yellow-400" />
                                    Quick Start Guide
                                </h3>
                                <div className="grid md:grid-cols-4 gap-6">
                                    {[
                                        { num: 1, icon: <Mic className="w-8 h-8" />, title: 'Click Mic', desc: 'Press the microphone to start' },
                                        { num: 2, icon: '🗣️', title: 'Speak', desc: 'Say anything in English' },
                                        { num: 3, icon: <Brain className="w-8 h-8" />, title: 'AI Analyzes', desc: 'Get instant feedback' },
                                        { num: 4, icon: <CheckCircle className="w-8 h-8" />, title: 'Improve', desc: 'Learn from suggestions' }
                                    ].map((step, i) => (
                                        <div key={i} className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl p-6 text-white transform hover:scale-105 transition-all">
                                            <div className="text-6xl mb-4">{typeof step.icon === 'string' ? step.icon : step.icon}</div>
                                            <div className="text-3xl font-bold mb-2">{step.num}</div>
                                            <h4 className="text-lg font-bold mb-2">{step.title}</h4>
                                            <p className="text-sm opacity-90">{step.desc}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Features */}
                            <div className="grid md:grid-cols-3 gap-6">
                                {[
                                    { icon: <Mic className="w-8 h-8" />, title: 'Pronunciation Scoring', desc: '0-100 score with detailed phoneme analysis' },
                                    { icon: <Brain className="w-8 h-8" />, title: 'Smart Corrections', desc: 'AI-powered grammar and vocabulary feedback' },
                                    { icon: <Volume2 className="w-8 h-8" />, title: 'Voice Responses', desc: 'Natural AI voice with helpful tips' },
                                    { icon: <Zap className="w-8 h-8" />, title: 'Instant Feedback', desc: 'Real-time speech recognition' },
                                    { icon: <CheckCircle className="w-8 h-8" />, title: 'Learning Tips', desc: 'Personalized recommendations' },
                                    { icon: <Sparkles className="w-8 h-8" />, title: 'Follow-ups', desc: 'Engaging conversation flow' }
                                ].map((feature, i) => (
                                    <div key={i} className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-6 border border-white border-opacity-20 card-hover">
                                        <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white mb-4">
                                            {feature.icon}
                                        </div>
                                        <h4 className="text-xl font-bold text-white mb-2">{feature.title}</h4>
                                        <p className="text-gray-200">{feature.desc}</p>
                                    </div>
                                ))}
                            </div>

                            {/* CTA */}
                            <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl p-12 text-center text-white shadow-2xl">
                                <h3 className="text-3xl font-bold mb-4">Ready to Improve Your English?</h3>
                                <p className="text-lg mb-6 opacity-90">Start practicing now with AI-powered feedback</p>
                                <button
                                    onClick={() => setShowAbout(false)}
                                    className="px-8 py-4 bg-white text-purple-600 rounded-full hover:scale-105 transition-transform font-bold text-lg shadow-lg"
                                >
                                    Start Practicing Now →
                                </button>
                            </div>
                        </div>
                    ) : (
                        /* Practice Interface */
                        <div className="animate-fadeIn max-w-4xl mx-auto">
                            <div className="text-center mb-8">
                                <h2 className="text-4xl md:text-5xl font-bold text-white mb-2">Practice Speaking</h2>
                                <p className="text-gray-200 text-lg">Click the microphone and speak naturally</p>
                            </div>

                            <div className="mb-8 flex justify-start">
                                <VoiceSelector
                                    selectedVoice={selectedVoice}
                                    onSelect={setSelectedVoice}
                                />
                            </div>

                            <VoiceInterface
                                personality="friendly"
                                userLevel="intermediate"
                                voiceId={selectedVoice}
                            />
                        </div>
                    )}
                </div>

                {/* Footer */}
                <footer className="fixed bottom-0 left-0 right-0 bg-white bg-opacity-10 backdrop-blur-md border-t border-white border-opacity-20">
                    <div className="max-w-7xl mx-auto px-4 py-4">
                        <div className="flex items-center justify-center space-x-4 text-sm">
                            <span className="px-3 py-1 bg-blue-500 bg-opacity-30 rounded-full text-white text-xs">
                                Google Gemini
                            </span>
                            <span className="px-3 py-1 bg-green-500 bg-opacity-30 rounded-full text-white text-xs">
                                Speech-to-Text
                            </span>
                            <span className="px-3 py-1 bg-purple-500 bg-opacity-30 rounded-full text-white text-xs">
                                ElevenLabs
                            </span>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
    );
}

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/welcome" element={<WelcomePage onContinue={() => window.location.href = '/login'} />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/signup" element={<Signup />} />
                    <Route
                        path="/*"
                        element={
                            <ProtectedRoute>
                                <MainApp />
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
