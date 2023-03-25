import { Container, Card, CardContent, Grid, Typography } from "@mui/material";
import { indigo } from "@mui/material/colors";

import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";
import React, { useState, useEffect, useMemo } from "react";
import { useSelector } from "react-redux";

import DataService from "../services/data";
import { LatestEventsTable, PlansTable, ToSeeTable } from "./fragments/Tables";

const MostSeenBar = () => {
  const [mostSeenData, setMostSeenData] = useState([]);
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getMostSeenFromApi = async () => {
      const mostSeen = dataService.getAnalyticsMostSeen(10);
      setMostSeenData(mostSeen);
    };

    getMostSeenFromApi();
  }, [dataService]);

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

const Analytics = () => {
  return (
    <div>
      <br />
      <Container>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">
                  Who have you seen the most of?
                </Typography>
                <ResponsiveContainer width="100%" height="100%">
                  <MostSeenBar />
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">
                  Who have you not seen lately?
                </Typography>
                <ToSeeTable />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Who did you see last?</Typography>
                <LatestEventsTable />
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">
                  Who do you want to see more of?
                </Typography>
                <PlansTable />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};

export default Analytics;
