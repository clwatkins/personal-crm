import axios from "axios";
import { API_ROUTES, LOCAL_STORAGE_KEY } from "./constants";

class AuthService {
    // Log user in, exchanging email + password for JWT.
    // JWT will be set in localStorage and returned. 
    async login(email, password) {
        var formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        const response = await axios
            .post(API_ROUTES.LOGIN_USER, formData);
        if (response.data.access_token) {
            localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(response.data));
        }
        return response.data;
    }
    logout() {
        localStorage.removeItem(LOCAL_STORAGE_KEY);
    }
    register(email, name, password) {
        return axios.post(API_ROUTES.REGISTER_USER, {
            email: email,
            name: name,
            raw_password: password,
        });
    }
}
export default new AuthService();