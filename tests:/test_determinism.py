{\rtf1\ansi\ansicpg950\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import numpy as np\
from fgoc_orbitfit import fgoc_orbitfit\
\
def test_determinism_repeatability():\
    MU = 398600.4418\
    states = [\
        (np.array([7000., 0., 0.]), np.array([0., 7.5, 0.])),\
        (np.array([7002., 1., 0.]), np.array([0., 7.5, 0.])),\
        (np.array([7004., 2., 0.]), np.array([0., 7.5, 0.])),\
    ]\
    out1 = fgoc_orbitfit(states, mu=MU)\
    out2 = fgoc_orbitfit(states, mu=MU)\
    assert out1[0] == out2[0]\
    assert abs(out1[1] - out2[1]) < 1e-15\
    assert abs(out1[2] - out2[2]) < 1e-15\
}