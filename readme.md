# DLS Exam Project

### Formål

### Hvad gør vi brug af:
    Frontend: 
        - Azure: Til hosting
        - Svelte: UI Framework
        - Google Maps API: Til vores spil så der er billeder og streetview

    Backend:
        - MongoDB: Raw game data
        - MySQL: User data (Username, Password, Email)
        - MySQL: Ydeligere user data (Alt andet relevant userdata, spil, rekorder, osv...)
        - Kubernetes: To be continued...
        - Docker: To be continued...
        - Python sessions: Hosting game
        - Email: Sende mails afsted hvis din rekord slås
        - RabbitMQ: Handles  meddelser

    
### Microservies 
    - User Auth: Checks user authentication, both credentials and creates new users
    - Leaderboard: Saves top 10 games, inlcuding score and user.
    - Notification: Sends email to users, based on leaderboard conditions.
    - Dead letter queue: Saves data (Idk how to describe)
    - Map and image processing: Gets  and confirms random street maps location (maybe map cache search, too save map locations, for less calls)
    - https://huggingface.co/datasets/osv5m/osv5m (For random location data, lon & lat that we can send to Google Street API to save calls)
    - Save User Relevant Game Data: Handles game and user data, then asserts what is relevant to save in the database.



    