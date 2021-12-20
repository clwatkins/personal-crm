// Assumes backend running on :5000
const backendAddr = `http://${window.location.hostname}:5000`;
console.log(backendAddr);

const eventEndpoints = {
  add: "persons",
  plan: "plans",
  see: "meetings",
  notes: "notes",
  personDetails: "person",
  analyticsMostSeen: "analytics/most-seen",
  analyticsToSee: "analytics/to-see",
  analyticsPersonsSummary: "analytics/persons-summary",
  analyticsEventsSummary: "analytics/events-summary",
};

// Event type == persons, plans, meetings
async function getInfoWithLimit(eventType, limit) {
  let addr = `${backendAddr}/${eventEndpoints[eventType]}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  return await res.json();
}

const getPeople = (limit) => getInfoWithLimit("add", limit);
const getPlans = (limit) => getInfoWithLimit("plan", limit);
const getMeetings = (limit) => getInfoWithLimit("see", limit);
const getPersonsSummary = (limit) =>
  getInfoWithLimit("analyticsPersonsSummary", limit);
const getEventsSummary = (limit) =>
  getInfoWithLimit("analyticsEventsSummary", limit);

// Event type == persons, notes
async function getInfoForPerson(eventType, personId) {
  const res = await fetch(
    `${backendAddr}/${eventEndpoints[eventType]}/${personId}`,
    {
      method: "GET",
    }
  );
  return await res.json();
}

var getPersonDetails = (personId) =>
  getInfoForPerson("personDetails", personId);
var getNotes = (personId) => getInfoForPerson("notes", personId);

async function createEvent(eventType, persons, text) {
  let addr = `${backendAddr}/${eventEndpoints[eventType]}`;
  let body = { persons: persons, what: text };

  const res = await fetch(addr, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(body),
  });

  return await res.json();
}

async function createNote(personId, note) {
  await fetch(`${backendAddr}/${eventEndpoints.notes}/${personId}`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify({
      what: note,
    }),
  });
}

async function updatePersonDetails(personId, newDetails) {
  await fetch(`${backendAddr}/${eventEndpoints.personDetails}/${personId}`, {
    method: "PATCH",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(newDetails),
  });
}

async function getMostSeen(limit) {
  let addr = `${backendAddr}/${eventEndpoints.analyticsMostSeen}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  return await res.json();
}

async function getToSee(limit) {
  let addr = `${backendAddr}/${eventEndpoints.analyticsToSee}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  return await res.json();
}

export {
  createEvent,
  getEventsSummary,
  getPeople,
  getMeetings,
  getPlans,
  getPersonDetails,
  updatePersonDetails,
  getPersonsSummary,
  getNotes,
  createNote,
  getMostSeen,
  getToSee,
};
