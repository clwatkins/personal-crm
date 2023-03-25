import AuthService from "../services/auth";
import { LOCAL_STORAGE_KEY } from "../services/constants";
import { createSlice } from '@reduxjs/toolkit';

function getInitialState() {
    let user = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    return user
        ? { isLoggedIn: true, token: user.access_token, user: user.user }
        : { isLoggedIn: false, token: null, user: null }
}

export const authSlice = createSlice({
    name: 'auth',
    initialState: getInitialState(),
    reducers: {
        loginSuccess: (state, action) => {
            state.isLoggedIn = true;
            state.token = action.payload.access_token;
            state.user = action.payload.user;
        },
        loginFailure: (state) => {
            state.isLoggedIn = false;
            state.token = null;
            state.user = null;
        },
        registerSuccess: (state) => {
            state.isLoggedIn = false;
            state.token = null;
            state.user = null;
        },
        registerFailure: (state) => {
            state.isLoggedIn = false;
            state.token = null;
            state.user = null;
        },
        logout: (state) => {
            state.isLoggedIn = false;
            state.token = null;
            state.user = null;
        }
    }
});

const { registerSuccess, registerFailure, loginSuccess, loginFailure, logout } = authSlice.actions;

export default authSlice.reducer;

export const userRegister = (email, name, password) => {
    return async (dispatch) => {
        try {
            let resp = await AuthService.register(email, name, password);
            console.log(resp);
            dispatch(registerSuccess())
        } catch (err) {
            console.log(err)
            dispatch(registerFailure())
        }
    }
}

export const userLogin = (email, password) => {
    return async (dispatch) => {
        try {
            let resp = await AuthService.login(email, password);
            console.log(resp);
            dispatch(loginSuccess(resp))
        } catch (err) {
            console.log(err)
            dispatch(loginFailure())
        }
    }
}

export const userLogout = () => {
    return async (dispatch) => {
        AuthService.logout();
        dispatch(logout());
    }
}