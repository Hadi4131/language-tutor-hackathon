import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PersonalitySelector = ({ onSelect, currentPersonality = 'friendly' }) => {
    const [personalities, setPersonalities] = useState([]);
    const [selected, setSelected] = useState(currentPersonality);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchPersonalities();
    }, []);

    const fetchPersonalities = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/personality/available');
            setPersonalities(response.data.personalities);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching personalities:', error);
            setLoading(false);
        }
    };

    const handleSelect = async (personalityId) => {
        try {
            await axios.post('http://localhost:8000/api/v1/personality/select', {
                personality_id: personalityId
            });
            setSelected(personalityId);
            if (onSelect) {
                onSelect(personalityId);
            }
        } catch (error) {
            console.error('Error selecting personality:', error);
        }
    };

    if (loading) {
        return <div className="text-center p-8">Loading personalities...</div>;
    }

    return (
        <div className="max-w-4xl mx-auto p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Choose Your AI Tutor</h2>
            <p className="text-gray-600 mb-6">
                Select a teaching personality that matches your learning style
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {personalities.map((personality) => (
                    <div
                        key={personality.id}
                        onClick={() => handleSelect(personality.id)}
                        className={`
                            cursor-pointer p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105
                            ${selected === personality.id
                                ? 'border-blue-500 bg-blue-50 shadow-lg'
                                : 'border-gray-200 bg-white hover:border-blue-300 hover:shadow-md'
                            }
                        `}
                    >
                        <div className="text-center mb-4">
                            <span className="text-6xl">{personality.avatar_emoji}</span>
                        </div>
                        <h3 className="text-lg font-bold text-gray-800 text-center mb-2">
                            {personality.name}
                        </h3>
                        <p className="text-sm text-gray-600 text-center mb-3">
                            {personality.description}
                        </p>
                        <div className="bg-gray-100 p-3 rounded-lg">
                            <p className="text-xs text-gray-700 italic">
                                "{personality.sample_response}"
                            </p>
                        </div>
                        <div className="mt-3 text-center">
                            <span className={`
                                inline-block px-3 py-1 rounded-full text-xs font-medium
                                ${personality.teaching_style === 'formal'
                                    ? 'bg-purple-100 text-purple-800'
                                    : 'bg-green-100 text-green-800'
                                }
                            `}>
                                {personality.teaching_style}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PersonalitySelector;
