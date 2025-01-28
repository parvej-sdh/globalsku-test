import streamlit as st
import cv2
import tempfile
import os
from pathlib import Path
import subprocess

AUDIO_DIR = Path("extracted_audio")
if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True)

def extract_frames(video_path, output_dir):
    # Read the video
    video = cv2.VideoCapture(video_path)
    
    # Get video properties
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    # Create progress bar
    progress_bar = st.progress(0)
    
    frame_count = 0
    saved_frames = 0
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
            
        # Save every 1 second (adjust fps to save more or fewer frames)
        if frame_count % fps == 0:
            frame_path = os.path.join(output_dir, f'frame_{saved_frames}.jpg')
            cv2.imwrite(frame_path, frame)
            saved_frames += 1
            
        # Update progress bar
        progress = int((frame_count / total_frames) * 100)
        progress_bar.progress(progress)
        
        frame_count += 1
    
    video.release()
    return saved_frames


def extract_audio(video_path: Path) -> Path:
    """
    Extracts audio from a video file and saves it as a .wav file.
    """
    audio_path = AUDIO_DIR / f"{video_path.stem}.wav"
    command = [
        "ffmpeg", "-i", str(video_path), "-q:a", "0", "-map", "a", str(audio_path), "-y"
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error extracting audio: {e}")

def main():
    st.title("Video to Frames Converter")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'])
    
    if uploaded_file is not None:
        # Create temporary file with proper extension
        file_extension = uploaded_file.name.split('.')[-1]
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}')
        tfile.write(uploaded_file.read())
        tfile.flush()
        
        # Create output directory
        output_dir = "extracted_frames"
        Path(output_dir).mkdir(exist_ok=True)
        
        if st.button("Extract Frames"):
            with st.spinner('Converting video to frames...'):
                st.write(f"Processing video: {uploaded_file.name}")
                st.write(f"Temporary file path: {tfile.name}")
                
                # Verify if video can be opened
                test_video = cv2.VideoCapture(tfile.name)
                if not test_video.isOpened():
                    st.error("Error: Could not open video file")
                    test_video.release()
                else:
                    test_video.release()
                    num_frames = extract_frames(tfile.name, output_dir)
                    st.success(f'Successfully extracted {num_frames} frames!')
                    
                    # Display some extracted frames
                    st.subheader("Preview of Extracted Frames")
                cols = st.columns(3)
                for idx, frame_file in enumerate(sorted(os.listdir(output_dir))[:3]):
                    frame_path = os.path.join(output_dir, frame_file)
                    cols[idx].image(frame_path, caption=f"Frame {idx+1}")

                audio = extract_audio(Path(tfile.name))
                st.audio(audio)
        
        # Clean up temporary file
        os.unlink(tfile.name)

if __name__ == "__main__":
    main()