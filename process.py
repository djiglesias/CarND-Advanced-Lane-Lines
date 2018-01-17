from moviepy.editor import VideoFileClip
from main.lane import Lane

lane = Lane()
file = './videos/project_video.mp4'
filename = './videos/test_video.mp4'
clips = VideoFileClip(file)
video = clips.fl_image(lane.process)
video.write_videofile(filename, audio=False)