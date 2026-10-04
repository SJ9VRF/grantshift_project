from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import math

@dataclass
class CalibrationSummary:
    n: int
    accuracy: float
    precision: float
    recall: float
    f1: float
    cohen_kappa: float

def binary_calibration(reference: Iterable[bool], candidate: Iterable[bool]) -> CalibrationSummary:
    ref=list(reference); cand=list(candidate)
    if len(ref)!=len(cand) or not ref: raise ValueError("non-empty equal-length inputs required")
    tp=sum(r and c for r,c in zip(ref,cand)); tn=sum((not r) and (not c) for r,c in zip(ref,cand))
    fp=sum((not r) and c for r,c in zip(ref,cand)); fn=sum(r and (not c) for r,c in zip(ref,cand))
    n=len(ref); acc=(tp+tn)/n; prec=tp/(tp+fp) if tp+fp else 0.0; rec=tp/(tp+fn) if tp+fn else 0.0
    f1=2*prec*rec/(prec+rec) if prec+rec else 0.0
    p_yes_ref=(tp+fn)/n; p_yes_c=(tp+fp)/n; pe=p_yes_ref*p_yes_c+(1-p_yes_ref)*(1-p_yes_c)
    kappa=(acc-pe)/(1-pe) if pe<1 else 1.0
    return CalibrationSummary(n,acc,prec,rec,f1,kappa)
