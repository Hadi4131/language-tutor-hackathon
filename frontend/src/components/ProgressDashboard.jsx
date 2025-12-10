import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Trophy, Flame, Award, TrendingUp } from 'lucide-react';

const ProgressDashboard = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/gamification/stats');
            setStats(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching stats:', error);
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

    if (!stats) {
        return <div className="text-center p-8 text-gray-500">No stats available yet. Start practicing!</div>;
    }

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {/* Header Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm opacity-90">Total Points</p>
                            <p className="text-3xl font-bold">{stats.user.total_points}</p>
                        </div>
                        <Trophy className="w-12 h-12 opacity-80" />
                    </div>
                </div>

                <div className="bg-gradient-to-br from-orange-500 to-red-500 text-white p-6 rounded-xl shadow-lg">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm opacity-90">Current Streak</p>
                            <p className="text-3xl font-bold">{stats.user.current_streak} 🔥</p>
                        </div>
                        <Flame className="w-12 h-12 opacity-80" />
                    </div>
                </div>

                <div className="bg-gradient-to-br from-purple-500 to-pink-500 text-white p-6 rounded-xl shadow-lg">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm opacity-90">Global Rank</p>
                            <p className="text-3xl font-bold">#{stats.user.rank || 'N/A'}</p>
                        </div>
                        <TrendingUp className="w-12 h-12 opacity-80" />
                    </div>
                </div>
            </div>

            {/* Progress Stats */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                <h3 className="text-xl font-bold text-gray-800 mb-4">Practice Progress</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                        <p className="text-3xl font-bold text-blue-600">{stats.progress.total_conversations}</p>
                        <p className="text-sm text-gray-600">Conversations</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-bold text-green-600">
                            {Math.round(stats.progress.overall_pronunciation_score) || 0}
                        </p>
                        <p className="text-sm text-gray-600">Avg. Pronunciation</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-bold text-purple-600">{stats.user.longest_streak}</p>
                        <p className="text-sm text-gray-600">Best Streak</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-bold text-orange-600">
                            {Math.round(stats.progress.total_practice_time_minutes) || 0}
                        </p>
                        <p className="text-sm text-gray-600">Minutes Practiced</p>
                    </div>
                </div>
            </div>

            {/* Achievements */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                    <Award className="w-6 h-6 mr-2 text-yellow-500" />
                    Achievements
                </h3>
                {stats.achievements.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {stats.achievements.map((achievement, idx) => (
                            <div
                                key={idx}
                                className="flex items-center space-x-3 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg"
                            >
                                <span className="text-4xl">{achievement.icon}</span>
                                <div>
                                    <p className="font-bold text-gray-800">{achievement.title}</p>
                                    <p className="text-sm text-gray-600">{achievement.description}</p>
                                    <p className="text-xs text-gray-500 mt-1">
                                        {new Date(achievement.earned_at).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500 text-center py-8">
                        No achievements yet. Keep practicing to earn your first badge!
                    </p>
                )}
            </div>
        </div>
    );
};

export default ProgressDashboard;
