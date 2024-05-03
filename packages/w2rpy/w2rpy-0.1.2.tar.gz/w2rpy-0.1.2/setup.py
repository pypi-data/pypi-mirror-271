# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:58:32 2024

@author: lrussell
"""

from distutils.core import setup

setup(
  name = 'w2rpy',         
  packages = ['w2rpy'],   
  version = '0.1.2',     
  license='MIT',        
  description = 'Water Resource Functions For Fluvial Systems',   
  author = 'Luke Russell',                   
  author_email = 'lrussell@wolfwaterresources.com',      
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
  install_requires=['pandas',
                    'numpy',
                    'shapely',
                    'geopandas',
                    'rasterio',
                    'pysheds',
                    'scipy'],
  )