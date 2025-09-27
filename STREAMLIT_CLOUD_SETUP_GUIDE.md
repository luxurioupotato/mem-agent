# 🚀 Streamlit Cloud Setup Guide

## 📋 **YOU NEED TO CREATE A STREAMLIT CLOUD APP FIRST!**

You have the dashboard files ready, but you haven't created a Streamlit Cloud app yet. Here's how to do it:

---

## 🎯 **STEP-BY-STEP STREAMLIT CLOUD SETUP**

### **Step 1: Go to Streamlit Cloud**
1. Visit [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. If you don't have a GitHub account, create one first

### **Step 2: Create New App**
1. Click **"New app"** button
2. You'll see a form to configure your app

### **Step 3: Configure Your App**
Fill out the form with these details:

**Repository:** `your-username/mem-agent` (or your actual repo name)
**Branch:** `main` (or `master`)
**Main file path:** `dashboard/app.py`
**App URL:** `mem-agent-dashboard` (or choose your own)

### **Step 4: Set Environment Variables**
Before deploying, you need to set the API URL:

1. In the app configuration, find **"Secrets"** section
2. Add this secret:
   ```toml
   API_BASE_URL = "https://saturday-distant-motors-clone.trycloudflare.com"
   ```

### **Step 5: Deploy**
1. Click **"Deploy!"**
2. Wait for the deployment to complete (2-5 minutes)
3. Your dashboard will be live at: `https://mem-agent-dashboard.streamlit.app`

---

## 🔧 **ALTERNATIVE: LOCAL STREAMLIT DASHBOARD**

If you want to test locally first:

### **Run Dashboard Locally**
```bash
# Navigate to your MEM_AGENT directory
cd E:\MEM_AGENT

# Set environment variable
$env:API_BASE_URL = "https://saturday-distant-motors-clone.trycloudflare.com"

# Run Streamlit
streamlit run dashboard/app.py
```

### **Access Local Dashboard**
- Open your browser
- Go to: `http://localhost:8501`
- Test the dashboard functionality

---

## 📋 **REQUIREMENTS FOR STREAMLIT CLOUD**

Make sure your `requirements.txt` includes:
```
streamlit
requests
```

If you don't have a `requirements.txt`, I can create one for you.

---

## 🚨 **TROUBLESHOOTING**

### **If you don't have a GitHub repository:**
1. Create a GitHub account
2. Create a new repository called `mem-agent`
3. Upload your MEM_AGENT files to the repository
4. Then follow the Streamlit Cloud setup

### **If deployment fails:**
1. Check that `dashboard/app.py` exists
2. Verify `requirements.txt` is in the root directory
3. Make sure the repository is public (free Streamlit Cloud requires public repos)

### **If the dashboard doesn't work:**
1. Check the API URL is correct
2. Verify the API is running and accessible
3. Check Streamlit Cloud logs for errors

---

## 🎯 **WHAT YOU'LL GET**

After successful setup, you'll have:
- ✅ A live Streamlit dashboard at `https://your-app-name.streamlit.app`
- ✅ Real-time connection to your MEM_AGENT API
- ✅ AI mentor chat interface
- ✅ Business analytics and metrics
- ✅ System health monitoring

---

## 📞 **NEED HELP?**

If you get stuck:
1. **Check GitHub**: Make sure your code is uploaded to GitHub
2. **Verify Files**: Ensure `dashboard/app.py` and `requirements.txt` exist
3. **Test API**: Confirm the API URL is working
4. **Check Logs**: Look at Streamlit Cloud deployment logs

**🎉 Once set up, you'll have a beautiful, functional dashboard for your MEM_AGENT system!**
