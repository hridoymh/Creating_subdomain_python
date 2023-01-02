import subprocess

def create_subdomain(subdomain: str, server_ip: str):
    # Create the directory for the subdomain
    subprocess.run(["mkdir", "-p", f"/var/www/{subdomain}"])

    # Create the Nginx configuration file for the subdomain
    with open(f"/etc/nginx/sites-available/{subdomain}", "w") as f:
        f.write(f"""
server {{
    listen 80;
    listen [::]:80;

    root /var/www/{subdomain};
    index index.html index.htm index.nginx-debian.html;

    server_name {subdomain};

    location / {{
        try_files $uri $uri/ =404;
    }}
}}
        """)

    # Create a symbolic link from the configuration file to the sites-enabled directory
    subprocess.run(["ln", "-s", f"/etc/nginx/sites-available/{subdomain}", f"/etc/nginx/sites-enabled/"])

    # Test the Nginx configuration
    subprocess.run(["nginx", "-t"])

    # Reload Nginx to apply the changes
    subprocess.run(["systemctl", "reload", "nginx"])

# Example usage
create_subdomain("subdomain.example.com", "your_server_ip")
