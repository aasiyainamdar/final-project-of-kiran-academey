-- Recruitment & Placement Management System - schema (MySQL 8)
CREATE DATABASE IF NOT EXISTS recruitment_db;
USE recruitment_db;

DROP TABLE IF EXISTS placements, joining_details, offers, interview_feedback, interview_rounds,
    application_status_history, applications, job_skills, jobs, companies, candidate_skills, candidates;

CREATE TABLE candidates (
    candidate_id   INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    phone          VARCHAR(15)  NOT NULL,
    qualification  VARCHAR(20)  NOT NULL,
    percentage     DECIMAL(5,2) NOT NULL,
    passing_year   INT          NOT NULL,
    technology     VARCHAR(50)  NOT NULL,
    backlogs       INT          NOT NULL DEFAULT 0,
    status         VARCHAR(20)  NOT NULL DEFAULT 'REGISTERED',
    registered_on  DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidate_skills (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id  INT NOT NULL,
    skill         VARCHAR(50) NOT NULL,
    UNIQUE (candidate_id, skill),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
);

CREATE TABLE companies (
    company_id     INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL UNIQUE,
    location       VARCHAR(100) NOT NULL,
    industry       VARCHAR(60),
    contact_email  VARCHAR(120),
    status         VARCHAR(10) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE jobs (
    job_id             INT AUTO_INCREMENT PRIMARY KEY,
    company_id         INT NOT NULL,
    title              VARCHAR(100) NOT NULL,
    technology         VARCHAR(50)  NOT NULL,
    min_qualification  VARCHAR(20)  NOT NULL,
    min_percentage     DECIMAL(5,2) NOT NULL,
    year_from          INT NOT NULL,
    year_to            INT NOT NULL,
    max_backlogs       INT NOT NULL DEFAULT 0,
    vacancies          INT NOT NULL,
    salary_lpa         DECIMAL(5,2) NOT NULL,
    status             VARCHAR(10) NOT NULL DEFAULT 'OPEN',
    posted_on          DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE job_skills (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    job_id  INT NOT NULL,
    skill   VARCHAR(50) NOT NULL,
    UNIQUE (job_id, skill),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

CREATE TABLE applications (
    application_id  INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id    INT NOT NULL,
    job_id          INT NOT NULL,
    applied_on      DATETIME DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(25) NOT NULL DEFAULT 'APPLIED',
    UNIQUE KEY uq_candidate_job (candidate_id, job_id),   -- duplicate application prevention
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE application_status_history (
    history_id      INT AUTO_INCREMENT PRIMARY KEY,
    application_id  INT NOT NULL,
    old_status      VARCHAR(25),
    new_status      VARCHAR(25) NOT NULL,
    changed_on      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);

CREATE TABLE interview_rounds (
    round_id        INT AUTO_INCREMENT PRIMARY KEY,
    application_id  INT NOT NULL,
    round_no        INT NOT NULL,
    round_type      VARCHAR(20) NOT NULL,
    scheduled_on    DATETIME NOT NULL,
    status          VARCHAR(15) NOT NULL DEFAULT 'SCHEDULED',
    UNIQUE (application_id, round_no),
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);

CREATE TABLE interview_feedback (
    feedback_id  INT AUTO_INCREMENT PRIMARY KEY,
    round_id     INT NOT NULL UNIQUE,
    rating       INT NOT NULL,
    remarks      VARCHAR(255),
    result       VARCHAR(10) NOT NULL,
    given_on     DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES interview_rounds(round_id)
);

CREATE TABLE offers (
    offer_id        INT AUTO_INCREMENT PRIMARY KEY,
    application_id  INT NOT NULL UNIQUE,
    salary_lpa      DECIMAL(5,2) NOT NULL,
    offer_date      DATE NOT NULL,
    status          VARCHAR(10) NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);

CREATE TABLE joining_details (
    joining_id    INT AUTO_INCREMENT PRIMARY KEY,
    offer_id      INT NOT NULL UNIQUE,
    joining_date  DATE NOT NULL,
    location      VARCHAR(100),
    FOREIGN KEY (offer_id) REFERENCES offers(offer_id)
);

CREATE TABLE placements (
    placement_id   INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id   INT NOT NULL,
    company_id     INT NOT NULL,
    job_id         INT NOT NULL,
    offer_id       INT NOT NULL UNIQUE,
    salary_lpa     DECIMAL(5,2) NOT NULL,
    placed_on      DATE NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (company_id)   REFERENCES companies(company_id),
    FOREIGN KEY (job_id)       REFERENCES jobs(job_id),
    FOREIGN KEY (offer_id)     REFERENCES offers(offer_id)
);
