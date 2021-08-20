// Assumes backend running on :5000
const backendAddr = `http://${window.location.hostname}:5000`;
console.log(backendAddr);

const eventEndpoints = {
  add: "people",
  plan: "plan",
  see: "see",
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
  console.log(data);
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
  console.log(data);
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
  console.log(data);
  return data.meetings;
}

async function postEvent(eventType, persons, context) {
  const reqData = {
    persons: persons,
    context: context,
  };

  const res = await fetch(`${backendAddr}/${eventEndpoints[eventType]}`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(reqData),
  });
  console.log(res);
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
  console.log(data);
  return data.data;
}

export { postEvent, getPeople, getEvents, getPlans, getMostSeen };
