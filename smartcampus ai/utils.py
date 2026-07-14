import streamlit as st
import os
from pathlib import Path
from PIL import Image, ImageDraw
import config

def load_css():
    """Loads assets/styles.css and injects it into the page."""
    css_path = config.CSS_PATH
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found.")

def gradient_title(title, subtitle=None):
    """Renders a beautiful gradient header using HTML."""
    st.markdown(f'<h1 class="gradient-header">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="gradient-subtitle">{subtitle}</p>', unsafe_allow_html=True)

def card(title, content, footer=None, border_color=None):
    """Helper to render a glassmorphism card using standard HTML."""
    border_style = f"border-left: 5px solid {border_color};" if border_color else ""
    footer_html = f'<div style="margin-top: 10px; font-size: 0.85rem; color: #64748b;">{footer}</div>' if footer else ""
    st.markdown(f'''
    <div class="glass-card" style="{border_style}">
        <div style="font-size: 0.95rem; font-weight: 600; color: #1e3c72; margin-bottom: 8px;">{title}</div>
        <div style="font-size: 1.8rem; font-weight: 700; font-family: Outfit, sans-serif;">{content}</div>
        {footer_html}
    </div>
    ''', unsafe_allow_html=True)

def alert(message, level="info"):
    """Displays a custom styled alert banner."""
    levels = {
        "success": "alert-success",
        "info": "alert-info",
        "warning": "alert-warning",
        "danger": "alert-danger"
    }
    class_name = levels.get(level, "alert-info")
    st.markdown(f'<div class="alert-banner {class_name}">{message}</div>', unsafe_allow_html=True)

def generate_default_assets():
    """Generates default images for logo and background texture using PIL if missing."""
    config.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    logo_path = config.LOGO_PATH
    if not logo_path.exists():
        # Create a beautiful 200x200 PNG logo with a smart hat/AI concept
        img = Image.new("RGBA", (200, 200), color=(30, 60, 114, 255))
        d = ImageDraw.Draw(img)
        # Outer ring
        d.ellipse([(15, 15), (185, 185)], outline=(30, 144, 255, 255), width=6)
        # Academic cap polygon
        d.polygon([(100, 55), (155, 90), (100, 125), (45, 90)], fill=(30, 144, 255, 255))
        # Cap stand
        d.rectangle([(92, 115), (108, 145)], fill=(255, 255, 255, 255))
        # Tassel
        d.line([(100, 90), (45, 90), (45, 130)], fill=(245, 158, 11, 255), width=4)
        img.save(logo_path, "PNG")
        
    bg_path = config.BACKGROUND_PATH
    if not bg_path.exists():
        # Create a subtle grid background image
        img = Image.new("RGB", (1200, 800), color=(248, 250, 252))
        d = ImageDraw.Draw(img)
        # Soft blue-grey grid lines
        for i in range(0, 1200, 60):
            d.line([(i, 0), (i, 800)], fill=(235, 241, 250), width=1)
        for j in range(0, 800, 60):
            d.line([(0, j), (1200, j)], fill=(235, 241, 250), width=1)
        img.save(bg_path, "JPEG")
