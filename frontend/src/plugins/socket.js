import { io } from "socket.io-client";

const socket = io("https://smart-inventory-app.onrender.com/"); 

export default {
  install(app) {
    app.config.globalProperties.$socket = socket;
  },
};
