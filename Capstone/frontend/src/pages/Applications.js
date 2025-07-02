import React from 'react';
import { Container, Typography } from '@mui/material';

const Applications = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Applications
      </Typography>
      <Typography variant="body1">
        Applications management page - Coming soon!
      </Typography>
    </Container>
  );
};

export default Applications; 