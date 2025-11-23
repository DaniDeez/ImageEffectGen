# 🌐 Web Demo Deployment Guide

This guide shows you how to deploy the Jigsaw Folk Art Filter as a web app on Streamlit Cloud (100% FREE!).

## 🚀 Quick Deploy to Streamlit Cloud (5 minutes!)

### Prerequisites
- GitHub account
- This repository pushed to GitHub

### Step-by-Step Instructions

#### 1. Push Your Code to GitHub

Make sure your repository is pushed to GitHub:
```bash
git push origin main
```

#### 2. Go to Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Sign in"** with your GitHub account
3. Authorize Streamlit to access your repositories

#### 3. Deploy Your App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository:** `DaniDeez/ImageEffectGen` (or your fork)
   - **Branch:** `main` (or your working branch)
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose a custom URL like `imageeffectgen` (optional)

3. Click **"Deploy!"**

#### 4. Wait for Deployment

- Streamlit Cloud will install dependencies (takes 2-5 minutes)
- Watch the deployment logs to see progress
- Once complete, your app will be live! 🎉

#### 5. Share Your App

Your app will be live at:
```
https://[your-app-name].streamlit.app
```

Share this URL with anyone - no installation required!

---

## 📋 Files Needed for Deployment

These files are already included in the repository:

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `packages.txt` | System-level dependencies (for OpenCV) |
| `.streamlit/config.toml` | Streamlit configuration |
| `src/` | Source code directory |

---

## ⚙️ Configuration

### Streamlit Cloud Settings

The app is configured via `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
maxUploadSize = 10  # Maximum upload size in MB
```

### Resource Limits

Streamlit Cloud free tier includes:
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited public apps
- ✅ Custom subdomain

**Note:** Large images or many concurrent users may hit limits. Consider:
- Resizing large images automatically
- Using smaller `piece_size` for faster processing
- Upgrading to Streamlit Cloud paid tier for production use

---

## 🔧 Troubleshooting

### Deployment Fails

**Problem:** Deployment logs show errors

**Solutions:**
1. Check that all files are committed and pushed
2. Verify `requirements.txt` has all dependencies
3. Check deployment logs for specific error messages
4. Make sure `streamlit_app.py` is in the root directory

### App is Slow

**Problem:** Image processing takes too long

**Solutions:**
1. Reduce default `piece_size` (faster processing)
2. Add image size limits in the code
3. Consider paid Streamlit Cloud tier for more resources

### OpenCV Errors

**Problem:** `ImportError: libGL.so.1` or similar

**Solution:** `packages.txt` file includes required system dependencies:
```
libgl1-mesa-glx
libglib2.0-0
```

Make sure this file is in your repository root.

### Upload Size Limit

**Problem:** "File size exceeds maximum"

**Solution:** Increase in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 20  # Increase to 20MB
```

---

## 🎨 Customization

### Change App Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
secondaryBackgroundColor = "#YOUR_COLOR"
textColor = "#YOUR_COLOR"
```

### Modify UI

Edit `streamlit_app.py`:
- Change layout in the main() function
- Add/remove parameters in sidebar
- Customize text and messages
- Add more presets

### Add Features

Some ideas:
- Batch processing multiple images
- Comparison slider (before/after)
- Gallery of processed images
- User accounts and history
- Export to different formats

---

## 🔄 Updating Your Deployed App

Streamlit Cloud auto-deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main
```

Your app will automatically redeploy! (takes 2-5 minutes)

---

## 🌍 Alternative Deployment Options

### Hugging Face Spaces

1. Create account on [huggingface.co](https://huggingface.co)
2. Create a new Space
3. Choose "Streamlit" as SDK
4. Upload files or connect GitHub repo
5. App deploys automatically

### Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add Procfile
echo "web: streamlit run streamlit_app.py" > Procfile

# Deploy
git push heroku main
```

### AWS/GCP/Azure

For production deployments:
- Use Docker container
- Deploy to cloud VM
- Use managed services (AWS Elastic Beanstalk, GCP App Engine)
- See cloud provider documentation

---

## 📊 Monitoring

### Streamlit Cloud Dashboard

Access at [share.streamlit.io](https://share.streamlit.io):
- View app analytics
- Check resource usage
- See deployment logs
- Manage app settings
- View error logs

### Usage Metrics

Monitor:
- Number of visitors
- Resource consumption
- Error rates
- Response times

---

## 💰 Costs

### Free Tier (Streamlit Cloud)

✅ **100% FREE** for public apps:
- Unlimited public apps
- 1 GB RAM per app
- Community support
- Custom subdomain

### Paid Plans

For production/private apps:
- **Starter:** $20/month
  - Private apps
  - More resources
  - Priority support

- **Team:** $250/month
  - Team collaboration
  - Even more resources
  - SLA support

---

## 🎯 Best Practices

1. **Optimize Performance**
   - Cache expensive operations with `@st.cache_data`
   - Limit image sizes
   - Use efficient algorithms

2. **User Experience**
   - Show progress indicators
   - Provide clear error messages
   - Include help text
   - Add examples

3. **Security**
   - Validate user inputs
   - Sanitize file uploads
   - Set size limits
   - Handle errors gracefully

4. **Maintenance**
   - Keep dependencies updated
   - Monitor error logs
   - Gather user feedback
   - Regular updates

---

## ✅ Deployment Checklist

Before deploying:

- [ ] All code committed and pushed to GitHub
- [ ] `streamlit_app.py` in repository root
- [ ] `requirements.txt` with all dependencies
- [ ] `packages.txt` with system dependencies
- [ ] `.streamlit/config.toml` configured
- [ ] Tested locally with `streamlit run streamlit_app.py`
- [ ] Repository is public (for free hosting)
- [ ] No sensitive data in code

---

## 🆘 Getting Help

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** Report bugs in this repository
- **Stack Overflow:** Tag with `streamlit`

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live web app accessible from anywhere
- ✅ No installation required for users
- ✅ Automatic updates when you push changes
- ✅ Free hosting for public apps
- ✅ Shareable URL

**Example URL:** `https://imageeffectgen.streamlit.app`

Share it with the world! 🌍
