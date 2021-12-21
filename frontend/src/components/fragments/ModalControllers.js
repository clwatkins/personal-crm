import React, { useState } from "react";

import { PlanForm, SeeForm } from "./Forms";
import { EventsSummaryTable, PersonsSummaryTable } from "./Tables";

import {
  ModalControlButtons,
  ModalControlButtonIcons,
} from "./ModalControlBars";

const PersonFormController = () => {
  const values = [
    { value: "see", label: "Seeing" },
    { value: "plan", label: "Planning" },
  ];
  const [selectedValue, setSelectedValue] = useState("see");

  const chooseFormToRender = (selectedValue) => {
    switch (selectedValue) {
      case "see":
        return <SeeForm />;
      case "plan":
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
  const [selectedValue, setSelectedValue] = useState("events");

  const chooseTableToRender = (selectedValue) => {
    switch (selectedValue) {
      case "people":
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
