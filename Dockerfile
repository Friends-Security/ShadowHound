# Use PowerShell base image with specific version
FROM mcr.microsoft.com/powershell:7.2-ubuntu-20.04

# Set working directory
WORKDIR /app

# Copy scripts
COPY ShadowHound-ADM.ps1 /app/
COPY ShadowHound-DS.ps1 /app/
COPY split_output.py /app/

# Install required PowerShell modules
SHELL ["pwsh", "-Command"]
RUN $ProgressPreference = 'SilentlyContinue' && \
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted && \
    Install-Module -Name ActiveDirectory -Force -SkipPublisherCheck -AllowClobber -Confirm:$false

# Switch back to sh for apt commands
SHELL ["/bin/sh", "-c"]
# Install Python for split_output.py
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create volume for output
VOLUME /output

# Set default command
ENTRYPOINT [ "pwsh" ]