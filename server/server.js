// Require the framework and instantiate it
const fastify = require('fastify')({ logger: true })
fastify.register(require("@fastify/cors"))
fastify.register(require('@fastify/websocket'))

fastify.register(require('@fastify/redis'), { 
  host: 'redis-12622.c277.us-east-1-3.ec2.cloud.redislabs.com',
  port: 12622,
  password: 'TxVYpEfg4DwZSjDxerOiWxNEhgIZouKa'
})



fastify.register(async function (fastify) {
  fastify.get('/*', { websocket: true }, (connection, req) => {
    connection.socket.on('message', message => {
      // message.toString() === 'hi from client'
      connection.socket.send('ok')
      fastify.websocketServer.clients.forEach(function each(client) {
        if (client.readyState === 1) {
          client.send(message);
        }
      });
    })
  })

  fastify.get('/', { websocket: true }, (connection /* SocketStream */, req /* FastifyRequest */) => {
    connection.socket.on('message', message => {
      // message.toString() === 'hi from client'
      connection.socket.send('hi from server')
    })
  })
})

fastify.listen({ port: 4000 }, err => {
  if (err) {
    fastify.log.error(err)
    process.exit(1)
  }
})

