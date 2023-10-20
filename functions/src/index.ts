

import {onRequest} from "firebase-functions/v2/https";


export const helloWorld = onRequest((request, response) => {
  if (request.method === "OPTIONS") {
    const headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    };
    response.send("").status(204).header(headers);
    return;
  }
  const headers = {"Access-Control-Allow-Origin": "*"};
  response.send("Hello world!").status(200).header(headers);
});
