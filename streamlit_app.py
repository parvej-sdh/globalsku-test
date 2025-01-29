import streamlit as st
import cv2
import tempfile
import os
from pathlib import Path
import shutil
import subprocess
from utils import detect_objects_in_frame, generate_listing, upload_audio_transcription, get_products

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
    st.title("GlobalSKU: Video Listing")
    
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
        
        if st.button("Get Listing"):
            with st.spinner('Converting video to frames...'):
                st.write(f"Processing video: {uploaded_file.name}")
                # st.write(f"Temporary file path: {tfile.name}")
                
                # Verify if video can be opened
                test_video = cv2.VideoCapture(tfile.name)
                if not test_video.isOpened():
                    st.error("Error: Could not open video file")
                    test_video.release()
                else:
                    test_video.release()
                    num_frames = extract_frames(tfile.name, output_dir)
                    st.success(f'Successfully extracted frames!')
                    
                    # Display some extracted frames
                frames = [str(Path(output_dir) / frame_file) for frame_file in os.listdir(output_dir)[:2]]
                st.subheader("Preview of Extracted Frames")
                cols = st.columns(len(frames))
                for idx, frame_file in enumerate(frames):
                    # frame_path = os.path.join(output_dir, frame_file)
                    cols[idx].image(frame_file, caption=f"Frame {idx+1}")

            with st.spinner('Extracting audio...'):
                
                audio_path = extract_audio(Path(tfile.name))
                st.subheader("Preview of Extracted audio")
                st.audio(audio_path)

            with st.spinner('Detecting products...'):
                try:
                    trans = upload_audio_transcription(audio_path)

                    query = get_products(trans["transcription"])["product_names"]
                    query = ", ".join(query)
                    # query = "katana, sword"
                    # frames = [str(Path(output_dir) / frame_file) for frame_file in os.listdir(output_dir)[:1]]
                    dets = [detect_objects_in_frame(frame_file, query) for frame_file in frames]
                    st.success(f'Successfully detected products!')
                    st.subheader("Preview of Detected Products")
                    cols = st.columns(len(frames))
                    detections = [det["detections"] for det in dets]
                    for idx, (frame, det) in enumerate(zip(frames, detections)):
                        # frame_path = os.path.join(output_dir, frame_file)
                        cols[idx].image(frame, caption=f'Product: {det[0]["class_name"].title()} | Confidence: {det[0]["confidence"]*100:.2f}%')

                    dets = str(dets)

                except Exception as e:
                    st.error(f"Could not detect products: {e}")
                    return


            # st.write(dets)

            with st.spinner('Generating Listing...'):
                listing = generate_listing(trans["transcription"], dets)

                # Extract product details
                product = listing["product_listing"]
                st.success(f'Successfully generated listing!')
                # Streamlit UI
                st.title("Product Listing")

                # Loop through product details and display them

                for key, value in product.items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    st.markdown(f"**{key.capitalize()}:** {value}")

                
        
        # Clean up temporary file
        os.unlink(tfile.name)
        shutil.rmtree("extracted_frames")
        shutil.rmtree("extracted_audio")

if __name__ == "__main__":
    main()
    # os.rmdir("extracted_frames")
    # os.rmdir("extracted_audio")