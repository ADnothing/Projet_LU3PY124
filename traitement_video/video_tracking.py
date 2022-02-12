from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.fx.all import scroll
from moviepy.video.tools.tracking import manual_tracking
from moviepy.video.io.VideoFileClip import VideoFileClip

clip = VideoFileClip("Les marcheurs, gouttes et ondes.mp4")
clip = clip.subclip(17, 31)
 



 


(w, h) = clip.size
cropped_clip = crop(clip, width=w/2, height=h/2, x_center=w*3/4, y_center=h/2)

# trajectory = manual_tracking(cropped_clip, t1=0, t2=31-17, fps=1,nobjects=1, savefile="track.txt")
# ...
# LATER, IN ANOTHER SCRIPT, RECOVER THESE TRAJECTORIES
from moviepy.video.tools.tracking import Trajectory
traj= Trajectory.load_list('track.txt')[0]

speed=(traj.xx[-1]-traj.xx[0])/traj.tt[-1]
new_clip = scroll(cropped_clip, w=clip.w//20, h=clip.h//20  , x_speed=speed,x_start=traj.xx[0], y_start=traj.yy[0])




new_clip.write_videofile('goutte.mp4')




