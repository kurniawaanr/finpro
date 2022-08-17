import { createSlice } from "@reduxjs/toolkit";
import { useRouter } from "next/router";

const initialState = {
  username: null,
  isLoggedIn: false,
};

const userReducer = createSlice({
  name: "user",
  initialState,
  reducers: {
    loginHandler: (state, action) => {
      state.username = action.username;
      state.isLoggedIn = true;
    },
    logoutHandler: (state) => {
      state.username = null;
      state.isLoggedIn = false;
      useRouter().push('/login');
    },
  },
});

export const { loginHandler, logoutHandler } = userReducer.actions;

//Export the variable
export const selectIsLoggedIn = (state) => state.userReducer.isLoggedIn;
export const selectUsername = (state) => state.userReducer.username;

export default userReducer.reducer;
