import subprocess
import sys
from pathlib import Path

def _call(name):
    path = Path(__file__).parent / "bin" / name
    sys.exit(subprocess.call([path, *sys.argv[1:]]))

def ph_align():
    _call("phonetisaurus-align")

def ph_arpa2wfst():
    _call("phonetisaurus-arpa2wfst")

def ph_g2pfst():
    _call("phonetisaurus-g2pfst")

def ph_g2prnn():
    _call("phonetisaurus-g2prnn")

def rnnlm():
    _call("rnnlm")

def estimate_ngram():
    _call("estimate-ngram")

def evaluate_ngram():
    _call("evaluate-ngram")

def interpolate_ngram():
    _call("interpolate-ngram")
