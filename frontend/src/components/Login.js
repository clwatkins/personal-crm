import React from "react";
import { Redirect } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userLogin } from "../reducers/authSlice";

function Login() {
    const dispatch = useDispatch();
    const isLoggedIn = useSelector(state => state.auth.isLoggedIn);

    function handleLogin() {
        console.log('Logging in...')
        dispatch(userLogin("hello@wor.ld", "helloworld!"));
        console.log('Logged in. Redirecting to home...')

        if (isLoggedIn) {
            <Redirect
                to={{
                    pathname: "/",
                }}
            />
        }
    }

    return (
        <div>
            <p>You must log in to view the page</p>
            <button onClick={handleLogin}>Log In</button>
        </div>
    )
}

export default Login;
