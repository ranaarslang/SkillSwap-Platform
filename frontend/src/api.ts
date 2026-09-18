import axios from 'axios'
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })
export const demoMatches = [
  { id: 1, user: { id: 2, first_name: 'Maya', last_name: 'Chen', username: 'maya' }, bio: 'Product designer teaching Figma and design systems.', skills_offered: ['Product design', 'Figma', 'Design systems'], skills_wanted: ['React', 'Storytelling'], match_score: 94, avatar_color: '#f2b84b', is_verified: true },
  { id: 2, user: { id: 3, first_name: 'Jonah', last_name: 'Williams', username: 'jonah' }, bio: 'Frontend engineer who loves making complex things feel simple.', skills_offered: ['React', 'TypeScript', 'Accessibility'], skills_wanted: ['Photography', 'Figma'], match_score: 87, avatar_color: '#98c7b8', is_verified: true },
  { id: 3, user: { id: 4, first_name: 'Sana', last_name: 'Patel', username: 'sana' }, bio: 'Data storyteller turning messy questions into clear decisions.', skills_offered: ['Python', 'Data visualization', 'SQL'], skills_wanted: ['Public speaking', 'Brand strategy'], match_score: 81, avatar_color: '#d7a7bc', is_verified: true },
  { id: 4, user: { id: 5, first_name: 'Leo', last_name: 'Martins', username: 'leo' }, bio: 'Independent filmmaker, editor, and curious lifelong learner.', skills_offered: ['Video editing', 'Storytelling', 'Motion design'], skills_wanted: ['Product design', 'Python'], match_score: 76, avatar_color: '#b4a6d5', is_verified: true }
]
