import {
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@mui/material";
import {
  getMeetings,
  getPersonsSummary,
  getPlans,
  getNotes,
  getToSee,
} from "../../Api";
import React, { useState, useEffect } from "react";

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

const EventsTable = () => {
  const [eventsList, setEventsList] = useState([]);

  useEffect(() => {
    const getMeetingsFromApi = async () => {
      const events = await getMeetings(10);
      setEventsList(events);
    };

    getMeetingsFromApi();
  }, []);

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

  useEffect(() => {
    const getPlansFromApi = async () => {
      const plans = await getPlans(10);
      setPlansList(plans);
    };

    getPlansFromApi();
  }, []);

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

  useEffect(() => {
    const getNotesFromApi = async (personId) => {
      const notes = await getNotes(personId);
      setNotesList(notes);
    };

    if (props.personId > 0) {
      getNotesFromApi(props.personId);
    }
  }, [props]);

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

  useEffect(() => {
    const getToSeeFromApi = async () => {
      const toSee = await getToSee(15);
      setToSeeList(toSee);
    };

    getToSeeFromApi();
  }, []);

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

  useEffect(() => {
    const getPersonsSummaryFromApi = async () => {
      const personsSummary = await getPersonsSummary(100);
      setPersonSummaryList(personsSummary);
    };

    getPersonsSummaryFromApi();
  }, []);

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

export { EventsTable, PersonsSummaryTable, PlansTable, NotesTable, ToSeeTable };
