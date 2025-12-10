import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Trophy, Medal, Award } from 'lucide-react';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchLeaderboard();
    }, []);

    const fetchLeaderboard = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/gamification/leaderboard?limit=20');
            setLeaderboard(response.data.leaderboard);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching leaderboard:', error);
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    const getMedalIcon = (rank) => {
        if (rank === 1) return { icon: <Trophy className="w-8 h-8 text-yellow-500" />, bg: 'bg-yellow-50' };
        if (rank === 2) return { icon: <Medal className="w-8 h-8 text-gray-400" />, bg: 'bg-gray-50' };
        if (rank === 3) return {
            icon:

                <Award className="w-8 h-8 text-orange-500" />, bg: 'bg-orange-50'
        };
        return { icon: <span className="text-xl font-bold text-gray-400">#{rank}</span>, bg: 'bg-white' };
    };

    return (
        <div className="max-w-3xl mx-auto p-6">
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">🏆 Global Leaderboard</h2>
                <p className="text-gray-600">Compete with learners worldwide!</p>
            </div>

            <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                            <tr>
                                <th className="px-6 py-4 text-left text-sm font-semibold">Rank</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold">Player</th>
                                <th className="px-6 py-4 text-right text-sm font-semibold">Points</th>
                                <th className="px-6 py-4 text-right text-sm font-semibold">Streak</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {leaderboard.map((entry, idx) => {
                                const medal = getMedalIcon(entry.rank);
                                return (
                                    <tr
                                        key={idx}
                                        className={`${medal.bg} hover:bg-blue-50 transition-colors`}
                                    >
                                        <td className="px-6 py-4">
                                            <div className="flex items-center justify-center w-12">
                                                {medal.icon}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <p className="font-medium text-gray-800">{entry.display_name}</p>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <span className="font-bold text-blue-600">{entry.total_points}</span>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <span className="font-bold text-orange-600">{entry.current_streak} 🔥</span>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Leaderboard;
