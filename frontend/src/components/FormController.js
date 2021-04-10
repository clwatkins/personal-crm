import { useState } from "react";

import { AddForm, PlanForm, SeeForm } from "./Forms";
import FormControlBar from "./FormControlBar";

const FormController = () => {
  const [formBarValue, setFormBarValue] = useState("see");

  const chooseFormToRender = (formBarValue) => {
    switch (formBarValue) {
      case "see":
        return <SeeForm />;
      case "add":
        return <AddForm />;
      case "plan":
        return <PlanForm />;
      default:
        return <SeeForm />;
    }
  };

  return (
    <div>
      <FormControlBar
        formBarValue={formBarValue}
        setFormBarValue={setFormBarValue}
      />
      {chooseFormToRender(formBarValue)}
      <br />
    </div>
  );
};

export default FormController;
