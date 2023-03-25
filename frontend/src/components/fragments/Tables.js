import {
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@mui/material";
import React, { useState, useEffect, useMemo } from "react";
import { useSelector } from 'react-redux';

import DataService from "../../services/data";

var dateFormat = require("dateformat");
const dateFormatLong = "ddd dd/mm/yy HH:MM";
const dateFormatShort = "dd mmm yyyy";

const dateOrNull = (date, longFormat) => {
  if (date === null) {
    return null;
  } else {
    return dateFormat(
      new Date(date),
      longFormat ? dateFormatLong : dateFormatShort
    );
  }
};

const LatestEventsTable = () => {
  const [eventsList, setEventsList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getMeetingsFromApi = async () => {
      const events = await dataService.getMeetings(10);
      if (events) {
        setEventsList(events);
      }
    };

    getMeetingsFromApi();
  }, [dataService]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>Who</TableCell>
          <TableCell>What</TableCell>
          <TableCell>When</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {eventsList.map((event) => (
          <TableRow key={event.id}>
            <TableCell component="th" scope="row">
              {event.person.name}
            </TableCell>
            <TableCell>{event.what}</TableCell>
            <TableCell>{dateOrNull(event.when, true)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const PlansTable = () => {
  const [plansList, setPlansList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPlansFromApi = async () => {
      const plans = await dataService.getPlans(10);
      if (plans) {
        setPlansList(plans);
      }
    };

    getPlansFromApi();
  }, [dataService]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>Who</TableCell>
          <TableCell>What</TableCell>
          <TableCell>When</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {plansList.map((plan) => (
          <TableRow key={plan.id}>
            <TableCell component="th" scope="row">
              {plan.person.name}
            </TableCell>
            <TableCell>{plan.what}</TableCell>
            <TableCell>{dateOrNull(plan.when, true)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const NotesTable = (props) => {
  const [notesList, setNotesList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPersonNotesFromApi = async (personId) => {
      const notes = await dataService.getPersonNotes(personId);
      if (notes) {
        setNotesList(notes);
      }
    };

    if (props.personId > 0) {
      getPersonNotesFromApi(props.personId);
    }
  }, [dataService, props]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell size="small">When</TableCell>
          <TableCell>What</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {notesList.map((note) => (
          <TableRow key={note.id}>
            <TableCell>{dateOrNull(note.when, true)}</TableCell>
            <TableCell>{note.what}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const ToSeeTable = () => {
  const [toSeeList, setToSeeList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPlansFromApi = async () => {
      const toSee = await dataService.getPlans(15);
      if (toSee) {
        setToSeeList(toSee);
      }
    };

    getPlansFromApi();
  }, [dataService]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>Who</TableCell>
          <TableCell>Days since last seen</TableCell>
          <TableCell>Total meetings</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {toSeeList.map((toSee) => (
          <TableRow key={toSee.id}>
            <TableCell>{toSee.name}</TableCell>
            <TableCell>{toSee.days_since_last_seen}</TableCell>
            <TableCell>{toSee.total_meetings}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const PersonsSummaryTable = () => {
  const [personsSummaryList, setPersonSummaryList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPersonsSummaryFromApi = async () => {
      const personsSummary = await dataService.getAnalyticsPersonsSummary(100);
      if (personsSummary) {
        setPersonSummaryList(personsSummary);
      }
    };

    getPersonsSummaryFromApi();
  }, [dataService]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>Who</TableCell>
          <TableCell>First Met At</TableCell>
          <TableCell>First Met Where</TableCell>
          <TableCell>Total Meetings</TableCell>
          <TableCell>Last Seen At</TableCell>
          <TableCell>Last Seen Where</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {personsSummaryList.map((personSummary) => (
          <TableRow key={personSummary.id}>
            <TableCell>{personSummary.name}</TableCell>
            <TableCell>
              {dateOrNull(personSummary.first_met_at, false)}
            </TableCell>
            <TableCell>{personSummary.first_met_comment}</TableCell>
            <TableCell>{personSummary.num_meetings}</TableCell>
            <TableCell>
              {dateOrNull(personSummary.last_seen_at, false)}
            </TableCell>
            <TableCell>{personSummary.last_seen}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const EventsSummaryTable = () => {
  const [eventsSummaryList, setEventsSummaryList] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getEventsSummaryFromApi = async () => {
      const eventsSummary = await dataService.getAnalyticsEventsSummary(100);
      if (eventsSummary) {
        setEventsSummaryList(eventsSummary);
      }
    };

    getEventsSummaryFromApi();
  }, [dataService]);

  return (
    <Table aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>What</TableCell>
          <TableCell>When</TableCell>
          <TableCell>Who</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {eventsSummaryList.map((eventSummary) => (
          <TableRow key={eventSummary.hash_id}>
            <TableCell>{eventSummary.what}</TableCell>
            <TableCell>{dateOrNull(eventSummary.when, true)}</TableCell>
            <TableCell>{eventSummary.who.join(", ")}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export {
  LatestEventsTable,
  PersonsSummaryTable,
  EventsSummaryTable,
  PlansTable,
  NotesTable,
  ToSeeTable,
};
