import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _image_component_streamlit = components.declare_component(
       
        "image_component_streamlit",

        url="http://localhost:3001",
    )
else:
   
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _image_component_streamlit = components.declare_component("image_component_streamlit", path=build_dir)

def image_component_streamlit(data=None, styles=None, hideToolTip=None, key=None, default=None):
   
    component_value = _image_component_streamlit(data=data, styles=styles, hideToolTip=hideToolTip, key=key, default=default)

    return component_value

if not _RELEASE:
    import streamlit as st

    heroes = [
    {
      "id": 1,
      "heroName": "Miya",
      "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
      "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
    },
    {
      "id": 2,
      "heroName": "Miya",
      "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
      "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
    },
    {
      "id": 3,
      "heroName": "Miya",
      "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
      "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
    }
  ]
    image_component_streamlit(data=heroes)