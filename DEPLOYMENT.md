# Deployment Guide

This guide will help you deploy your AI Video Generator to GitHub and Vercel.

## Prerequisites

1. **GitHub Account**: Create a free account at [github.com](https://github.com)
2. **Vercel Account**: Create a free account at [vercel.com](https://vercel.com)
3. **Git**: Make sure Git is installed on your system

## Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner and select "New repository"
3. Name your repository: `ai-video-generator`
4. Make it **Public** (required for free Vercel deployment)
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in your project directory:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-video-generator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository: `ai-video-generator`
4. Vercel will automatically detect the configuration from `vercel.json`
5. Click "Deploy"

### Option B: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy from your project directory:
```bash
vercel
```

3. Follow the prompts to link your project

## Step 4: Configure Environment Variables (Optional)

If you need to configure any environment variables:

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add any required variables

## Step 5: Update API Endpoints

The frontend is already configured to work with both local development and deployment:

- **Local Development**: Uses `http://localhost:8000`
- **Production**: Uses `/api` (relative URL for Vercel)

## Deployment Structure

```
ai-video-generator/
├── frontend/          # Static files (HTML, CSS, JS)
├── backend/           # Python API
├── vercel.json        # Vercel configuration
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Custom Domain (Optional)

1. Go to your Vercel project dashboard
2. Navigate to Settings → Domains
3. Add your custom domain
4. Configure DNS settings as instructed

## Troubleshooting

### Common Issues

1. **Build Failures**: Check the Vercel build logs for Python dependency issues
2. **API Errors**: Ensure the backend routes are properly configured in `vercel.json`
3. **CORS Issues**: The frontend is configured to handle CORS automatically

### Performance Optimization

1. **Image Optimization**: Vercel automatically optimizes images
2. **Caching**: Static files are cached by default
3. **CDN**: Vercel provides global CDN for fast loading

## Monitoring

- **Analytics**: View usage statistics in Vercel dashboard
- **Logs**: Check function logs for debugging
- **Performance**: Monitor Core Web Vitals in Vercel Analytics

## Updates

To update your deployed application:

```bash
# Make your changes
git add .
git commit -m "Update description"
git push origin main
```

Vercel will automatically redeploy when you push to the main branch.

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Documentation**: [docs.github.com](https://docs.github.com)
- **Project Issues**: Create issues in your GitHub repository
