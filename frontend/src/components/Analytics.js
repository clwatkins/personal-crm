import {
  Container,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@material-ui/core";
import { indigo } from "@material-ui/core/colors";

import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";
import React, { useState, useEffect } from "react";

import { getMostSeen } from "../Api";
import { EventsTable, PlansTable } from "./Tables";

const MostSeenBar = () => {
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
      width={400}
      height={250}
      data={mostSeenData}
      margin={{
        top: 10,
        right: 10,
        left: 10,
        bottom: 0,
      }}
    >
      <XAxis dataKey="name" />
      <YAxis />
      <Bar dataKey="count" fill={indigo[700]} />
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
                <Typography variant="h6">Who have you seen lately?</Typography>
                <EventsTable />
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
