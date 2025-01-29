// src/components/student/VideoPlayer/RecommendedVideos.jsx
import React, { useRef } from 'react';
import { ChevronLeft, ChevronRight, Clock } from 'lucide-react';

const RecommendedVideos = ({ onVideoSelect }) => {
  const scrollContainerRef = useRef(null);
  
  const videos = [
    { 
      id: 1, 
      title: 'Introduction to Biology', 
      thumbnail: '/api/placeholder/320/180',
      duration: '10:30'
    },
    { 
      id: 2, 
      title: 'Cell Structure', 
      thumbnail: '/api/placeholder/320/180',
      duration: '8:45'
    },
    { 
      id: 3, 
      title: 'DNA and RNA', 
      thumbnail: '/api/placeholder/320/180',
      duration: '12:15'
    },
    { 
      id: 4, 
      title: 'Photosynthesis', 
      thumbnail: '/api/placeholder/320/180',
      duration: '15:20'
    },
    { 
      id: 5, 
      title: 'Cell Division', 
      thumbnail: '/api/placeholder/320/180',
      duration: '11:10'
    }
  ];

  const scroll = (direction) => {
    if (scrollContainerRef.current) {
      const scrollAmount = 300;
      scrollContainerRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div className="mt-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Recommended Videos</h3>
        <div className="flex space-x-2">
          <button 
            onClick={() => scroll('left')}
            className="p-1 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button 
            onClick={() => scroll('right')}
            className="p-1 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
      
      <div 
        ref={scrollContainerRef}
        className="flex space-x-4 overflow-x-auto pb-4 hide-scrollbar"
      >
        {videos.map(video => (
          <div 
            key={video.id} 
            className="flex-shrink-0 w-64 cursor-pointer group"
            onClick={() => onVideoSelect(`https://youtube.com/watch?v=${video.id}`)}
          >
            <div className="relative">
              <img
                src={video.thumbnail}
                alt={video.title}
                className="w-full h-36 rounded-lg object-cover group-hover:ring-2 ring-blue-400 transition-all"
              />
              <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/70 rounded-md text-white text-xs flex items-center">
                <Clock className="w-3 h-3 mr-1" />
                {video.duration}
              </div>
            </div>
            <h4 className="mt-2 text-sm font-medium group-hover:text-blue-600 transition-colors line-clamp-2">
              {video.title}
            </h4>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendedVideos;