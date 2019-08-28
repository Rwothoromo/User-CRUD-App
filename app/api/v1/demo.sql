CREATE VIEW question_details_view AS
SELECT
    q.id id,
    q.description question,
    q.created_by created_by_q,
    q.created_at created_at_q,
    a.id answer_id,
    a.description answer,
    a.created_by created_by_a,
    a.created_at created_at_a,
    c.name category
FROM
    questions q
    LEFT JOIN answers a ON q.id = a.question
    LEFT JOIN categories c ON q.category = c.id
