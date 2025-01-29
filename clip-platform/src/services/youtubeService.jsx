// src/services/youtubeService.js
import axios from 'axios';

const API_KEY = 'AIzaSyDDlGs4iL26uBDGFgx7kikqvILYntC50wU'; // Replace with your actual YouTube API key

export const searchYouTubeVideos = async (query, maxResults = 10) => {
  try {
    const response = await axios.get(`https://www.googleapis.com/youtube/v3/search`, {
      params: {
        part: 'snippet',
        maxResults,
        q: query,
        type: 'video',
        videoCategoryId: '27', // Education category
        key: API_KEY
      }
    });

    // Get additional video details (duration, view count)
    const videoIds = response.data.items.map(item => item.id.videoId).join(',');
    const videoDetails = await axios.get(`https://www.googleapis.com/youtube/v3/videos`, {
      params: {
        part: 'contentDetails,statistics',
        id: videoIds,
        key: API_KEY
      }
    });

    // Combine the data
    return response.data.items.map((item, index) => ({
      id: item.id.videoId,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.medium.url,
      channelTitle: item.snippet.channelTitle,
      publishedAt: item.snippet.publishedAt,
      duration: videoDetails.data.items[index]?.contentDetails.duration,
      viewCount: videoDetails.data.items[index]?.statistics.viewCount
    }));
  } catch (error) {
    console.error('YouTube API Error:', error);
    throw error;
  }
};

export const getRelatedVideos = async (videoId, maxResults = 10) => {
  try {
    const response = await axios.get(`https://www.googleapis.com/youtube/v3/search`, {
      params: {
        part: 'snippet',
        maxResults,
        relatedToVideoId: videoId,
        type: 'video',
        key: API_KEY
      }
    });

    return response.data.items.map(item => ({
      id: item.id.videoId,
      title: item.snippet.title,
      thumbnail: item.snippet.thumbnails.medium.url,
      channelTitle: item.snippet.channelTitle
    }));
  } catch (error) {
    console.error('YouTube API Error:', error);
    throw error;
  }
};

// Helper function to format YouTube duration string
export const formatDuration = (duration) => {
  if (!duration) return '0:00';
  
  const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
  const hours = (match[1] || '0').slice(0, -1);
  const minutes = (match[2] || '0').slice(0, -1);
  const seconds = (match[3] || '0').slice(0, -1);
  
  if (hours !== '0') {
    return `${hours}:${minutes.padStart(2, '0')}:${seconds.padStart(2, '0')}`;
  }
  return `${minutes || '0'}:${seconds.padStart(2, '0')}`;
};