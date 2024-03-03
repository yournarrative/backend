INSERT INTO documents (
    user_id,
    content,
    question,
    document_type
)
VALUES
(
 (SELECT id FROM users WHERE email = 'shayaan.jagtap@gmail.com'),
 'Shayaan is a data scientist and software engineering who knows python and sql.',
 'Who are you and what are your skills?',
 'Q&A'
),
(
 (SELECT id FROM users WHERE email = 'tryghosted@gmail.com'),
 'GhostedAI is a startup who knows how to get you to take adderall and code all weekend.',
 'Who are you and what are your skills?',
 'Q&A'
);