# Audio-visual representational similarity analysis (RSA) project for Cognitive Robotics Master's Dissertation 

## Experiment 
- [Meadows: Multiple arrangements tasks](https://meadows-research.com/experiments/Audio-Visual_RSA/)

## Set up ## 
**Setting up the environment:**

```
cd Audio-visual_similarity 
# CREATE VIRTUAL ENVIRONMENT
# virtualenv venv -p python3
source venv/bin/activate
```
- The data are presumed to be at ~/Audio-visual_similarity
- Install dependencies: pip install -r requirements.txt

**Run**
```
python3 mp4.py #download youtube playlist and individual videos 
python3 process_mp4.py #process videos - cut, crop, scale, normalise sound, extract audio, extract image and save
```

**Data and AVIMA_analysis** 
This is the data collected from the 2020 participants and the analysis of this data. Stimuli used for this research can be found [here](https://info.com)

**AVIMA_analysis2** 
This is the data and analysis of data collected in 2021 using the shown stimuli 
