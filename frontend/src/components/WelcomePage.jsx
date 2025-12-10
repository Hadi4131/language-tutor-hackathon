import React from "react";
import { WavyBackground } from "./ui/WavyBackground";
import { ArrowRight, Sparkles, Zap } from "lucide-react";

export function WelcomePage({ onContinue }) {
    return (
        <WavyBackground
            className="max-w-5xl mx-auto px-4"
            colors={["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"]}
            backgroundFill="linear-gradient(to bottom right, #1e1b4b, #581c87)"
        >
            <div className="text-center space-y-8 animate-fadeIn">
                {/* Logo/Icon */}
                <div className="flex justify-center mb-6">
                    <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-2xl animate-pulse-slow">
                        <span className="text-6xl">🗣️</span>
                    </div>
                </div>

                {/* Main Heading */}
                <h1 className="text-5xl md:text-7xl font-bold text-white mb-4">
                    Welcome to
                    <span className="block mt-2 bg-gradient-to-r from-cyan-400 to-pink-400 bg-clip-text text-transparent">
                        AI Language Tutor
                    </span>
                </h1>

                {/* Subtitle */}
                <p className="text-xl md:text-2xl text-gray-200 max-w-2xl mx-auto leading-relaxed">
                    Master English with real-time AI-powered pronunciation feedback,
                    intelligent grammar corrections, and personalized learning tips
                </p>

                {/* Feature Pills */}
                <div className="flex flex-wrap items-center justify-center gap-4 my-8">
                    <div className="flex items-center space-x-2 bg-white bg-opacity-20 backdrop-blur-sm px-4 py-2 rounded-full text-white">
                        <Sparkles className="w-5 h-5" />
                        <span>AI-Powered</span>
                    </div>
                    <div className="flex items-center space-x-2 bg-white bg-opacity-20 backdrop-blur-sm px-4 py-2 rounded-full text-white">
                        <Zap className="w-5 h-5" />
                        <span>Real-time Feedback</span>
                    </div>
                    <div className="flex items-center space-x-2 bg-white bg-opacity-20 backdrop-blur-sm px-4 py-2 rounded-full text-white">
                        <span className="text-xl">🎯</span>
                        <span>Pronunciation Scoring</span>
                    </div>
                </div>

                {/* CTA Button */}
                <button
                    onClick={onContinue}
                    className="group mt-8 px-10 py-5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full text-xl font-bold shadow-2xl hover:scale-110 hover:shadow-pink-500/50 transition-all duration-300 flex items-center space-x-3 mx-auto"
                >
                    <span>Start Learning Now</span>
                    <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
                </button>

                {/* Powered By */}
                <div className="mt-12 pt-8 border-t border-white border-opacity-20">
                    <p className="text-sm text-gray-300 mb-4">Powered by Advanced AI Technology</p>
                    <div className="flex items-center justify-center space-x-4 text-xs">
                        <span className="px-3 py-1 bg-blue-500 bg-opacity-30 rounded-full text-white">
                            Google Gemini
                        </span>
                        <span className="px-3 py-1 bg-green-500 bg-opacity-30 rounded-full text-white">
                            Speech-to-Text
                        </span>
                        <span className="px-3 py-1 bg-purple-500 bg-opacity-30 rounded-full text-white">
                            ElevenLabs
                        </span>
                    </div>
                </div>
            </div>
        </WavyBackground>
    );
}
