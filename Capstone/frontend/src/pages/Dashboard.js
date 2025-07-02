import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [myTeam, setMyTeam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [teamName, setTeamName] = useState('');

  useEffect(() => {
    if (user?.role === 'student') {
      fetchMyTeam();
    } else {
      setLoading(false);
    }
    // eslint-disable-next-line
  }, [user]);

  const fetchMyTeam = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/teams/my/');
      setMyTeam(response.data);
    } catch (error) {
      if (error.response?.status === 404) {
        setMyTeam(null);
      } else {
        setError('Failed to fetch team information');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTeam = async () => {
    try {
      const response = await api.post('/api/teams/create/', {
        name: teamName,
      });
      setMyTeam(response.data);
      setCreateDialogOpen(false);
      setTeamName('');
      setError('');
    } catch (error) {
      setError(error.response?.data?.name?.[0] || 'Failed to create team');
    }
  };

  const getWelcomeMessage = () => {
    switch (user?.role) {
      case 'student':
        return 'Welcome to your Student Dashboard';
      case 'teacher':
        return 'Welcome to your Professor Dashboard';
      case 'admin':
        return 'Welcome to your Admin Dashboard';
      default:
        return 'Welcome to the Project Allocation System';
    }
  };

  const getDashboardContent = () => {
    switch (user?.role) {
      case 'student':
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Team Management
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Create or join a team to start applying for projects.
                  </Typography>
                  {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" minHeight="60px">
                      <CircularProgress size={24} />
                    </Box>
                  ) : myTeam ? (
                    <Alert severity="success" sx={{ mt: 2 }}>
                      You are in team: <b>{myTeam.name}</b>
                    </Alert>
                  ) : (
                    <Button
                      variant="contained"
                      color="primary"
                      sx={{ mt: 2 }}
                      onClick={() => setCreateDialogOpen(true)}
                    >
                      Create Team
                    </Button>
                  )}
                  {error && (
                    <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
                  )}
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Applications
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Track your team's project applications and responses.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        );
      
      case 'teacher':
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Applications Received
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Review and respond to team applications for your projects.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Profile Management
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Update your research domains and available project slots.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        );
      
      case 'admin':
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    System Overview
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Monitor the overall allocation process and statistics.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    User Management
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Manage users, teams, and applications across the system.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        );
      
      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        {getWelcomeMessage()}
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        Hello, {user?.first_name} {user?.last_name} ({user?.username})
      </Typography>

      <Box sx={{ mt: 4 }}>
        {getDashboardContent()}
      </Box>
      {/* Create Team Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>Create New Team</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Team Name"
            fullWidth
            variant="outlined"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
            sx={{ mt: 1 }}
            helperText="Choose a unique name for your team"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateTeam}
            variant="contained"
            disabled={!teamName.trim()}
          >
            Create Team
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Dashboard; 