# 🎯 Quick Cloudinary Setup Guide

## Where to Get Your API Keys

### 1. Sign Up (Free)
👉 https://cloudinary.com/users/register/free

### 2. Get Your Credentials
After signing up, go to your dashboard:
👉 https://console.cloudinary.com/

You'll see a box labeled **"Account Details"** with:

```
Cloud name:    dxyz123abc
API Key:       123456789012345
API Secret:    abcdefghijklmnopqrstuvwxyz123
```

## Where to Add Them

### For Render (Production)

Go to: **Render Dashboard → Your Service → Environment**

Add these 3 variables:

| Key | Value | Example |
|-----|-------|---------|
| `CLOUDINARY_CLOUD_NAME` | Your cloud name | `dxyz123abc` |
| `CLOUDINARY_API_KEY` | Your API key | `123456789012345` |
| `CLOUDINARY_API_SECRET` | Your API secret | `abcdefghijklmnopqrstuvwxyz123` |

### For Local Development (Optional)

Edit your `.env` file:

```env
CLOUDINARY_CLOUD_NAME=dxyz123abc
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123
```

**Note:** If you leave these empty locally, images will be stored in `media/` folder (which is fine for development).

## That's It! 🎉

Once you add these to Render and deploy:
- Product images will automatically upload to Cloudinary
- Images will persist across deployments
- No more ephemeral storage issues

---

## Verification

After deployment, check if it's working:

1. Go to Render Shell
2. Run: `python test_db_connection.py`
3. Check for: `✓ CLOUDINARY_CLOUD_NAME: dxyz...`

Or check your Cloudinary dashboard:
👉 https://console.cloudinary.com/console/media_library

You should see product images appearing there!
