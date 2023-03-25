// TODO: this needs to be cleaned up and made https
export const LOCAL_STORAGE_KEY = 'user';

const _API_STEM = `http://${window.location.hostname}:5000`;
const _FRAGMENTS = {
    ANALYTICS_EVENTS_SUMMARY: '/analytics/events-summary',
    ANALYTICS_MOST_SEEN: '/analytics/most-seen',
    ANALYTICS_PERSONS_SUMMARY: '/analytics/persons-summary',
    ANALYTICS_TO_SEE: '/analytics/to-see',
    LOGIN: '/login',
    MEETINGS: '/meetings',
    NOTES: '/notes',
    PEOPLE: '/persons',
    PERSON: '/person',
    PLANS: '/plans',
    REGISTER: '/register',    
}
export const API_ROUTES = {
    CREATE_USER_MEETING:_API_STEM + _FRAGMENTS.MEETINGS,
    CREATE_USER_PERSON_NOTE:_API_STEM + _FRAGMENTS.NOTES,
    CREATE_USER_PEOPLE: _API_STEM + _FRAGMENTS.PEOPLE,
    CREATE_USER_PLAN: _API_STEM + _FRAGMENTS.PLANS,
    FETCH_USER_ANALYTICS_EVENTS_SUMMARY: _API_STEM + _FRAGMENTS.ANALYTICS_EVENTS_SUMMARY,
    FETCH_USER_ANALYTICS_MOST_SEEN: _API_STEM + _FRAGMENTS.ANALYTICS_MOST_SEEN,
    FETCH_USER_ANALYTICS_PERSONS_SUMMARY: _API_STEM + _FRAGMENTS.ANALYTICS_PERSONS_SUMMARY,
    FETCH_USER_ANALYTICS_TO_SEE: _API_STEM + _FRAGMENTS.ANALYTICS_TO_SEE,
    FETCH_USER_MEETINGS: _API_STEM + _FRAGMENTS.MEETINGS,
    FETCH_USER_NOTES: _API_STEM + _FRAGMENTS.NOTES,
    FETCH_USER_PEOPLE: _API_STEM + _FRAGMENTS.PEOPLE,
    FETCH_USER_PERSON_DETAILS: _API_STEM + _FRAGMENTS.PERSON,
    FETCH_USER_PERSON_NOTES: _API_STEM + _FRAGMENTS.NOTES,
    FETCH_USER_PLANS: _API_STEM + _FRAGMENTS.PLANS,
    LOGIN_USER: _API_STEM + _FRAGMENTS.LOGIN,
    UPDATE_USER_PERSON_DETAILS: _API_STEM + _FRAGMENTS.PERSON,
    REGISTER_USER: _API_STEM + _FRAGMENTS.REGISTER,
}
