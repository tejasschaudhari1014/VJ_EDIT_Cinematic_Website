# VJ EDIT — Cinematic Video Ordering Website

## Features
- Cinematic black/red/orange landing page
- Services and pricing sections
- Instagram profile ordering links: https://www.instagram.com/_vj_505?dlrf=ZG1mMTN3MDJvZ2xz
- Order request form with optional reference video/image upload
- SQLite order storage
- Basic admin order dashboard at `/admin`
- Order status updates

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start:
   `python app.py`
6. Open `http://127.0.0.1:5000`

## Important before public deployment
- `/admin` is a demo dashboard and is NOT password protected. Add authentication before deployment.
- Change `SECRET_KEY` using an environment variable.
- Configure cloud storage for large customer videos; local uploads are not suitable for many hosting platforms.
- Confirm final prices, delivery times, payment method and refund policy before accepting paid orders.
- Instagram links open the profile; customers send their order details through Instagram DM.
