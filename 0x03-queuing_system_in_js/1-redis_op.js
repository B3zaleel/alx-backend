#!/usr/bin/yarn dev
import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const setNewSchool = (schoolName, value) => {
  client.SET(schoolName, value, (_err, reply) => {
    if (reply) {
      console.log('Reply:', reply);
    }
  });
};

const displaySchoolValue = (schoolName) => {
  client.GET(schoolName, (_err, reply) => {
    if (reply) {
      console.log(reply);
    }
  });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
