"""
-------------------------------------------------
SegDB - Navigate the SegDB Segmentations,
        e.g., looking up SegDB ID's by a reference
        code or name.
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg
Email:  leonard.nuernberg@maastrichtuniversity.nl
-------------------------------------------------
"""

from typing import List, Optional
from ..classes.Segment import Segment
from ..classes.DB import db
import os, json

class Navigator:
  
  def __init__(self) -> None:
    pass
  
  def 