import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Grid,
  Alert,
  CircularProgress,
  Divider,
  IconButton,
  Tooltip,
  Paper,
} from '@mui/material';
import {
  Add as AddIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  Email as EmailIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import TeamMemberCard from '../components/teams/TeamMemberCard';

const Teams = () => {
  const { user } = useAuth();
  const [myTeam, setMyTeam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [invitations, setInvitations] = useState([]);
  const [formData, setFormData] = useState({
    teamName: '',
    inviteUsername: '',
  });

  useEffect(() => {
    fetchMyTeam();
    fetchInvitations();
  }, []);

  const fetchMyTeam = async () => {
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

  const fetchInvitations = async () => {
    try {
      const response = await api.get('/api/teams/invitations/');
      setInvitations(response.data);
    } catch (error) {
      console.error('Failed to fetch invitations:', error);
    }
  };

  const handleCreateTeam = async () => {
    try {
      const response = await api.post('/api/teams/create/', {
        name: formData.teamName,
      });
      setMyTeam(response.data);
      setCreateDialogOpen(false);
      setFormData({ ...formData, teamName: '' });
      setError('');
    } catch (error) {
      setError(error.response?.data?.name?.[0] || 'Failed to create team');
    }
  };

  const handleInviteMember = async () => {
    try {
      await api.post('/api/teams/invite/', {
        user_id: formData.inviteUsername,
      });
      setInviteDialogOpen(false);
      setFormData({ ...formData, inviteUsername: '' });
      setError('');
      // Refresh team data to show new invitation
      fetchMyTeam();
    } catch (error) {
      setError(error.response?.data?.user_id?.[0] || 'Failed to invite member');
    }
  };

  const handleInvitationResponse = async (invitationId, status) => {
    try {
      await api.put(`/api/teams/response/${invitationId}/`, {
        status: status,
      });
      fetchInvitations();
      if (status === 'accepted') {
        fetchMyTeam();
      }
      setError('');
    } catch (error) {
      setError('Failed to respond to invitation');
    }
  };

  const handleDeleteTeam = async () => {
    try {
      await api.delete(`/api/teams/${myTeam.id}/`);
      setMyTeam(null);
      setDeleteDialogOpen(false);
      setError('');
    } catch (error) {
      setError('Failed to delete team');
    }
  };

  const handleMemberUpdate = () => {
    fetchMyTeam();
  };

  const handleMemberRemove = (memberId) => {
    if (myTeam) {
      setMyTeam({
        ...myTeam,
        members: myTeam.members.filter(member => member.id !== memberId),
        member_count: myTeam.member_count - 1
      });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'accepted':
        return 'success';
      case 'rejected':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'accepted':
        return 'Accepted';
      case 'rejected':
        return 'Rejected';
      case 'pending':
        return 'Pending';
      default:
        return status;
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Team Management
        </Typography>
        <Button
          startIcon={<RefreshIcon />}
          onClick={() => {
            fetchMyTeam();
            fetchInvitations();
          }}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* My Team Section */}
      {myTeam ? (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
              <Box>
                <Typography variant="h5" component="h2" gutterBottom>
                  My Team: {myTeam.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Created by {myTeam.leader.first_name} {myTeam.leader.last_name} on{' '}
                  {new Date(myTeam.created_at).toLocaleDateString()}
                </Typography>
              </Box>
              <Box display="flex" alignItems="center" gap={2}>
                <Chip
                  label={`${myTeam.member_count}/4 Members`}
                  color={myTeam.is_full ? 'success' : 'primary'}
                  icon={<GroupIcon />}
                />
                {myTeam.leader.id === user.id && (
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<DeleteIcon />}
                    onClick={() => setDeleteDialogOpen(true)}
                  >
                    Delete Team
                  </Button>
                )}
              </Box>
            </Box>

            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <Typography variant="h6" gutterBottom>
                  Team Members
                </Typography>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  {myTeam.members.map((member) => (
                    <TeamMemberCard
                      key={member.id}
                      member={member}
                      onMemberUpdate={handleMemberUpdate}
                      onMemberRemove={handleMemberRemove}
                    />
                  ))}
                </Paper>
              </Grid>

              <Grid item xs={12} md={4}>
                <Typography variant="h6" gutterBottom>
                  Team Actions
                </Typography>
                <Box display="flex" flexDirection="column" gap={2}>
                  {user.role === 'student' && myTeam.can_invite && (
                    <Button
                      variant="contained"
                      startIcon={<EmailIcon />}
                      onClick={() => setInviteDialogOpen(true)}
                      fullWidth
                    >
                      Invite Member
                    </Button>
                  )}
                  
                  {myTeam.can_leave && (
                    <Button
                      variant="outlined"
                      color="warning"
                      startIcon={<CloseIcon />}
                      onClick={() => setDeleteDialogOpen(true)}
                      fullWidth
                    >
                      Leave Team
                    </Button>
                  )}
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      ) : (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              You're not in a team yet
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Create a team to start applying for projects, or wait for an invitation to join an existing team.
            </Typography>
            {user.role === 'student' && (
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setCreateDialogOpen(true)}
              >
                Create Team
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Pending Invitations Section */}
      {invitations.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Pending Invitations
            </Typography>
            <List>
              {invitations.map((invitation) => (
                <ListItem key={invitation.id} divider>
                  <ListItemAvatar>
                    <Avatar>
                      <PersonIcon />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={`Invitation to join: ${invitation.team.name}`}
                    secondary={`From: ${invitation.team.leader.first_name} ${invitation.team.leader.last_name}`}
                  />
                  <Box>
                    <Tooltip title="Accept">
                      <IconButton
                        color="success"
                        onClick={() => handleInvitationResponse(invitation.id, 'accepted')}
                      >
                        <CheckIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Reject">
                      <IconButton
                        color="error"
                        onClick={() => handleInvitationResponse(invitation.id, 'rejected')}
                      >
                        <CloseIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

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
            value={formData.teamName}
            onChange={(e) => setFormData({ ...formData, teamName: e.target.value })}
            sx={{ mt: 1 }}
            helperText="Choose a unique name for your team"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleCreateTeam} 
            variant="contained"
            disabled={!formData.teamName.trim()}
          >
            Create Team
          </Button>
        </DialogActions>
      </Dialog>

      {/* Invite Member Dialog */}
      <Dialog open={inviteDialogOpen} onClose={() => setInviteDialogOpen(false)}>
        <DialogTitle>Invite Team Member</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="University ID"
            fullWidth
            variant="outlined"
            value={formData.inviteUsername}
            onChange={(e) => setFormData({ ...formData, inviteUsername: e.target.value })}
            helperText="Enter the University ID of the student you want to invite"
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setInviteDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleInviteMember} 
            variant="contained"
            disabled={!formData.inviteUsername.trim()}
          >
            Send Invitation
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Team Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>
          {myTeam?.leader?.id === user.id ? 'Delete Team' : 'Leave Team'}
        </DialogTitle>
        <DialogContent>
          <Typography>
            {myTeam?.leader?.id === user.id 
              ? 'Are you sure you want to delete this team? This action cannot be undone and will remove all team members.'
              : 'Are you sure you want to leave this team?'
            }
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleDeleteTeam} 
            color="error"
            variant="contained"
          >
            {myTeam?.leader?.id === user.id ? 'Delete Team' : 'Leave Team'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Teams; 