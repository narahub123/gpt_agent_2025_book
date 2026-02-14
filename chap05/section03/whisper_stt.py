import os
import torch
import pandas as pd
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


os.environ["PATH"] += os.pathsep + r"C:\Users\user\Downloads\ffmpeg-8.0.1-full_build-shared\bin"

