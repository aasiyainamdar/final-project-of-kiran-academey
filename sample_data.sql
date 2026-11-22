USE recruitment_db;
INSERT INTO companies (name, location, industry, contact_email) VALUES
 ('TechNova Solutions','Pune','IT Services','hr@technova.com'),
 ('DataBridge Analytics','Bengaluru','Analytics','jobs@databridge.com'),
 ('CloudPeak Systems','Hyderabad','Cloud','careers@cloudpeak.com');

INSERT INTO jobs (company_id,title,technology,min_qualification,min_percentage,year_from,year_to,max_backlogs,vacancies,salary_lpa) VALUES
 (1,'Python Developer','Python','BE',60,2023,2026,0,3,4.5),
 (2,'Data Analyst','Python','BSC',55,2022,2026,1,2,5.0),
 (3,'Java Developer','Java','BCA',60,2023,2026,0,2,4.0);
INSERT INTO job_skills (job_id,skill) VALUES (1,'Python'),(1,'MySQL'),(2,'Python'),(2,'SQL'),(3,'Java'),(3,'MySQL');

INSERT INTO candidates (name,email,phone,qualification,percentage,passing_year,technology,backlogs,status) VALUES
 ('Aarav Patil','aarav@example.com','9876543210','BE',72.5,2025,'Python',0,'VERIFIED'),
 ('Sneha Kulkarni','sneha@example.com','9822012345','BSC',58.0,2024,'Python',0,'VERIFIED'),
 ('Rohan Deshmukh','rohan@example.com','9890011223','BCA',66.0,2025,'Java',0,'VERIFIED'),
 ('Priya Joshi','priya@example.com','9765432109','BE',54.0,2025,'Python',2,'REGISTERED');
INSERT INTO candidate_skills (candidate_id,skill) VALUES
 (1,'Python'),(1,'MySQL'),(1,'SQL'),(2,'Python'),(2,'SQL'),(3,'Java'),(3,'MySQL'),(4,'Python');
