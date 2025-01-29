// src/services/contentVerificationService.js
import axios from 'axios';

const CLAUDE_API_KEY = import.meta.env.VITE_CLAUDE_API_KEY;
const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';

export const verifyEducationalContent = async (videoMetadata) => {
  try {
    const response = await axios.post(
      CLAUDE_API_URL,
      {
        model: "claude-3-opus-20240229",
        max_tokens: 1024,
        messages: [{
          role: "user",
          content: `Analyze this YouTube video metadata to determine if it's genuinely educational content.
            
            Title: ${videoMetadata.title}
            Description: ${videoMetadata.description}
            Channel: ${videoMetadata.channelTitle}

            Rules for Educational Content:
            1. Must have clear educational purpose (teaching, explaining, or instructing)
            2. Must be structured like a lesson/tutorial
            3. No entertainment-only or vlog content
            4. No clickbait or misleading content
            5. Must be appropriate for students
            6. Should have academic or professional value

            Respond in JSON format only:
            {
              "isEducational": boolean,
              "confidence": number between 0-1,
              "subject": "subject area",
              "gradeLevel": "grade level or range",
              "reason": "brief explanation"
            }`
        }]
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': CLAUDE_API_KEY,
          'anthropic-version': '2023-06-01'
        }
      }
    );

    return JSON.parse(response.data.content[0].text);
  } catch (error) {
    console.error('Claude API Error:', error);
    return {
      isEducational: false,
      confidence: 0,
      subject: null,
      gradeLevel: null,
      reason: "Verification failed"
    };
  }
};

// Batch verification with rate limiting
export const batchVerifyContent = async (videos) => {
  try {
    const batchSize = 3; // Process in small batches to avoid rate limits
    const delay = 1000; // 1 second delay between batches
    const verifiedVideos = [];

    for (let i = 0; i < videos.length; i += batchSize) {
      const batch = videos.slice(i, i + batchSize);
      
      // Process batch sequentially to respect rate limits
      for (const video of batch) {
        try {
          const verificationResult = await verifyEducationalContent(video);
          if (verificationResult.isEducational) {
            verifiedVideos.push({
              ...video,
              verificationData: verificationResult
            });
          }
          await new Promise(resolve => setTimeout(resolve, delay));
        } catch (error) {
          console.error('Video verification failed:', error);
          continue;
        }
      }
    }

    return verifiedVideos;
  } catch (error) {
    console.error('Batch verification error:', error);
    return [];
  }
};