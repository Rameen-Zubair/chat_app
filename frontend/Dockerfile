# Use an Nginx base image for serving frontend
FROM nginx:latest

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf  

# Copy frontend files into the container
COPY . /usr/share/nginx/html

# Expose Nginx port
EXPOSE 80
