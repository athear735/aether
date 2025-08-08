# 🚀 AETHER Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Proper File Structure**: Ensure the following files exist in your repo root

## Required Files

### 1. `streamlit_app.py` (Entry Point)
✅ Already created - This is the main entry point for Streamlit Cloud

### 2. `requirements.txt` or `requirements-streamlit.txt`
Choose one of these approaches:

**Option A: Use the lightweight requirements file**
```bash
# Rename to requirements.txt before deployment
mv requirements-streamlit.txt requirements.txt
```

**Option B: Keep both files and specify in Streamlit Cloud**
- Use `requirements-streamlit.txt` for cloud deployment
- Keep `requirements.txt` for local development

### 3. `packages.txt` (System Dependencies)
✅ Already created - Contains system packages needed for deployment

### 4. `.streamlit/config.toml` (Streamlit Configuration)
✅ Already exists - Contains theme and server settings

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit the new files**:
```bash
git add streamlit_app.py requirements-streamlit.txt packages.txt STREAMLIT_DEPLOYMENT.md
git add .streamlit/secrets.toml.example
git commit -m "Add Streamlit Cloud deployment configuration"
git push origin main
```

2. **Choose your requirements file**:
```bash
# If you want to use the lightweight version for deployment
cp requirements-streamlit.txt requirements.txt
git add requirements.txt
git commit -m "Use lightweight requirements for Streamlit Cloud"
git push
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account if not already connected
4. Select your repository: `AETHER`
5. Select branch: `main` (or your default branch)
6. Main file path: `streamlit_app.py`
7. Click "Deploy"

### Step 3: Configure Secrets

1. In Streamlit Cloud dashboard, go to your app settings
2. Click on "Secrets" in the left sidebar
3. Add your secrets in TOML format:

```toml
# Required
API_URL = "https://your-backend-api.com"  # Your deployed API endpoint

# Optional (if using OpenAI)
OPENAI_API_KEY = "sk-..."

# Add other secrets as needed
```

## Common Deployment Errors and Solutions

### Error 1: "ModuleNotFoundError"
**Cause**: Missing dependencies in requirements.txt
**Solution**: 
- Check the error message for the missing module
- Add it to `requirements-streamlit.txt`
- Commit and push the changes

### Error 2: "torch" installation fails
**Cause**: PyTorch is too heavy for free tier
**Solutions**:
1. Remove PyTorch completely if not needed
2. Use CPU-only version with proper index URL:
```txt
--find-links https://download.pytorch.org/whl/torch_stable.html
torch==2.0.1+cpu
```
3. Use API-based models instead (OpenAI, HuggingFace API)

### Error 3: "Memory limit exceeded"
**Cause**: App uses too much memory (free tier limit: 1GB)
**Solutions**:
- Remove heavy ML libraries
- Use API-based models instead of local models
- Reduce data processing in the app
- Cache results using `@st.cache_data`

### Error 4: "Cannot connect to API"
**Cause**: Backend API not accessible from Streamlit Cloud
**Solutions**:
1. Deploy your backend API separately (Render, Railway, Heroku)
2. Update `API_URL` in Streamlit secrets
3. Ensure CORS is enabled in your backend
4. Use HTTPS for production APIs

### Error 5: "App is over the resource limit"
**Cause**: Free tier limitations
**Solutions**:
- Reduce dependencies
- Optimize code
- Consider upgrading to a paid tier

## Optimization Tips

### 1. Minimize Dependencies
- Only include packages actually used in the web interface
- Use API calls instead of local model inference
- Remove development/testing packages

### 2. Use Caching
```python
@st.cache_data
def expensive_computation(param):
    # Your computation here
    return result

@st.cache_resource
def load_model():
    # Load model once
    return model
```

### 3. Optimize Imports
```python
# Instead of importing everything
# from transformers import *

# Import only what you need
from transformers import pipeline
```

### 4. Handle API Failures Gracefully
```python
try:
    response = call_api(endpoint)
except Exception as e:
    st.error("API temporarily unavailable")
    # Provide fallback behavior
```

## Backend Deployment Options

Since AETHER needs a backend API, consider these free/cheap options:

### 1. **Render** (Recommended)
- Free tier available
- Easy deployment from GitHub
- Automatic HTTPS
- Guide: Use existing `render.yaml`

### 2. **Railway**
- $5 free credit monthly
- Simple deployment
- Good for Python apps

### 3. **Google Cloud Run**
- Free tier available
- Scales to zero
- Pay per use

### 4. **Heroku** (Free tier discontinued)
- Now requires paid plan
- Still good option if budget allows

## Testing Locally Before Deployment

```bash
# Test with Streamlit
streamlit run streamlit_app.py

# Test with lightweight requirements
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

## Monitoring Your Deployment

1. **Check Logs**: In Streamlit Cloud dashboard
2. **Resource Usage**: Monitor memory and CPU
3. **Error Tracking**: Set up error notifications
4. **User Analytics**: Use Streamlit's built-in analytics

## Need Help?

- Check Streamlit Cloud [documentation](https://docs.streamlit.io/streamlit-cloud)
- Join Streamlit [community forum](https://discuss.streamlit.io)
- Review your app logs in the dashboard
- Ensure backend API is running and accessible

## Next Steps

1. Deploy backend API first
2. Get the API URL
3. Deploy Streamlit app
4. Configure secrets
5. Test the full application

---

**Remember**: The key to successful Streamlit Cloud deployment is keeping dependencies minimal and using external APIs for heavy computations.

© 2024 AlgoRythm Tech - AETHER Project
