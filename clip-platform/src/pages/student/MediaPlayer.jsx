// src/pages/student/MediaPlayer.jsx
import React, { useState } from 'react';
import VideoSection from '../../components/student/VideoPlayer/VideoSection';
import ChatSection from '../../components/student/Chat/ChatSection';
import YouTubeRecommendations from '../../components/student/VideoPlayer/YouTubeRecommendations';
import Sidebar from '../../components/student/Navigation/Sidebar';
import { Bell, MessageSquare } from 'lucide-react';

const MediaPlayer = () => {
  const [currentVideo, setCurrentVideo] = useState('dQw4w9WgXcQ'); // Default video ID

  const handleVideoSelect = (videoId) => {
    setCurrentVideo(videoId);
    // In a real application, you would also:
    // 1. Track this selection in student's watch history
    // 2. Update learning analytics
    // 3. Store progress/completion data
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 p-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-semibold">Ongoing Lesson</h1>
            <div className="flex items-center space-x-4">
              <Bell className="w-6 h-6 text-gray-600 cursor-pointer hover:text-gray-800" />
              <MessageSquare className="w-6 h-6 text-gray-600 cursor-pointer hover:text-gray-800" />
            </div>
          </div>
        </header>

        {/* Video Content */}
        <div className="flex-1 overflow-auto">
          <div className="max-w-6xl mx-auto p-6">
            <div className="bg-white rounded-xl shadow-sm">
              <VideoSection currentVideo={`https://www.youtube.com/watch?v=${currentVideo}`} />
              <div className="p-6">
                <YouTubeRecommendations onVideoSelect={handleVideoSelect} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar */}
      <ChatSection />
    </div>
  );
};

export default MediaPlayer;