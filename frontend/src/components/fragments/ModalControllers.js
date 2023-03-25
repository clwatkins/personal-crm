import React, { useState } from "react";

import { PlanForm, SeeForm, EVENT_TYPES } from "./Forms";
import { EventsSummaryTable, PersonsSummaryTable } from "./Tables";

import {
  ModalControlButtons,
  ModalControlButtonIcons,
} from "./ModalControlBars";

export const TABLE_TYPES = {
  EVENTS: "EVENTS",
  PEOPLE: "PEOPLE"
}

const PersonFormController = () => {
  const values = [
    { value: EVENT_TYPES.SEE, label: "Seeing" },
    { value: EVENT_TYPES.PLAN, label: "Planning" },
  ];
  const [selectedValue, setSelectedValue] = useState(EVENT_TYPES.SEE);

  const chooseFormToRender = (selectedValue) => {
    switch (selectedValue) {
      case EVENT_TYPES.SEE:
        return <SeeForm />;
      case EVENT_TYPES.PLAN:
        return <PlanForm />;
      default:
        return <SeeForm />;
    }
  };

  return (
    <div>
      <ModalControlButtons
        buttonValues={values}
        selectedValue={selectedValue}
        setSelectedValue={setSelectedValue}
      />
      {chooseFormToRender(selectedValue)}
      <br />
    </div>
  );
};

const SummaryTableController = () => {

  const [selectedValue, setSelectedValue] = useState(TABLE_TYPES.EVENTS);

  const chooseTableToRender = (selectedValue) => {
    switch (selectedValue) {
      case TABLE_TYPES.PEOPLE:
        return <PersonsSummaryTable />;
      default:
        return <EventsSummaryTable />;
    }
  };

  return (
    <div>
      <ModalControlButtonIcons
        selectedValue={selectedValue}
        setSelectedValue={setSelectedValue}
      />
      {chooseTableToRender(selectedValue)}
      <br />
    </div>
  );
};

export { PersonFormController, SummaryTableController };
