{\rtf1\ansi\ansicpg950\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import numpy as np\
from fgoc_orbitfit import fgoc_orbitfit\
\
MU = 398600.4418\
\
states = []\
times = []\
t0 = 0.0\
for k in range(4):\
    # Inject a stronger inconsistency to mimic focal instability\
    r = np.array([7000.0 + 25.0*k, 80.0*k, 10.0*k])\
    v = np.array([0.2*k, 7.5 - 0.25*k, 0.08*k])\
    states.append((r, v))\
    times.append(t0 + 60.0*k)\
\
flag, S, P, diag = fgoc_orbitfit(states, mu=MU, times=times, flag_threshold=0.5)\
print("Anomalous orbit-fit mode")\
print("flag:", flag, "S:", S, "P:", P)\
print("FDR:", diag["FDR"], "FSBI:", diag["FSBI"])\
print("term_sep:", diag["term_sep"], "term_cm:", diag["term_cm"])\
}
