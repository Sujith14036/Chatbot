import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  ListItemText,
  Chip,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

function App() {
  const [studentProfile, setStudentProfile] = useState({
    id: 1,
    name: '',
    academic_interests: [],
    past_courses: [],
    career_goals: [],
    performance_metrics: {},
    major: '',
    year: '',
    gpa: 0
  });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newInterest, setNewInterest] = useState('');
  const [newGoal, setNewGoal] = useState('');

  const handleGetRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/recommendations', {
        student_profile: studentProfile,
        number_of_recommendations: 5
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
    setLoading(false);
  };

  const addInterest = () => {
    if (newInterest.trim()) {
      setStudentProfile(prev => ({
        ...prev,
        academic_interests: [...prev.academic_interests, newInterest.trim()]
      }));
      setNewInterest('');
    }
  };

  const addGoal = () => {
    if (newGoal.trim()) {
      setStudentProfile(prev => ({
        ...prev,
        career_goals: [...prev.career_goals, newGoal.trim()]
      }));
      setNewGoal('');
    }
  };

  const removeInterest = (interest) => {
    setStudentProfile(prev => ({
      ...prev,
      academic_interests: prev.academic_interests.filter(i => i !== interest)
    }));
  };

  const removeGoal = (goal) => {
    setStudentProfile(prev => ({
      ...prev,
      career_goals: prev.career_goals.filter(g => g !== goal)
    }));
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          AI Course Recommendation System
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Student Profile
          </Typography>
          
          <TextField
            fullWidth
            label="Name"
            value={studentProfile.name}
            onChange={(e) => setStudentProfile(prev => ({ ...prev, name: e.target.value }))}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Major"
            value={studentProfile.major}
            onChange={(e) => setStudentProfile(prev => ({ ...prev, major: e.target.value }))}
            margin="normal"
          />

          <Box sx={{ my: 2 }}>
            <Typography variant="subtitle1">Academic Interests</Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
              <TextField
                size="small"
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                placeholder="Add interest"
              />
              <Button variant="contained" onClick={addInterest}>Add</Button>
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {studentProfile.academic_interests.map((interest, index) => (
                <Chip
                  key={index}
                  label={interest}
                  onDelete={() => removeInterest(interest)}
                />
              ))}
            </Box>
          </Box>

          <Box sx={{ my: 2 }}>
            <Typography variant="subtitle1">Career Goals</Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
              <TextField
                size="small"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                placeholder="Add goal"
              />
              <Button variant="contained" onClick={addGoal}>Add</Button>
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {studentProfile.career_goals.map((goal, index) => (
                <Chip
                  key={index}
                  label={goal}
                  onDelete={() => removeGoal(goal)}
                />
              ))}
            </Box>
          </Box>

          <Button
            variant="contained"
            color="primary"
            onClick={handleGetRecommendations}
            disabled={loading}
            sx={{ mt: 2 }}
          >
            Get Recommendations
          </Button>
        </Paper>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : recommendations.length > 0 ? (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Courses
            </Typography>
            <List>
              {recommendations.map((rec, index) => (
                <ListItem key={index} divider>
                  <ListItemText
                    primary={rec.course.title}
                    secondary={
                      <>
                        <Typography component="span" variant="body2" color="text.primary">
                          {rec.course.description}
                        </Typography>
                        <br />
                        Match Score: {Math.round(rec.match_score * 100)}%
                        <br />
                        {rec.reasons.map((reason, i) => (
                          <Typography key={i} component="div" variant="body2" color="text.secondary">
                            • {reason}
                          </Typography>
                        ))}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        ) : null}
      </Box>
    </Container>
  );
}

export default App; 