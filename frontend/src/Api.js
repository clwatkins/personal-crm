// Assumes backend running on :5000
const backendAddr = `http://${window.location.hostname}:5000`;
console.log(backendAddr);

const eventEndpoints = {
  add: "people",
  plan: "plan",
  see: "see",
  notes: "note",
  analyticsMostSeen: "analytics/most-seen",
};

async function getPeople(limit) {
  let addr = `${backendAddr}/${eventEndpoints.add}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  const data = await res.json();
  return data.people;
}

async function getPlans(limit) {
  let addr = `${backendAddr}/${eventEndpoints.plan}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  const data = await res.json();
  return data.plans;
}

async function getEvents(limit) {
  let addr = `${backendAddr}/${eventEndpoints.see}`;
  if (limit > 0) {
    addr = addr + `?limit=${limit}`;
  }
  const res = await fetch(addr, {
    method: "GET",
  });
  const data = await res.json();
  return data.meetings;
}

async function postEvent(eventType, persons, context) {
  const reqData = {
    persons: persons,
    context: context,
  };

  await fetch(`${backendAddr}/${eventEndpoints[eventType]}`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(reqData),
  });
}

async function getNotes(personId) {
  let addr = `${backendAddr}/${eventEndpoints.notes}/${personId}`;
  const res = await fetch(addr, {
    method: "GET",
  });
  const data = await res.json();
  return data.notes;
}

async function postNote(personId, note) {
  const reqData = {
    context: note,
  };
  console.log(reqData);

  await fetch(`${backendAddr}/${eventEndpoints.notes}/${personId}`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(reqData),
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
  const data = await res.json();
  return data.data;
}

export { postEvent, getPeople, getEvents, getPlans, getNotes, postNote, getMostSeen };
