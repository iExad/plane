import express, { Request, Response } from "express";
import expressWs, { Application } from "express-ws";
import { Server } from "@hocuspocus/server";
import { Database } from "@hocuspocus/extension-database";
import { Logger } from "@hocuspocus/extension-logger";
import debounce from "debounce";

let debounced: any;

const server = Server.configure({
  async onChange(data) {
    const save = () => {
      console.log(
        `Document ${data.documentName} changed by ${data.context.user.name}`
      );
    };

    debounced?.clear();
    debounced = debounce(save, 4000);
    debounced();
  },
  onListen: async ({ instance, port }) => {
    console.log("ran onListen", instance, port);
  },
  onConnect: async ({ socketId }) => {
    console.log("ran onConnect", socketId);
  },
  async connected() {
    console.log("connections:", server.getConnectionsCount());
  },
  onRequest: async ({ request }) => {
    console.log("ran onRequest", request);
  },
  extensions: [
    new Logger(),
    new Database({
      // Return a Promise to retrieve data …
      fetch: async ({ documentName, socketId }) => {
        return new Promise((resolve, reject) => {
          console.log("ran fetch", documentName, socketId);
        });
      },
      // … and a Promise to store data:
      store: async ({ documentName, state, socketId }) => {
        return new Promise((resolve, reject) => {
          console.log("ran stroe", documentName, socketId);
        });
      },
    }),
  ],
});

const { app }: { app: Application } = expressWs(express());

app.get("/", (_request: Request, response: Response) => {
  response.send("Hello World!");
});

app.ws("/collaboration", (websocket, request: Request) => {
  console.log("aaya");
  const context = {
    user: {
      id: 1234,
      name: "Jane",
    },
  };

  server.handleConnection(websocket, request, context);
});

app.listen(1234, () => console.log("Listening on http://127.0.0.1:1234"));
