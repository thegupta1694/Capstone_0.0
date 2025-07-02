import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Avatar,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Alert,
} from '@mui/material';
import {
  Person as PersonIcon,
  EmojiEvents as CrownIcon,
  Delete as DeleteIcon,
  ExitToApp as LeaveIcon,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const TeamMemberCard = ({ member, onMemberUpdate, onMemberRemove }) => {
  const { user } = useAuth();
  const [removeDialogOpen, setRemoveDialogOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

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

  const handleLeaveTeam = async () => {
    setLoading(true);
    setError('');
    
    try {
      await api.post('/api/teams/leave/');
      onMemberUpdate();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to leave team');
    } finally {
      setLoading(false);
      setRemoveDialogOpen(false);
    }
  };

  const handleRemoveMember = async () => {
    setLoading(true);
    setError('');
    
    try {
      await api.delete(`/api/teams/members/${member.id}/remove/`);
      onMemberRemove(member.id);
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to remove member');
    } finally {
      setLoading(false);
      setRemoveDialogOpen(false);
    }
  };

  const canRemoveMember = () => {
    // Team leader can remove any member except themselves
    // Admin can remove any member
    return (user.role === 'admin' || member.team?.leader?.id === user.id) && 
           member.user.id !== user.id;
  };

  const canLeaveTeam = () => {
    // Any member can leave except the team leader
    return member.user.id === user.id && !member.is_leader;
  };

  return (
    <>
      <Card variant="outlined" sx={{ mb: 1 }}>
        <CardContent sx={{ py: 2 }}>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box display="flex" alignItems="center">
              <Avatar sx={{ mr: 2 }}>
                <PersonIcon />
              </Avatar>
              <Box>
                <Typography variant="subtitle1" component="div">
                  {member.user.first_name} {member.user.last_name}
                  {member.is_leader && (
                    <CrownIcon 
                      sx={{ ml: 1, fontSize: 16, color: 'gold' }} 
                      titleAccess="Team Leader"
                    />
                  )}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {member.user.username} • {member.user.department}
                </Typography>
              </Box>
            </Box>
            
            <Box display="flex" alignItems="center" gap={1}>
              <Chip
                label={getStatusText(member.status)}
                color={getStatusColor(member.status)}
                size="small"
              />
              
              {canRemoveMember() && (
                <Tooltip title="Remove member">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => setRemoveDialogOpen(true)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              )}
              
              {canLeaveTeam() && (
                <Tooltip title="Leave team">
                  <IconButton
                    size="small"
                    color="warning"
                    onClick={() => setRemoveDialogOpen(true)}
                  >
                    <LeaveIcon />
                  </IconButton>
                </Tooltip>
              )}
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Remove/Leave Confirmation Dialog */}
      <Dialog open={removeDialogOpen} onClose={() => setRemoveDialogOpen(false)}>
        <DialogTitle>
          {canLeaveTeam() ? 'Leave Team' : 'Remove Member'}
        </DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Typography>
            {canLeaveTeam() 
              ? 'Are you sure you want to leave this team?'
              : `Are you sure you want to remove ${member.user.first_name} ${member.user.last_name} from the team?`
            }
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRemoveDialogOpen(false)} disabled={loading}>
            Cancel
          </Button>
          <Button 
            onClick={canLeaveTeam() ? handleLeaveTeam : handleRemoveMember}
            color="error"
            variant="contained"
            disabled={loading}
          >
            {loading ? 'Processing...' : (canLeaveTeam() ? 'Leave Team' : 'Remove Member')}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default TeamMemberCard; 