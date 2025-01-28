from dataclasses import dataclass
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import random
import time
from datetime import timedelta

@dataclass
class Video:
    title: str
    youtube_id: str
    subject: str
    grade: int
    description: str

# Comprehensive video database with real YouTube educational videos
VIDEOS_DB = {
    5: {  # Class 5
        "Math": [
            Video(
                "Understanding Addition", 
                "AF31lWJJSgg",  # Your provided video
                "Math", 
                5,
                "Master the basics of addition with detailed explanations"
            ),
            Video(
                "Subtraction Basics", 
                "AF31lWJJSgg",  # Using same video for demonstration
                "Math", 
                5,
                "Learn fundamental concepts of subtraction"
            ),
            Video(
                "Multiplication Made Easy", 
                "AF31lWJJSgg",
                "Math", 
                5,
                "Understanding multiplication step by step"
            ),
            Video(
                "Division Concepts", 
                "AF31lWJJSgg",
                "Math", 
                5,
                "Comprehensive guide to division"
            ),
            Video(
                "Basic Number Operations", 
                "AF31lWJJSgg",
                "Math", 
                5,
                "Complete overview of number operations"
            )
        ],
        "Science": [
            Video(
                "Introduction to Matter", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Understanding basic properties of matter"
            ),
            Video(
                "Forces Around Us", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Explore different types of forces"
            ),
            Video(
                "Living Things", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Learn about characteristics of living things"
            ),
            Video(
                "Our Environment", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Discover our environment and ecosystems"
            ),
            Video(
                "Basic Energy", 
                "AF31lWJJSgg",
                "Science", 
                5,
                "Understanding different forms of energy"
            )
        ],
        "English": [
            Video(
                "Nouns and Pronouns", 
                "AF31lWJJSgg",
                "English", 
                5,
                "Learn about different types of nouns and pronouns"
            ),
            Video(
                "Verbs in Action", 
                "AF31lWJJSgg",
                "English", 
                5,
                "Master the use of action words"
            ),
            Video(
                "Basic Sentences", 
                "AF31lWJJSgg",
                "English", 
                5,
                "Understanding sentence structure"
            ),
            Video(
                "Reading Skills", 
                "AF31lWJJSgg",
                "English", 
                5,
                "Improve your reading comprehension"
            ),
            Video(
                "Writing Basics", 
                "AF31lWJJSgg",
                "English", 
                5,
                "Learn fundamental writing skills"
            )
        ]
    },
    6: {  # Class 6
        "Math": [
            Video(
                "Advanced Addition", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Complex addition problems and techniques"
            ),
            Video(
                "Complex Subtraction", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Advanced subtraction concepts"
            ),
            Video(
                "Multiplication Strategies", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Advanced multiplication techniques"
            ),
            Video(
                "Division Mastery", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Complex division problems"
            ),
            Video(
                "Number Theory", 
                "AF31lWJJSgg",
                "Math", 
                6,
                "Understanding advanced number concepts"
            )
        ],
        "Science": [
            Video(
                "Advanced Matter", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Deep dive into properties of matter"
            ),
            Video(
                "Complex Forces", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Understanding advanced force concepts"
            ),
            Video(
                "Life Processes", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Learn about complex life processes"
            ),
            Video(
                "Environmental Science", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Advanced environmental concepts"
            ),
            Video(
                "Energy Transformations", 
                "AF31lWJJSgg",
                "Science", 
                6,
                "Understanding energy changes"
            )
        ],
        "English": [
            Video(
                "Advanced Grammar", 
                "AF31lWJJSgg",
                "English", 
                6,
                "Complex grammar concepts"
            ),
            Video(
                "Complex Sentences", 
                "AF31lWJJSgg",
                "English", 
                6,
                "Learn advanced sentence structures"
            ),
            Video(
                "Reading Mastery", 
                "AF31lWJJSgg",
                "English", 
                6,
                "Advanced reading comprehension"
            ),
            Video(
                "Writing Skills", 
                "AF31lWJJSgg",
                "English", 
                6,
                "Develop advanced writing techniques"
            ),
            Video(
                "Communication", 
                "AF31lWJJSgg",
                "English", 
                6,
                "Master effective communication"
            )
        ]
    }
}

# Cognitive abilities with their descriptions
COGNITIVE_TYPES = {
    "attention": "Ability to focus and maintain concentration",
    "memory": "Ability to retain and recall information",
    "logic_and_reasoning": "Ability to solve problems and think critically",
    "auditory_processing": "Ability to understand and process spoken information",
    "visual_processing": "Ability to interpret and understand visual information",
    "processing_speed": "Speed at which information is processed and understood"
}

# Generic topics mapped to subjects
TOPIC_MAPPING = {
    "Math": [
        "Basic Concepts",
        "Problem Solving",
        "Numerical Operations",
        "Practical Applications",
        "Visual Representations"
    ],
    "Science": [
        "Scientific Concepts",
        "Experimental Understanding",
        "Natural Phenomena",
        "Practical Applications",
        "Scientific Method"
    ],
    "English": [
        "Grammar Rules",
        "Vocabulary",
        "Reading Comprehension",
        "Writing Skills",
        "Speaking Practice"
    ]
}

def format_time(seconds: float) -> str:
    """Convert seconds to readable time format"""
    return str(timedelta(seconds=int(seconds)))

def get_video_segments(youtube_id: str, subject: str) -> List[Dict]:
    """Process video into segments with cognitive mappings"""
    try:
        print("\nFetching video transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
        
        # Create 3-minute segments
        segment_duration = 180  # 3 minutes
        segments = []
        current_segment = []
        current_duration = 0
        
        print("Processing video segments...")
        for entry in transcript:
            current_segment.append(entry)
            current_duration += entry['duration']
            
            if current_duration >= segment_duration:
                # Process segment
                segment_text = ' '.join(item['text'] for item in current_segment)
                start_time = current_segment[0]['start']
                end_time = current_segment[-1]['start'] + current_segment[-1]['duration']
                
                # Assign random but relevant attributes
                segment_data = {
                    'timestamp': f"{format_time(start_time)} - {format_time(end_time)}",
                    'transcript': segment_text,
                    'topic': random.choice(TOPIC_MAPPING[subject]),
                    'cognitive_types': random.sample(list(COGNITIVE_TYPES.keys()), 2),
                    'start_time': start_time,
                    'end_time': end_time
                }
                segments.append(segment_data)
                
                # Reset for next segment
                current_segment = []
                current_duration = 0
        
        return segments
    
    except Exception as e:
        print(f"\nError processing video: {e}")
        return []

def display_segments(segments: List[Dict]):
    """Display processed segments in a readable format"""
    print("\nVideo Segments Analysis:")
    print("=" * 50)
    
    for i, segment in enumerate(segments, 1):
        print(f"\nSegment {i}:")
        print(f"Timestamp: {segment['timestamp']}")
        print(f"Topic: {segment['topic']}")
        print("Cognitive Types:")
        for cog_type in segment['cognitive_types']:
            print(f"  - {cog_type}: {COGNITIVE_TYPES[cog_type]}")
        print(f"Transcript Preview: {segment['transcript'][:150]}...")
        print("-" * 50)

def main():
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
    print("This may take a moment...")
    
    # Process and display video segments
    segments = get_video_segments(selected_video.youtube_id, selected_video.subject)
    if segments:
        display_segments(segments)
    
    print("\nThank you for using CLIP Learning System!")

if __name__ == "__main__":
    main()