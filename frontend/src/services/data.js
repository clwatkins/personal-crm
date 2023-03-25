import axios from "axios";
import { API_ROUTES } from "./constants";

export default class DataService {
  constructor(authToken) {
    this.authToken = authToken;
  }

  authHeader() {
    if (this.authToken) {
      return { Authorization: 'Bearer ' + this.authToken };
    } else {
      return {};
    }
  }

  async _getWithProps(apiRoute, optionalProps) {
    let config = { ...optionalProps ? optionalProps : {}, ...{ headers: this.authHeader() } }
    let response = await axios
      .get(
        apiRoute,
        config);
    if (response.status === 200) {
      return response.data
    } else {
      console.error(response.status, response.statusText)
    }
  }

  async _postData(apiRoute, data) {
    let response = await axios.post(apiRoute, data, { headers: this.authHeader() });
    if (response.status !== 201) {
      console.error(response.status, response.statusText)
    }
  }

  limitOr(limit) {
    return limit > 0 ? { limit: limit } : {}
  }

  getPeople = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_PEOPLE, this.limitOr(limit));
  getPersonDetails = (personId) => this._getWithProps(API_ROUTES.FETCH_USER_PERSON_DETAILS + `/${personId}`);
  getPersonNotes = (personId) => this._getWithProps(API_ROUTES.FETCH_USER_PERSON_NOTES + `/${personId}`);
  getPlans = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_PLANS, this.limitOr(limit));
  getMeetings = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_MEETINGS, this.limitOr(limit));
  getAnalyticsEventsSummary = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_ANALYTICS_EVENTS_SUMMARY, this.limitOr(limit));
  getAnalyticsMostSeen = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_ANALYTICS_MOST_SEEN, this.limitOr(limit));
  getAnalyticsPersonsSummary = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_ANALYTICS_PERSONS_SUMMARY, this.limitOr(limit));
  getAnalyticsToSee = (limit) => this._getWithProps(API_ROUTES.FETCH_USER_ANALYTICS_TO_SEE, this.limitOr(limit));

  createPeople = (persons, text) => this._postData(API_ROUTES.CREATE_USER_PEOPLE, { persons: persons, what: text });
  createMeeting = (persons, text) => this._postData(API_ROUTES.CREATE_USER_MEETING, { persons: persons, what: text });
  createPlan = (persons, text) => this._postData(API_ROUTES.CREATE_USER_PLAN, { persons: persons, what: text });
  createNote = (personId, text) => this._postData(API_ROUTES.CREATE_USER_PERSON_NOTE + `/${personId}`, { what: text });

  async updatePersonDetails(personId, newDetails) {
    let response = await axios.patch(API_ROUTES.UPDATE_USER_PERSON_DETAILS + `/${personId}`, newDetails, { headers: this.authHeader() });
    if (response.status !== 200) {
      console.error(response.status, response.statusText)
    }
  }
}
