# Use Node.js as base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json before installing dependencies
COPY package.json package-lock.json ./

# Install dependencies inside the container
RUN npm install --legacy-peer-deps

# Ensure TypeScript and dependencies are available before building
RUN npm install axios recharts typescript @types/react @types/react-dom --legacy-peer-deps

# Copy the rest of the application
COPY . .

# **DEBUG: Check if axios and recharts are installed**
RUN npm list axios recharts typescript @types/react @types/react-dom

# **Build the React app (with TypeScript & Vite)**
RUN npm run build

# Install 'serve' to serve the built app
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Serve the `dist/` folder
CMD ["serve", "-s", "dist", "-l", "3000"]

