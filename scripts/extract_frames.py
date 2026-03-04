import cv2
import sys
import os

def extract_frames(video_path, target_fps=15, max_width=1920, remove_bg=False):
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video.")
        sys.exit(1)

    if remove_bg:
        try:
            from rembg import remove
            print("Using rembg for background removal (may require downloading model on first run).")
        except ImportError:
            print("Error: rembg not installed. Run 'pip install rembg' or omit --remove-bg")
            sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Original Video: {fps:.2f} fps, {duration:.2f}s, {width}x{height}, {total_frames} frames")
    
    # Calculate intervals to match target fps
    skip = int(round(fps / target_fps)) if fps > target_fps else 1
    actual_fps = fps / skip
    
    # Scale width if it exceeds max_width while maintaining aspect ratio
    scale = max_width / width if width > max_width else 1.0
    out_w, out_h = int(width * scale), int(height * scale)
    
    os.makedirs('frames', exist_ok=True)
    
    count = 0
    saved_count = 0
    
    print(f"Extracting at ~{actual_fps:.2f} fps (saving every {skip} frames). Output: {out_w}x{out_h} (WebP quality 80)")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % skip == 0:
            if scale != 1.0:
                frame = cv2.resize(frame, (out_w, out_h), interpolation=cv2.INTER_AREA)
            
            if remove_bg:
                # rembg expects RGB inputs/outputs but with cv2 we must pass either RGB image or PIL.
                # It's easiest to process with remove() directly on the raw numpy array.
                from rembg import remove
                frame = remove(frame)  # Returns RGBA array

            output_path = f"frames/frame_{saved_count+1:04d}.webp"
            
            # Encode as WebP with 80% quality
            cv2.imwrite(output_path, frame, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
            saved_count += 1
            if saved_count % 10 == 0:
                print(f"Saved {saved_count} frames...")
                
        count += 1
        
    cap.release()
    print(f"Done! Saved {saved_count} frames in total to the 'frames/' directory.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <video_path> [target_fps] [--remove-bg]")
        sys.exit(1)
        
    video = sys.argv[1]
    
    remove_bg = "--remove-bg" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--remove-bg"]
    
    fps = int(args[1]) if len(args) > 1 else 15
    extract_frames(video, fps, remove_bg=remove_bg)
