import pandas
from os.path import join, expanduser, isfile, isdir
import subprocess, os, glob, time, shutil
from subprocess import STDOUT
from ww import f 
from datetime import timedelta
from tempfile import NamedTemporaryFile
from ffmpeg_normalize import FFmpegNormalize

# seperate audio and video in folder 'stimuli'
sourcedir = join(expanduser('~/Audio-visual_similarity/source_videos'))
outdir = expanduser('~/Audio-visual_similarity/processed')
videodir = join(outdir, 'video')
interdir = join(outdir, 'intermediate')
audiodir = join(outdir, 'audio')
imgdir = join(outdir, 'image')
for subdir in (audiodir, imgdir, videodir, interdir):
    if not isdir(subdir):
        os.mkdir(subdir)

# crop mp4 videos
dur = timedelta(seconds=3)
table = pandas.read_csv('stimuli.csv')
nvideos = len(table.index)
for v, (_, video) in enumerate(table.iterrows()):
    vidnum = v + 1
    print(f('{video.stimulus_name} {vidnum}/{nvideos}'))

    # check if you have the file locally
    fpath = join(sourcedir, video.original_filename)
    assert isfile(fpath)

    print('\tcutting video')
    tstart = timedelta(seconds=video.start_time)
    f_vid_cut = join(interdir, video.stimulus_name + '_cut.mp4')
    cmd = f('ffmpeg -y -ss {tstart} -i "{fpath}" -t {dur} -c copy {f_vid_cut}')
    out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

    print('\tnormalizing loudness')
    f_vid_norm = join(interdir, video.stimulus_name + '_normalized.mp4')
    ffmpeg_normalize = FFmpegNormalize(
        audio_codec='aac',
        video_codec='libx264',
    )
    ffmpeg_normalize.add_media_file(f_vid_cut, f_vid_norm)
    ffmpeg_normalize.run_normalization()

    print('\tcropping video')
    f_vid_cropped = join(interdir, video.stimulus_name + '_cropped.mp4')
    half_size = int(video.crop_size / 2)
    x = video.centre_x - half_size
    y = video.centre_y - half_size
    w, h = video.crop_size, video.crop_size
    cmd = f('ffmpeg -y -i {f_vid_norm} -filter:v "crop={w}:{h}:{x}:{y}" {f_vid_cropped}')
    out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

    print('\tscaling video')
    f_vid_scaled = join(interdir, video.stimulus_name + '_scaled.mp4')
    cmd = f('ffmpeg -y -i {f_vid_cropped} -vf scale=256:256 {f_vid_scaled}') 
    out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

    print('\tsaving final video')
    f_vid = join(videodir, video.stimulus_name + '.mp4')
    shutil.copyfile(f_vid_scaled, f_vid)

    print('\textracting audio')
    f_aud = join(audiodir, video.stimulus_name + '.wav')
    cmd = f('ffmpeg -y -i {f_vid} -ab 160k -ac 2 -ar 44100 -vn {f_aud}')
    out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

    print('\textracting image')
    tstill = timedelta(seconds=video.tstill)-tstart
    f_img = join(imgdir, video.stimulus_name + '.png')
    cmd = f('ffmpeg -y -i {f_vid} -ss {tstill} -vframes 1 {f_img}')
    out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

print('combining videos')
f_vidlist = join(outdir, 'videos.txt')
with open(f_vidlist, mode='w') as input_file:
    video_list = glob.glob(join(videodir, '*.mp4'))
    input_file.writelines(["file '{}'\n".format(v) for v in video_list])

f_com = join(outdir, 'combined.mp4')
cmd = f('ffmpeg -f concat -safe 0 -i {f_vidlist} -c copy {f_com}')
out = subprocess.check_output(cmd, shell=True, stderr=STDOUT)

print('Done')
