"use strict";

// Read the .env file.
import * as dotenv from "dotenv";
dotenv.config();

// Require the framework
import Fastify from "fastify";


// Instantiate Fastify with some config
const app = Fastify({
  logger: true,
});

app.register(AutoLoad, {
  dir: path.join(__dirname, 'plugins'),
  options: Object.assign({}, opts)
})

// This loads all plugins defined in routes
// define your routes in one of these
app.register(AutoLoad, {
  dir: path.join(__dirname, 'routes'),
  options: Object.assign({}, opts)
})

export default async (req, res) => {
    await app.ready();
    app.server.emit('request', req, res);
}