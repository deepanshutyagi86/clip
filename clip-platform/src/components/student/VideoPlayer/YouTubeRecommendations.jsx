import React, { useState, useEffect, useCallback } from 'react';
import { Search, Clock, PlayCircle, Loader2 } from 'lucide-react';
import { searchYouTubeVideos, getRelatedVideos, formatDuration } from '../../../services/youtubeService';
import _ from 'lodash';

// Mock student data structure
const studentData = {
  id: 'ST001',
  grade: 6,
  subjects: ['Mathematics', 'Science'],
  currentTopics: ['algebra', 'chemical_reactions'],
  learningPreferences: {
    preferredDuration: '10-15min',
    difficulty: 'intermediate'
  },
  recentSearches: [],
  watchHistory: []
};

const YouTubeRecommendations = ({ onVideoSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [personalizedPlaylists, setPersonalizedPlaylists] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Generate search query based on student context
  const generateContextualQuery = (topic) => {
    const gradeLevel = `grade ${studentData.grade}`;
    return `${topic} ${gradeLevel} education tutorial`;
  };

  // Debounced search function
  const debouncedSearch = useCallback(
    _.debounce(async (query) => {
      try {
        setLoading(true);
        const results = await searchYouTubeVideos(query);
        setSearchResults(results);
        setError(null);
      } catch (err) {
        setError('Failed to fetch search results');
        setSearchResults([]);
      } finally {
        setLoading(false);
      }
    }, 500),
    []
  );

  // Generate personalized playlists based on student data
  const generatePersonalizedPlaylists = async () => {
    try {
      setLoading(true);
      const playlists = await Promise.all(
        studentData.currentTopics.map(async (topic) => {
          const query = generateContextualQuery(topic);
          const videos = await searchYouTubeVideos(query, 5);
          return {
            topic,
            videos
          };
        })
      );
      setPersonalizedPlaylists(playlists);
    } catch (err) {
      setError('Failed to generate playlists');
      setPersonalizedPlaylists([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle search input
  useEffect(() => {
    if (searchQuery.trim()) {
      debouncedSearch(searchQuery);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery, debouncedSearch]);

  // Generate initial playlists
  useEffect(() => {
    generatePersonalizedPlaylists();
  }, []);

  const VideoCard = ({ video }) => (
    <div 
      className="flex-shrink-0 w-72 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => onVideoSelect(video.id)}
    >
      <div className="relative">
        <img
          src={video.thumbnail}
          alt={video.title}
          className="w-full h-40 object-cover rounded-t-lg"
        />
        <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/70 rounded text-white text-xs">
          {formatDuration(video.duration)}
        </div>
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-sm line-clamp-2 h-10">{video.title}</h3>
        <p className="text-xs text-gray-600 mt-1">{video.channelTitle}</p>
        <div className="flex items-center space-x-2 mt-2 text-xs text-gray-600">
          <PlayCircle className="w-3 h-3" />
          <span>{parseInt(video.viewCount).toLocaleString()} views</span>
        </div>
      </div>
    </div>
  );
  
  const PlaylistSection = ({ playlist }) => (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-4 capitalize px-4">
        {playlist.topic.replace('_', ' ')} Playlist
      </h2>
      <div className="relative">
        <div className="flex overflow-x-auto gap-4 pb-4 px-4 hide-scrollbar">
          {playlist.videos.map(video => (
            <VideoCard key={video.id} video={video} />
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto py-6">
      {/* Search Bar */}
      <div className="relative mb-6">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search for educational videos..."
          className="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <Search className="absolute left-3 top-3.5 text-gray-400 w-5 h-5" />
        {loading && (
          <Loader2 className="absolute right-3 top-3.5 w-5 h-5 animate-spin text-blue-500" />
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="text-red-500 mb-4">{error}</div>
      )}

      {/* Search Results */}
      {searchQuery && searchResults.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Search Results</h2>
          <div className="grid gap-4">
            {searchResults.map(video => (
              <VideoCard key={video.id} video={video} />
            ))}
          </div>
        </div>
      )}

      {/* Personalized Playlists */}
      {!searchQuery && personalizedPlaylists.map(playlist => (
        <PlaylistSection key={playlist.topic} playlist={playlist} />
      ))}
    </div>
  );
};

export default YouTubeRecommendations;