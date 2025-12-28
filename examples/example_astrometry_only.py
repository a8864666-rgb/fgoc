{\rtf1\ansi\ansicpg950\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from fgoc import fgoc\
\
ra = [10.0, 10.002, 10.004]\
dec = [20.0, 20.001, 20.002]\
mjd = [60000.0, 60000.01, 60000.02]\
\
flag, score, axis, sign = fgoc(ra, dec, mjd)\
\
print("Astrometry-only")\
print("flag:", flag)\
print("score:", score)\
print("axis:", axis)\
print("sign:", sign)\
}
