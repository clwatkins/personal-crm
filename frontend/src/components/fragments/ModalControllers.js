import React, { useState } from "react";

import { PlanForm, SeeForm } from "./Forms";
import { EventsSummaryTable, PersonsSummaryTable } from "./Tables";

import FormControlBar from "./FormControlBar";

const PersonFormController = () => {
  const formBarValues = [
    { value: "see", label: "Seeing" },
    { value: "plan", label: "Planning" },
  ];
  const [selectedFormBarValue, setSelectedFormBarValue] = useState("see");

  const chooseFormToRender = (selectedFormBarValue) => {
    switch (selectedFormBarValue) {
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
      <FormControlBar
        formBarValues={formBarValues}
        selectedFormBarValue={selectedFormBarValue}
        setSelectedFormBarValue={setSelectedFormBarValue}
      />
      {chooseFormToRender(selectedFormBarValue)}
      <br />
    </div>
  );
};

const SummaryTableController = () => {
  const formBarValues = [
    { value: "events", label: "Events" },
    { value: "people", label: "People" },
  ];
  const [selectedFormBarValue, setSelectedFormBarValue] = useState("events");

  const chooseTableToRender = (selectedFormBarValue) => {
    switch (selectedFormBarValue) {
      case "people":
        return <PersonsSummaryTable />;
      default:
        return <EventsSummaryTable />;
    }
  };

  return (
    <div>
      <FormControlBar
        formBarValues={formBarValues}
        selectedFormBarValue={selectedFormBarValue}
        setSelectedFormBarValue={setSelectedFormBarValue}
      />
      {chooseTableToRender(selectedFormBarValue)}
      <br />
    </div>
  );
};

export { PersonFormController, SummaryTableController };
