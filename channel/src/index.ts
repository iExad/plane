import express, { Request, Response } from "express";
import expressWs, { Application } from "express-ws";
import { Server } from "@hocuspocus/server";

const server = Server.configure({});

const { app }: { app: Application } = expressWs(express());

app.get("/", (_request: Request, response: Response) => {
  response.send("Hello World!");
});

app.ws("/collaboration", (websocket, request: Request) => {
  const context = {
    user: {
      id: 1234,
      name: "Jane",
    },
  };

  server.handleConnection(websocket, request, context);
});

app.listen(1234, () => console.log("Listening on http://127.0.0.1:1234"));
