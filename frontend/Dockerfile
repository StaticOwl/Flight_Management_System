FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY ./flights/package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY ./flights/ ./

# Build the application
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]