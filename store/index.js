import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit";

import userReducer from "./features/userReducer";

export function makeStore() {
  return configureStore({
    reducer: {
      userReducer: userReducer,
    },
  });
}

const store = makeStore();

export default store;