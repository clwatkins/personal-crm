import {
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@mui/material";
import { getMeetings, getPlans, getNotes, getToSee } from "../../Api";
import React, { useState, useEffect } from "react";

var dateFormat = require("dateformat");
const dateFormatStr = "ddd dd/mm/yy HH:MM";

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
            <TableCell>
              {dateFormat(new Date(event.when), dateFormatStr)}
            </TableCell>
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
            <TableCell>
              {dateFormat(new Date(plan.when), dateFormatStr)}
            </TableCell>
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
            <TableCell>
              {dateFormat(new Date(note.when), dateFormatStr)}
            </TableCell>
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

export { EventsTable, PlansTable, NotesTable, ToSeeTable };
