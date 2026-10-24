# Lost and Found Item Tracking Website  

## Overview  
This project is a web-based platform designed to help users report, search, and recover lost and found items efficiently.  

**Live demo:** https://lost-found-tracking.onrender.com (hosted on Render's free plan, so the first request after a period of inactivity can take up to a minute while the service wakes up).

## Features  

### User Authentication  
- **Login and Signup**: Users can create an account or log in using their email credentials and are verified before signing up.  
- **Password Reset**: Users can request a reset link by email; links are signed and expire after 1 hour.  

### User Dashboard  
- Provides an overview of all user posts, interactions, and personal information.  

### Reporting Lost and Found Items  
- **Lost Items**: Users can submit details about their lost items, including description, date, location, and images.  
- **Found Items**: Individuals can report found items with relevant details or match them to existing lost item reports.  

### Searching and Filtering  
- **Search Lost Items**: Users can search the database for lost items using keywords.  
- **Filtered Search**: Apply filters like category, date, and location to refine search results.  

### Listings  
- **Lost Items Listing**: Publicly accessible list of all lost item reports.  
- **Found Items Listing**: Publicly accessible list of all found item reports.  

### Matching and Verification  
- **Automated Matching**: Suggests potential matches between lost and found items based on descriptions and metadata.  
- **Ownership Verification**: Claimants must provide verification (e.g., questionnaire, unique identifiers, proof of purchase) before retrieving items.  

### Post Management  
- Users can add, edit, update status, or delete their item reports.  

### Communication and Fraud Prevention  
- **Chat System**: Enables direct messaging between users to coordinate item returns.  
- **Fraud Alert**: Flags suspicious claims or activities to prevent fraudulent retrievals.  

### Community Engagement  
- **Top Contributor Recognition**: Recognizes and rewards users who frequently report and return items through leaderboards or badges.  
- **Social Media Sharing**: Allows users to share reports on platforms like Facebook and Twitter for increased visibility.  

### Admin Control  
- Admins can oversee reports, manage disputes, and ensure compliance with platform rules.  

## Technologies
- **Frontend**: HTML, CSS, Bootstrap, Jinja2
- **Backend**: Flask, Flask-SocketIO (real-time chat)
- **Database**: PostgreSQL in production (Render), SQLite for local development
- **AI Matching**: Google Gemini embeddings (`gemini-embedding-001`) + cosine similarity
- **Email**: Mailjet Send API (HTTPS) for password reset emails
- **Hosting**: Render (Gunicorn with a threaded `gthread` worker)

## Getting Started
1. Clone the repository.
2. Create a virtualenv and install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in the values (see below).
4. Run the development server: `python run.py`

### Environment variables
| Variable | Required | Purpose |
|---|---|---|
| `SECRET_KEY` | Yes (unless `FLASK_DEBUG=true`) | Flask session/CSRF signing key. The app refuses to start without it outside debug mode. |
| `FLASK_DEBUG` | No | Set to `true` for local development to enable Flask debug mode and allow an insecure default `SECRET_KEY`. |
| `DATABASE_URL` | No | SQLAlchemy database URI. Defaults to a local `sqlite:///lostandfound.db` if unset. |
| `GOOGLE_API_KEY` | No | Enables AI-based lost/found matching via Gemini embeddings. Matching is disabled without it. |
| `MAILJET_API_KEY` / `MAILJET_SECRET_KEY` | No | Mailjet API credentials for sending password reset emails. Without them no email is sent; in debug mode the reset link is logged to the console instead. |
| `MAIL_SENDER` | No | "From" address for emails. Must be a validated sender in your Mailjet account. |
| `MAIL_SENDER_NAME` | No | Display name for the sender. Defaults to `Lost & Found`. |
| `SEED_DEMO_USERS` | No | Set to `true` to seed demo `admin@test.com` / `user@test.com` accounts on startup (local dev only). |
| `DEMO_ADMIN_PASSWORD` / `DEMO_USER_PASSWORD` | No | Override the seeded demo account passwords. |

## Deployment
The app is deployed on [Render](https://render.com) as a Blueprint defined in [`render.yaml`](render.yaml), and every commit pushed to `main` is deployed automatically.

- Render runs `flask db upgrade` (database migrations) and then starts Gunicorn with a single `gthread` worker (`-w 1 --threads 100`). Flask-SocketIO runs in `threading` mode, so real-time chat works over regular threads with WebSocket support from `simple-websocket`. Keep it to one worker: Socket.IO rooms live in that worker's memory, and multiple workers would need a message queue such as Redis.
- Secrets marked `sync: false` in `render.yaml` (`DATABASE_URL`, `GOOGLE_API_KEY`, `MAILJET_*`, `MAIL_SENDER`) must be set in the service's **Environment** tab on Render, which only prompts for them when a Blueprint is first created. Never set `FLASK_DEBUG` in production.
- Render's free plan blocks outbound SMTP ports, which is why email is sent over HTTPS through Mailjet's API rather than SMTP.

## Contributing  
University group based work.

## License  
This project is licensed under the [MIT License]().