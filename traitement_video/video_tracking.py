from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.fx.all import scroll
from moviepy.video.tools.tracking import manual_tracking
from moviepy.video.io.VideoFileClip import VideoFileClip

import matplotlib.pyplot as plt

clip = VideoFileClip("20220211_175425.mp4")
clip = clip.subclip(6.5, 8.5)
 



(w, h) = clip.size

# cropping = manual_tracking(clip, t1=0, t2=1, fps=2,nobjects=1, savefile="cropping.txt")

from moviepy.video.tools.tracking import Trajectory
cropping= Trajectory.load_list("cropping.txt")[0]
croppingwidth=cropping.xx[1]-cropping.xx[0]
croppingx=(cropping.xx[1]+cropping.xx[0])/2

croppingy=(cropping.yy[1]+cropping.yy[0])/2
croppingheight=cropping.yy[1]-cropping.yy[0]


cropped_clip = crop(clip, width=croppingwidth, height=h/2, x_center=croppingx, y_center=croppingy)


# speed=(traj.xx[-1]-traj.xx[0])/traj.tt[-1]
# new_clip = scroll(cropped_clip, w=clip.w//20, h=clip.h//20  , x_speed=speed,x_start=traj.xx[0], y_start=traj.yy[0])

# track = manual_tracking(cropped_clip, t1=0, t2=4, fps=15,nobjects=1, savefile="tracking2.txt")




tracking= Trajectory.load_list("tracking2.txt")[0]
plt.plot(tracking.tt,tracking.yy)

# cropped_clip.write_videofile('goutte.mp4')




