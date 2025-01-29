// src/components/student/VideoPlayer/VideoSection.jsx
import React from 'react';
import ReactPlayer from 'react-player';

const VideoSection = ({ currentVideo }) => {
  return (
    <div className="relative">
      <div className="w-full aspect-video bg-black rounded-lg overflow-hidden">
        <ReactPlayer
          url={currentVideo}
          width="100%"
          height="100%"
          controls
          playing
        />
      </div>
    </div>
  );
};

export default VideoSection;