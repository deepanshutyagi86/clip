import React, { useState, useEffect } from 'react';
import ReactPlayer from 'react-player';
import { MessageSquare, BookOpen, ListVideo } from 'lucide-react';

// Import components (we'll create these next)
import ChatBot from '../../components/student/Chat/ChatBot';
import VideoControls from '../../components/student/VideoPlayer/Controls';
import RecommendedPlaylists from '../../components/student/Dashboard/RecommendedPlaylists';
import AdaptivePrompt from '../../components/student/Popups/AdaptivePrompt';

const MediaPlayer = () => {
  const [showChat, setShowChat] = useState(false);
  const [showPrompt, setShowPrompt] = useState(false);
  const [currentVideo, setCurrentVideo] = useState('https://www.youtube.com/watch?v=dQw4w9WgXcQ');

  // Simulate random prompts
  useEffect(() => {
    const promptTimer = setInterval(() => {
      setShowPrompt(true);
      setTimeout(() => setShowPrompt(false), 5000);
    }, 15000);

    return () => clearInterval(promptTimer);
  }, []);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Video Section */}
        <div className="w-full bg-black aspect-video">
          <ReactPlayer
            url={currentVideo}
            width="100%"
            height="100%"
            controls
            playing
          />
        </div>

        {/* Video Info */}
        <div className="p-4 bg-white shadow">
          <h1 className="text-2xl font-semibold">Introduction to Mathematics</h1>
          <p className="text-gray-600 mt-2">
            Learn the fundamentals of mathematics with our comprehensive guide.
          </p>
        </div>
      </div>

      {/* Sidebar */}
      <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200 flex gap-4">
          <button
            onClick={() => setShowChat(!showChat)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              showChat ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            Chat
          </button>
        </div>

        {showChat ? (
          <ChatBot />
        ) : (
          <RecommendedPlaylists onVideoSelect={setCurrentVideo} />
        )}
      </div>

      {/* Popup Dialog */}
      {showPrompt && (
        <AdaptivePrompt onClose={() => setShowPrompt(false)} />
      )}
    </div>
  );
};

export default MediaPlayer;