from dataclasses import dataclass
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import random
from datetime import timedelta

# Define our basic Video class to store video information
@dataclass
class Video:
    title: str
    youtube_id: str
    subject: str
    grade: int
    description: str

# Our video database with two classes, two subjects, three videos each
VIDEOS_DB = {
    5: {  # Class 5
        "Math": [
            Video(
                "Basic Mathematics", 
                "AF31lWJJSgg",  # First provided video
                "Math", 
                5,
                "Learn fundamental mathematics concepts with detailed explanations"
            ),
            Video(
                "Number Operations", 
                "EXUr_VfIiSI",  # Second provided video
                "Math", 
                5,
                "Master basic number operations and calculations"
            ),
            Video(
                "Math Practice Problems", 
                "AF31lWJJSgg",  # Using first video again for demonstration
                "Math", 
                5,
                "Practice solving mathematical problems step by step"
            )
        ],
        "Science": [
            Video(
                "Introduction to Science", 
                "EXUr_VfIiSI",
                "Science", 
                5,
                "Basic introduction to scientific concepts"
            ),
            Video(
                "Natural Phenomena", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Understanding the world around us"
            ),
            Video(
                "Scientific Method", 
                "EXUr_VfIiSI",
                "Science", 
                5,
                "Learn how scientists solve problems"
            )
        ]
    },
    6: {  # Class 6
        "Math": [
            Video(
                "Advanced Mathematics", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "More complex mathematical concepts and applications"
            ),
            Video(
                "Problem Solving", 
                "EXUr_VfIiSI",
                "Math", 
                6,
                "Advanced problem-solving techniques"
            ),
            Video(
                "Mathematical Reasoning", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Develop logical thinking through mathematics"
            )
        ],
        "Science": [
            Video(
                "Scientific Principles", 
                "EXUr_VfIiSI",
                "Science", 
                6,
                "Advanced scientific concepts and theories"
            ),
            Video(
                "Experimental Science", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Learn about scientific experiments"
            ),
            Video(
                "Applied Science", 
                "EXUr_VfIiSI",
                "Science", 
                6,
                "Real-world applications of science"
            )
        ]
    }
}

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    return str(timedelta(seconds=int(seconds))).zfill(8)

def get_random_segment_duration() -> int:
    """Generate random segment duration between 30 and 120 seconds"""
    return random.randint(30, 120)

def get_topic_by_subject(subject: str) -> str:
    """Get a random topic based on subject"""
    topics = {
        "Math": [
            "Number Operations",
            "Problem Solving",
            "Logical Reasoning",
            "Pattern Recognition",
            "Mathematical Concepts",
            "Practical Applications"
        ],
        "Science": [
            "Scientific Principles",
            "Natural Phenomena",
            "Experimental Methods",
            "Scientific Reasoning",
            "Real-world Applications",
            "Data Analysis"
        ]
    }
    return random.choice(topics.get(subject, topics["Math"]))

def get_random_cognitive_types(count: int = 2) -> List[tuple]:
    """Get random cognitive abilities with descriptions"""
    cognitive_types = {
        "attention": "Ability to focus on specific details and maintain concentration",
        "memory": "Ability to retain and recall information effectively",
        "logic_and_reasoning": "Ability to analyze problems and think critically",
        "auditory_processing": "Ability to understand and process spoken information",
        "visual_processing": "Ability to interpret and understand visual information",
        "processing_speed": "Speed at which information is processed and understood"
    }
    return random.sample(list(cognitive_types.items()), count)

def analyze_video(youtube_id: str, subject: str):
    """
    Analyze video and generate three different analyses:
    1. Transcript with timestamps
    2. Topics with timestamps
    3. Cognitive abilities with timestamps
    """
    try:
        # Get the transcript
        print("\nFetching video transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
        total_duration = transcript[-1]['start'] + transcript[-1]['duration']
        
        # Initialize our analysis segments
        current_time = 0
        transcript_segments = []
        topic_segments = []
        cognitive_segments = []
        
        print("Processing video segments...")
        while current_time < total_duration:
            # Get random duration for this segment
            segment_duration = get_random_segment_duration()
            end_time = min(current_time + segment_duration, total_duration)
            
            # Collect transcript text for this segment
            segment_text = ""
            for entry in transcript:
                if current_time <= entry['start'] < end_time:
                    segment_text += f"{entry['text']} "
            
            # Create timestamp string
            timestamp = f"{format_timestamp(current_time)} - {format_timestamp(end_time)}"
            
            # Add to our three analyses
            transcript_segments.append({
                'timestamp': timestamp,
                'text': segment_text.strip()
            })
            
            topic_segments.append({
                'timestamp': timestamp,
                'topic': get_topic_by_subject(subject)
            })
            
            cognitive_segments.append({
                'timestamp': timestamp,
                'cognitive_types': get_random_cognitive_types()
            })
            
            current_time = end_time
        
        return transcript_segments, topic_segments, cognitive_segments
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return [], [], []

def display_analysis(transcript_segments, topic_segments, cognitive_segments):
    """Display all three analyses in a clear, formatted way"""
    
    print("\n1. TRANSCRIPT ANALYSIS")
    print("=" * 80)
    for segment in transcript_segments:
        print(f"\nTimestamp: {segment['timestamp']}")
        print(f"Transcript: {segment['text']}")
        print("-" * 80)
    
    print("\n2. TOPIC ANALYSIS")
    print("=" * 80)
    for segment in topic_segments:
        print(f"\nTimestamp: {segment['timestamp']}")
        print(f"Topic: {segment['topic']}")
        print("-" * 80)
    
    print("\n3. COGNITIVE ABILITY ANALYSIS")
    print("=" * 80)
    for segment in cognitive_segments:
        print(f"\nTimestamp: {segment['timestamp']}")
        print("Cognitive Types:")
        for cog_type, description in segment['cognitive_types']:
            print(f"  - {cog_type.replace('_', ' ').title()}: {description}")
        print("-" * 80)

def main():
    """Main function to run the CLIP Learning System"""
    print("\n=== Welcome to CLIP Learning System ===")
    print("An intelligent video learning platform")
    
    # Get user's class
    while True:
        try:
            grade = int(input("\nEnter your class (5 or 6): "))
            if grade not in [5, 6]:
                print("Please enter either 5 or 6")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Display subjects
    print("\nAvailable subjects:")
    subjects = list(VIDEOS_DB[grade].keys())
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")
    
    # Get subject choice
    while True:
        try:
            subject_idx = int(input("\nSelect subject number: ")) - 1
            if subject_idx not in range(len(subjects)):
                print("Please enter a valid subject number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    selected_subject = subjects[subject_idx]
    
    # Display available videos
    print(f"\nAvailable {selected_subject} videos:")
    videos = VIDEOS_DB[grade][selected_subject]
    for i, video in enumerate(videos, 1):
        print(f"\n{i}. {video.title}")
        print(f"   Description: {video.description}")
    
    # Get video choice
    while True:
        try:
            video_idx = int(input("\nSelect video number: ")) - 1
            if video_idx not in range(len(videos)):
                print("Please enter a valid video number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    selected_video = videos[video_idx]
    
    print(f"\nProcessing video: {selected_video.title}")
    
    # Process and display video segments
    transcript_segments, topic_segments, cognitive_segments = analyze_video(
        selected_video.youtube_id, 
        selected_video.subject
    )
    
    if transcript_segments and topic_segments and cognitive_segments:
        display_analysis(transcript_segments, topic_segments, cognitive_segments)
    else:
        print("Error: Could not process video segments")
    
    print("\nThank you for using CLIP Learning System!")

if __name__ == "__main__":
    main()