import {
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@material-ui/core";
import { getEvents, getPlans, getNotes } from "../Api";
import React, { useState, useEffect } from "react";

var dateFormat = require("dateformat");
const dateFormatStr = "ddd dd/mm/yy HH:MM";

const EventsTable = () => {
  const [eventsList, setEventsList] = useState([]);

  useEffect(() => {
    const getEventsFromApi = async () => {
      const events = await getEvents(10);
      setEventsList(events);
    };

    getEventsFromApi();
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
          <TableRow key={event.local_query_id}>
            <TableCell component="th" scope="row">
              {event.person_name}
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
          <TableRow key={plan.local_query_id}>
            <TableCell component="th" scope="row">
              {plan.person_name}
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

    getNotesFromApi(props.personId);
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
          <TableRow key={note.local_query_id}>
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

export { EventsTable, PlansTable, NotesTable };
