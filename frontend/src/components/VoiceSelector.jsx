import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Loader2, ChevronDown, Check, Volume2 } from 'lucide-react';

const VoiceSelector = ({ selectedVoice, onSelect }) => {
    const [voices, setVoices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        fetchVoices();

        // Click outside to close
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const fetchVoices = async () => {
        try {
            const apiUrl = import.meta.env.DEV
                ? 'http://localhost:8000'
                : (import.meta.env.VITE_API_URL || 'http://localhost:8000');
            const response = await axios.get(`${apiUrl}/api/v1/voices`);
            setVoices(response.data.voices);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching voices:', err);
            setError('Failed to load voices');
            setLoading(false);
        }
    };

    const getSelectedName = () => {
        const voice = voices.find(v => v.voice_id === selectedVoice);
        return voice ? voice.name : "Default Voice";
    };

    return (
        <div className="relative w-64" ref={dropdownRef}>
            {/* Header / Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                disabled={loading || !!error}
                className={`
                    w-full flex items-center justify-between px-4 py-3 
                    bg-white bg-opacity-10 backdrop-blur-md 
                    border border-white border-opacity-20 rounded-xl 
                    text-white transition-all duration-200 
                    hover:bg-opacity-20 focus:outline-none focus:ring-2 focus:ring-purple-400
                    ${isOpen ? 'ring-2 ring-purple-400 bg-opacity-20' : ''}
                `}
            >
                <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                        <Volume2 className="w-4 h-4 text-white" />
                    </div>
                    <div className="text-left">
                        <span className="block text-xs text-purple-200 font-medium uppercase tracking-wider">Voice</span>
                        <span className="block font-semibold truncate leading-none mt-0.5">
                            {loading ? 'Loading...' : getSelectedName()}
                        </span>
                    </div>
                </div>
                {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin opacity-70" />
                ) : (
                    <ChevronDown className={`w-5 h-5 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
                )}
            </button>

            {/* Error Message */}
            {error && (
                <div className="absolute top-full mt-2 left-0 w-full bg-red-500 bg-opacity-90 text-white text-xs p-2 rounded-lg z-50">
                    {error}
                </div>
            )}

            {/* Dropdown Menu */}
            {isOpen && !loading && !error && (
                <div className="absolute top-full mt-2 left-0 w-full max-h-80 overflow-y-auto custom-scrollbar 
                    bg-gray-900 bg-opacity-95 backdrop-blur-xl border border-white border-opacity-10 
                    rounded-xl shadow-2xl z-50 animate-fadeIn origin-top transform transition-all">
                    <div className="p-2 space-y-1">
                        {voices.map((voice) => (
                            <button
                                key={voice.voice_id}
                                onClick={() => {
                                    onSelect(voice.voice_id);
                                    setIsOpen(false);
                                }}
                                className={`
                                    w-full flex items-center justify-between p-3 rounded-lg transition-all
                                    ${selectedVoice === voice.voice_id
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                                        : 'text-gray-300 hover:bg-white hover:bg-opacity-10'
                                    }
                                `}
                            >
                                <div className="text-left">
                                    <div className="font-semibold">{voice.name}</div>
                                    <div className="text-xs opacity-70 flex items-center space-x-2">
                                        <span>{voice.category}</span>
                                        {voice.description && (
                                            <>
                                                <span>•</span>
                                                <span className="truncate max-w-[100px]">{voice.description}</span>
                                            </>
                                        )}
                                    </div>
                                </div>
                                {selectedVoice === voice.voice_id && (
                                    <Check className="w-4 h-4" />
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default VoiceSelector;
