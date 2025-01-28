from dataclasses import dataclass
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import random
from datetime import timedelta
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import vlc
from pytube import YouTube
import os
from datetime import datetime, timedelta
import json


class InteractionLogger:
    """
    Handles logging of all user interactions with the video player.
    Maintains a chronological record of events and their timestamps.
    """
    def __init__(self):
        self.interactions = []
        self.start_time = datetime.now()

    def log_interaction(self, action, video_time):
        """Log a single interaction with timestamp"""
        interaction = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'video_time': str(timedelta(milliseconds=video_time)),
            'action': action
        }
        self.interactions.append(interaction)

    def generate_summary(self):
        """Create a detailed summary of all interactions"""
        summary = "\nVIDEO INTERACTION SUMMARY\n"
        summary += "=" * 50 + "\n"
        
        # Group interactions by type
        action_groups = {}
        for interaction in self.interactions:
            action = interaction['action']
            if action not in action_groups:
                action_groups[action] = []
            action_groups[action].append(interaction)

        # Generate summary statistics
        total_pauses = len(action_groups.get('pause', []))
        total_seeks = len(action_groups.get('seek', []))
        
        summary += f"\nTotal Viewing Session: {datetime.now() - self.start_time}\n"
        summary += f"Total Pauses: {total_pauses}\n"
        summary += f"Total Seeks: {total_seeks}\n\n"
        
        # Detailed chronological log
        summary += "Chronological Interaction Log:\n"
        summary += "-" * 50 + "\n"
        for interaction in self.interactions:
            summary += f"[{interaction['timestamp']}] "
            summary += f"At video time {interaction['video_time']}: "
            summary += f"{interaction['action']}\n"

        return summary

class VideoPlayer:
    """
    Custom video player with interaction tracking capabilities.
    Provides a user-friendly interface for video playback and monitors all interactions.
    """
    def __init__(self, video_path, video_title):
        self.window = ctk.CTk()
        self.window.title(f"CLIP Learning System - {video_title}")
        self.window.geometry("800x600")
        
        # Initialize VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)
        
        # Initialize interaction logger
        self.logger = InteractionLogger()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create and arrange UI elements"""
        # Video frame
        self.video_frame = ctk.CTkFrame(self.window)
        self.video_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Control frame
        self.control_frame = ctk.CTkFrame(self.window)
        self.control_frame.pack(fill='x', padx=10, pady=5)
        
        # Progress bar
        self.progress = ttk.Scale(
            self.control_frame,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.on_progress_change
        )
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # Control buttons
        self.setup_control_buttons()
        
        # Bind video frame to player
        self.player.set_hwnd(self.video_frame.winfo_id())
        
    def setup_control_buttons(self):
        """Create playback control buttons"""
        button_frame = ctk.CTkFrame(self.control_frame)
        button_frame.pack(pady=5)
        
        # Play/Pause button
        self.play_button = ctk.CTkButton(
            button_frame,
            text="Play",
            command=self.toggle_play
        )
        self.play_button.pack(side='left', padx=5)
        
        # Backward button (10 seconds)
        self.back_button = ctk.CTkButton(
            button_frame,
            text="◄◄ 10s",
            command=lambda: self.seek_relative(-10000)
        )
        self.back_button.pack(side='left', padx=5)
        
        # Forward button (10 seconds)
        self.forward_button = ctk.CTkButton(
            button_frame,
            text="10s ►►",
            command=lambda: self.seek_relative(10000)
        )
        self.forward_button.pack(side='left', padx=5)
        
    def toggle_play(self):
        """Handle play/pause functionality"""
        if self.player.is_playing():
            self.player.pause()
            self.play_button.configure(text="Play")
            self.logger.log_interaction('pause', self.player.get_time())
        else:
            self.player.play()
            self.play_button.configure(text="Pause")
            self.logger.log_interaction('play', self.player.get_time())
            
    def seek_relative(self, offset):
        """Handle seeking forward or backward"""
        current_time = self.player.get_time()
        new_time = max(0, current_time + offset)
        self.player.set_time(int(new_time))
        self.logger.log_interaction(
            f"seek {'forward' if offset > 0 else 'backward'}",
            new_time
        )
        
    def on_progress_change(self, value):
        """Handle manual seeking through progress bar"""
        value = float(value)
        length = self.player.get_length()
        target_time = int((value / 100) * length)
        self.player.set_time(target_time)
        self.logger.log_interaction('seek', target_time)
        
    def update_progress(self):
        """Update progress bar position"""
        if self.player.is_playing():
            length = self.player.get_length()
            if length > 0:
                current_time = self.player.get_time()
                progress = (current_time / length) * 100
                self.progress.set(progress)
        self.window.after(1000, self.update_progress)
        
    def start(self):
        """Start the video player"""
        self.player.play()
        self.update_progress()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
        
    def on_closing(self):
        """Handle window closing and generate interaction summary"""
        self.player.stop()
        print(self.logger.generate_summary())
        self.window.destroy()

def download_youtube_video(youtube_id: str, output_path: str = "videos") -> str:
    """
    Download YouTube video and return the local file path.
    Includes progress feedback for better user experience.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Initialize YouTube object
        yt = YouTube(f'https://www.youtube.com/watch?v={youtube_id}')
        
        # Get the highest resolution stream
        video = yt.streams.get_highest_resolution()
        
        # Generate output filename
        output_file = os.path.join(output_path, f"{youtube_id}.mp4")
        
        # Download if not already present
        if not os.path.exists(output_file):
            print("\nDownloading video...")
            video.download(output_path, filename=f"{youtube_id}.mp4")
            print("Download completed!")
        else:
            print("\nVideo already downloaded, using cached version.")
            
        return output_file
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def process_video_with_player(video: Video):
    """Process video and launch the video player"""
    try:
        # First download the video
        video_path = download_youtube_video(video.youtube_id)
        
        if video_path and os.path.exists(video_path):
            # Launch video player
            print("\nLaunching video player...")
            player = VideoPlayer(video_path, video.title)
            player.start()
            
        else:
            print("Error: Could not prepare video for playback")
            
    except Exception as e:
        print(f"Error processing video: {e}")


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
    
    # Process video segments and show analysis
    transcript_segments, topic_segments, cognitive_segments = analyze_video(
        selected_video.youtube_id, 
        selected_video.subject
    )
    
    if transcript_segments and topic_segments and cognitive_segments:
        display_analysis(transcript_segments, topic_segments, cognitive_segments)
        
        # Launch video player after showing analysis
        process_video_with_player(selected_video)
    else:
        print("Error: Could not process video segments")

if __name__ == "__main__":
    main()