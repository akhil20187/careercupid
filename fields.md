# Report Generation API Fields

## Input Fields

### User Details (Form Data - JSON string)
- `name`: string
- `email`: string
- `date_of_birth`: string (Format: DD/MM/YYYY)
- `city`: string
- `career_goal`: enum
  - "Looking for a new job"
  - "Complete career change"
  - "Transition to a new role"

### File Upload
- `resume_file`: UploadFile (Resume document)

## Output Fields (CareerReport)

### User Details
- Contains all input fields from User Details above

### Numerology Report
- `life_path_number`: integer
- `life_path_explanation`: string
- `life_path_strengths`: string[]
- `life_path_challenges`: string[]
- `personality_number`: integer
- `personality_explanation`: string
- `personality_traits`: string[]

### Suitable Roles (Array)
Each role contains:
- `title`: string
- `explanation`: string

### Career Summary
A formatted string containing:
- Personal greeting
- Career journey
- Key achievements
- Core strengths
- Notable projects and impact
- Professional growth
- Potential growth directions
