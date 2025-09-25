
        # MANUAL SETUP INSTRUCTIONS FOR COMPLEX TASKS
        
        ## Phase 2: Website Deployment & Mautic Funnel
        
        ### 1. Domain Configuration (MANUAL)
        - Register domain name with a reputable registrar
        - Configure DNS A record to point to VM external IP (34.28.159.240)
        - Set up CNAME records for www and subdomains
        - Wait for DNS propagation (24-48 hours)
        
        ### 2. SSL Certificate Setup (MANUAL)
        - Install Certbot: `sudo apt-get install certbot python3-certbot-nginx`
        - Obtain SSL certificate: `sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com`
        - Configure auto-renewal: `sudo crontab -e` (add: 0 12 * * * /usr/bin/certbot renew --quiet`)
        
        ### 3. Mautic Installation (MANUAL)
        - Access Mautic installation: http://34.28.159.240/mautic/
        - Follow installation wizard
        - Configure database connection (mautic/mautic_password)
        - Set up admin user account
        - Configure email settings for campaigns
        
        ### 4. Content Creation (MANUAL)
        - Write compelling website copy
        - Create lead capture forms
        - Design email marketing sequences
        - Set up analytics tracking (Google Analytics, Facebook Pixel)
        
        ## Phase 3: Chatbot Persona Development
        
        ### 1. Persona Definition (MANUAL)
        - Define chatbot personality and tone
        - Create conversation flow diagrams
        - Write sample dialogues
        - Set up escalation procedures
        
        ### 2. Integration Testing (MANUAL)
        - Test chatbot responses
        - Verify lead qualification logic
        - Test integration with Mautic
        - Configure monitoring and alerts
        
        ## Phase 4: Tool Integration & Data Pipelines
        
        ### 1. Tool Selection (MANUAL)
        - Choose web scraping tools
        - Select data processing platforms
        - Configure API integrations
        - Set up monitoring dashboards
        
        ### 2. Business Logic (MANUAL)
        - Define data processing rules
        - Create content generation templates
        - Set up social media schedules
        - Configure SEO optimization
        
        ## Phase 5: Full Agency Automation
        
        ### 1. Process Design (MANUAL)
        - Map client onboarding workflow
        - Create service delivery templates
        - Design revenue tracking system
        - Plan scaling infrastructure
        
        ### 2. Quality Assurance (MANUAL)
        - Test all automation workflows
        - Verify data accuracy
        - Check system performance
        - Document procedures
        