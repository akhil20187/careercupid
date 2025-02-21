# Product Requirements Document - Numerojobs

## 1. Product Overview
Numerojobs is an AI-powered job platform that combines traditional job matching with numerological compatibility analysis to create optimal matches between job seekers and employers.

## 2. MVP Features

### 2.1 User Authentication & Profile Management
#### Job Seekers
- Sign up/login with email or social media (LinkedIn/Google)
- Basic profile creation
  - Personal details (name, email, phone, date of birth)
  - Resume upload/builder
  - Career preferences (industry, job title, location)
  - Career goals (Looking for a new job, Complete career change, Transition to a new role )
  - Goal selection (learn/earn/work-life balance)

#### Recruiters
- Company profile creation
  - Basic company details
  - Incorporation date
  - Founder details (including DOB)
  - Company location and size

### 2.2 Core Features - Job Seekers (Free Tier)
1. **Resume Management**
   - Resume upload (PDF/DOC)
   - Basic resume parser to extract:
     - Personal information
     - Work experience
     - Education
     - Skills
   - 3 free resume generations

2. **Basic Numerological Analysis**
   - Life Path Number calculation
   - Expression Number calculation
   - Personality traits analysis
   - Career sector compatibility

3. **Job Search & Apply**
   - Search jobs by title, location, skills
   - View basic compatibility score
   - Apply to unlimited jobs
   - Track application status

### 2.3 Core Features - Recruiters (Free Tier)
1. **Job Posting Management**
   - Create up to 2 free job listings
   - Basic job details:
     - Title, description, location
     - Required skills
     - Experience level
     - Salary range
   - 20 candidate searches per job post

2. **Basic Candidate Search**
   - Filter by skills, experience, location
   - View basic compatibility scores
   - Access to candidate profiles
   - Basic communication system

## 3. Advanced Features (Post-MVP)

### 3.1 Premium Features - Job Seekers
1. **Advanced Career Guidance**
   - Personalized upskilling recommendations
   - Goal-based job suggestions
   - Career path planning

2. **Expert Counseling**
   - One-on-one sessions with numerology experts
   - Career counseling
   - Profile optimization

### 3.2 Premium Features - Recruiters
1. **Advanced Recruiting Tools**
   - Unlimited job postings
   - Advanced search filters
   - Bulk candidate processing
   - Detailed compatibility reports

2. **Analytics Dashboard**
   - Hiring metrics
   - Compatibility analytics
   - ROI tracking

## 4. Technical Requirements

### 4.1 Platform Architecture
- Web application (responsive design)
- RESTful API backend
- Secure user authentication
- Cloud-based infrastructure
- Database management system

### 4.2 Integration Requirements
- Email service provider
- SMS gateway
- Payment gateway
- Social media APIs
- Cloud storage

## 5. Data Requirements

### 5.1 Numerology Data
1. **Basic Numerological Calculations**
   ```
   Life Path Number = Sum of (Birth Date + Birth Month + Birth Year)
   Expression Number = Sum of (numerical values of all letters in full name)
   Personality Number = Sum of (numerical values of consonants in name)
   Heart's Desire Number = Sum of (numerical values of vowels in name)
   ```

2. **Letter-Number Mapping**
   ```
   1: A, J, S
   2: B, K, T
   3: C, L, U
   4: D, M, V
   5: E, N, W
   6: F, O, X
   7: G, P, Y
   8: H, Q, Z
   9: I, R
   ```

3. **Number Interpretations Database**
   - Personality traits for each number (1-9)
   - Career inclinations for each number
   - Compatible career sectors
   - Leadership styles
   - Work preferences

### 5.2 Job Market Data
1. **Industry Classifications**
   - Standard industry codes
   - Sector categories
   - Job role taxonomies

2. **Skills Database**
   - Technical skills
   - Soft skills
   - Industry-specific skills
   - Skill relationships and hierarchies

### 5.3 Compatibility Algorithms
1. **Basic Compatibility Score**
   ```
   Compatibility = (
     (Skill Match %) * 0.4 +
     (Numerological Match %) * 0.3 +
     (Goal Alignment %) * 0.3
   )
   ```

2. **Advanced Compatibility Metrics**
   - Manager-Employee compatibility
   - Company culture fit
   - Team dynamics
   - Growth potential

## 6. Security Requirements
- Encryption for sensitive data
- Secure authentication
- GDPR compliance
- Data backup and recovery
- Access control and permissions

## 7. Performance Requirements
- Page load time < 3 seconds
- Search results < 2 seconds
- Real-time notifications
- Support for concurrent users
- 99.9% uptime

## 8. Success Metrics
### 8.1 MVP Phase
- User registration rate
- Job application rate
- Job posting rate
- Basic compatibility accuracy
- User engagement metrics

### 8.2 Advanced Phase
- Premium conversion rate
- Placement success rate
- User satisfaction scores
- Platform retention rate
- Revenue metrics

## 9. Timeline
### Phase 1 (MVP) - 3 months
- Week 1-2: Design & Architecture
- Week 3-6: Core Features Development
- Week 7-8: Basic Numerology Integration
- Week 9-10: Testing & Bug Fixes
- Week 11-12: Beta Launch

### Phase 2 (Advanced Features) - 6 months
- Month 1-2: Premium Features Development
- Month 3-4: Advanced Algorithms
- Month 5: Testing & Optimization
- Month 6: Full Launch
