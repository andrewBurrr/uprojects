# Use an official Node.js runtime as the base image
FROM node:14 AS build

# Set the working directory within the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application code to the container
COPY . .

# Build the React app for production
RUN npm run build

FROM nginx:latest

# Copy the react build
COPY --from=build /app/build /usr/share/nginx/html