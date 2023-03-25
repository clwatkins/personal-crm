import React from "react";
import { useHistory, Link } from "react-router-dom";
import { styled, Button, Grid, Toolbar, Typography } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";

import { userLogout } from "../reducers/authSlice";

const HeaderButton = styled(Button)(() => ({
    color: "white",
    fontSize: "1rem",
}));

const AppBar = () => {
    return <AppBar position="static">
        <Toolbar>
            <Grid justify="space-between" container spacing={12}>
                <Grid item xs={11}>
                    <Link to="/">
                        <HeaderButton>FriendCRM</HeaderButton>
                    </Link>

                    <Link to="/people">
                        <HeaderButton>People</HeaderButton>
                    </Link>

                    <Link to="/analytics">
                        <HeaderButton>Analytics</HeaderButton>
                    </Link>
                </Grid>
                <Grid item xs={1}>
                    <AuthButton />
                </Grid>
            </Grid>
        </Toolbar>
    </AppBar>
}

function AuthButton() {
    const isLoggedIn = useSelector(state => state.auth.isLoggedIn);
    const userName = useSelector(state => state.auth.user);

    const dispatch = useDispatch();
    let history = useHistory();

    if (!isLoggedIn) {
        return (
            <Link to="/login">
                <HeaderButton>Login</HeaderButton>
            </Link>
        )
    } else {
        return (
            <>
                <Typography variant="h6" display="inline">
                    Welcome {userName}!
                </Typography>
                <HeaderButton onClick={() => {
                    dispatch(userLogout()); history.push("/login");
                }}>Logout</HeaderButton>
            </>
        )
    }
}

export default AppBar;