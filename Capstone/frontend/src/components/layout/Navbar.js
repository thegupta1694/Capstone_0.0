import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Menu,
  MenuItem,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleClose();
    navigate('/login');
  };

  const getNavItems = () => {
    const items = [
      { text: 'Dashboard', path: '/dashboard' },
      { text: 'Professors', path: '/professors' },
      { text: 'Teams', path: '/teams' },
      { text: 'Applications', path: '/applications' },
    ];

    // Filter based on user role
    if (user?.role === 'admin') {
      return items;
    } else if (user?.role === 'teacher') {
      return items.filter(item => item.text !== 'Teams');
    } else {
      return items.filter(item => item.text !== 'Teams');
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Project Allocation System
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {getNavItems().map((item) => (
            <Button
              key={item.text}
              color="inherit"
              onClick={() => navigate(item.path)}
            >
              {item.text}
            </Button>
          ))}

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">
              {user?.first_name} {user?.last_name}
            </Typography>
            <Avatar
              sx={{ width: 32, height: 32, cursor: 'pointer' }}
              onClick={handleMenu}
            >
              {user?.first_name?.[0] || user?.username?.[0] || 'U'}
            </Avatar>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </Box>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 