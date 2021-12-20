import React, { useState, useEffect } from "react";

import { indigo } from "@material-ui/core/colors";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  LineChart,
  Line,
  Tooltip,
} from "recharts";

import { getMostSeen, getPersonTimeline } from "../Api";

var dateFormat = require("dateformat");
const dateFormatStr = "yyyy-mm-dd";

const MostSeenBarChart = () => {
  const [mostSeenData, setMostSeenData] = useState([]);

  useEffect(() => {
    const getMostSeenFromApi = async () => {
      const mostSeen = await getMostSeen(10);
      setMostSeenData(mostSeen);
    };

    getMostSeenFromApi();
  }, []);

  return (
    <BarChart
      layout="vertical"
      height={400}
      width={300}
      data={mostSeenData}
      margin={{
        top: 10,
        right: 10,
        left: 10,
        bottom: 0,
      }}
    >
      <XAxis type="number" />
      <YAxis dataKey="name" type="category" />
      <Bar dataKey="count" fill={indigo[700]} label={{ fill: "white" }}></Bar>
    </BarChart>
  );
};

const PersonTimelineChart = (props) => {
  const [personTimeline, setPersonTimeline] = useState([]);

  useEffect(() => {
    const getPersonTimelineFromApi = async (personId) => {
      const timeline = await getPersonTimeline(personId);
      const modifiedTimelineData = timeline.map((obj) => ({
        ...obj,
        date: Date.parse(obj.when),
      }));
      setPersonTimeline(modifiedTimelineData);
    };

    getPersonTimelineFromApi(props.personId);
  }, [props]);

  console.log(personTimeline);

  var formatXAxis = (dateObj) => {
    console.log(dateObj);
    console.log(dateFormat(dateObj, dateFormatStr));
    return dateFormat(dateObj, dateFormatStr);
  };

  return (
    <LineChart height={300} width={600} data={personTimeline}>
      <XAxis
        dataKey="number"
        type="date"
        domain={["dataMin", "dataMax"]}
        tickFormatter={formatXAxis}
      />
      <YAxis />
      <Tooltip dataKey="what" />
      <Line dataKey="count" type="monotone" stroke="#8884d8" />
    </LineChart>
  );
};

export { MostSeenBarChart, PersonTimelineChart };
